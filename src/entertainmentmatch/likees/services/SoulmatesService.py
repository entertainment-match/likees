from entertainmentmatch.likees.services import Service
from entertainmentmatch.likees.models import Vote, Item, Soulmates_Coef, UserLikees
from django.db.models import Q
from django.conf import settings
from django.db import transaction

class SoulmatesService(Service.Service):
    def get_soulmates(self, user_id, limit):
        soulmates_coef = Soulmates_Coef.objects.select_related().filter(Q(user1=user_id) | Q(user2=user_id)).order_by('-coef')[:limit] 
        
        soulmates = []

        for coef in soulmates_coef:
            soulmate = None

            # Como el coeficiente G es bidireccional y solo se calcula n/2 el user sera user1 o user2
            if coef.user1.id == user_id:
                soulmate = coef.user2
            else:
                soulmate = coef.user1

            element = [soulmate, coef.coef]
            soulmates.append(element) 

        return soulmates 

    def get_soulmate_movies(self, user_id):
        soulmates = self.get_soulmates(user_id, settings.SOULMATE_LIMIT)
    
        if soulmates is None or len(soulmates) == 0:
            return None
        
        soulmate_ids = []
        for soulmate in soulmates:
            soulmate_ids.append(soulmate[0].id)

        votes = Vote.objects.filter(user__in=soulmate_ids)

        items = []
        for vote in votes:
            items.append(vote.item.id)
        return Item.objects.filter(id__in=items)

    @transaction.commit_on_success
    def get_soulmates_by_user(self, user):
        """
        Calcula la afinididad de un usuario con el resto de usuarios.
    
        """
        Soulmates_Coef.objects.filter(Q(user1=user) | Q(user2=user)).delete()
    
        votes_user = Vote.objects.filter(user=user.id)
        
        if votes_user.count() < 40:
            return
        
        votes_a = {}
    
        for vote_user in votes_user:
            votes_a[vote_user.item.id] = vote_user.rate
    
        users = UserLikees.objects.all().exclude(pk=user.id)
    
        for user_soul in users:
            votes_soul = Vote.objects.filter(user=user_soul.id)
    
            if votes_soul.count() < 40:
                continue
    
            votes_b = {}
    
            for vote_soul in votes_soul:
                votes_b[vote_soul.item.id] = vote_soul.rate
    
            print "Calculando coef G entre " + user.username + "(" + str(votes_user.count()) + ")" + " " + user_soul.username + "(" + str(votes_soul.count()) + ")" + "..."
    
            coef = Soulmates_Coef()
            coef.user1 = user
            coef.user2 = user_soul
            coef.coef = self.soulmates(votes_a, votes_b)
            coef.save()
    
    def soulmates(self, votes_x, votes_y):
        """
        Algoritmo encargado de encontrar la afinidad entre
        los votos del user1 y el user2.
    
        """
        ita = iter(sorted(votes_x.iteritems()))
        itb = iter(sorted(votes_y.iteritems()))
       
        enda = False
        endb = False
    
        coefG = 0
        coefGCount = 0
    
        if not enda:
            try:
                vote_x = ita.next()
            except StopIteration:
                enda = True
        
        if not endb:
            try:
                vote_y = itb.next()
            except StopIteration:
                endb = True
    
        while not enda and not endb:
    
            key_x, value_x = vote_x
            key_y, value_y = vote_y
            
            if key_x == key_y:
                
                coefGCount = coefGCount + 1

                # Comparten la misma pelicula
                coefD = abs(value_x - value_y)
    
                if 5 > coefD and coefD > 2:
                    coefG = coefG + 1
                elif coefD == 2:
                    coefG = coefG + 5
                elif coefD == 1:
                    coefG = coefG + 10
                elif coefD == 0:
                    coefG = coefG + 20
                
                try:
                    vote_x = ita.next()
                except StopIteration:
                    enda = True
                
                try:
                    vote_y = itb.next()
                except StopIteration:
                    endb = True
            elif key_x < key_y:
                # No coinciden, avanzamos el iterador de A
                try:
                    vote_x = ita.next()
                except StopIteration:
                    enda = True
            elif key_x > key_y:
                # No coinciden, avanzamos el iterador de B
                try:
                    vote_y = itb.next()
                except StopIteration:
                    endb = True
        if coefGCount == 0:
            return 0
        else:
            # return (coefG * 100) / (coefGCount * 20)
            return (coefG * 5) / coefGCount
    
    def get_soulmates_all_users():
        """
        Encuentra la afinidad entre todos los usuarios.
         
        """
        users1 = UserLikees.objects.all()
        users2 = UserLikees.objects.all()
        
        Soulmates_Coef.objects.all().delete()
         
        for user1 in users1:
            votes1 = Vote.objects.filter(user=user1.id)
            
            if votes1.count() < 40:
                continue
            
            votes_a = {}
            
            for vote1 in votes1:
                votes_a[vote1.item.id] = vote1.rate
                
                for user2 in users2:
                    if user1.id == user2.id:
                        break
                    
                    votes2 = Vote.objects.filter(user=user2.id)
                    
                    if votes2.count() < 40:
                        continue
                        
                    votes_b = {}
                    
                    for vote2 in votes2:
                        votes_b[vote2.item.id] = vote2.rate
                    
                        print "Calculando coef G entre " + user1.username + "(" + str(votes1.count()) + ")" + " " + user2.username + "(" + str(votes2.count()) + ")" + "..."
                         
                        coef = Soulmates_Coef()
                        coef.user1 = user1
                        coef.user2 = user2
                        coef.coef = soulmates (votes_a, votes_b)
                        coef.save()
