'''
Created on 19/01/2011

@author: dysphoria
'''
from entertainmentmatch.likees.models import Event, Vote
from django.db.models import Q

def main():
    eventos = Event.objects.using('likees_pro').all().filter(Q(action='vote')).order_by('when')
    
    for evento in eventos:
        vote = Vote(
                user_id=evento.from_user_id,
                item_id=evento.item_id,
                rate=evento.value,
                date=evento.when)
        
        aux = Vote.objects.using('likees_pro').all().filter(Q(item=evento.item_id) & Q(user=evento.from_user_id))
        
        for a in aux:
            vote.id = a.id
        
        vote.save(using='likees_pro')