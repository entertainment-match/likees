from entertainmentmatch.likees.models import Item, UserLikees, Vote, Event
from entertainmentmatch.likees.services import Service
from django.db import connection

class VoteService(Service.Service):
    def vote(self, user_id, item_id, rate):
        
        vote = Vote.objects.filter(user=user_id,item=item_id)

        if vote is not None:
            for v in vote: 
                v.delete()

        vote = Vote(user_id=user_id, item_id=item_id, rate=rate)
        vote.save()

        #add vote to Event
        user = UserLikees.objects.get(pk=user_id)
        item = Item.objects.get(pk=item_id)
        votes_count = item.votes_count
        if votes_count is None:
            votes_count = 1
        else:
            votes_count += 1
        item.votes_count = votes_count
        item.save()
        self.update_event(user,item,'vote',rate)

    def get_item_ratings(self, item_id):
        cursor = connection.cursor() 
        cursor.execute("SELECT rate, count(*) FROM likees_vote WHERE item_id = %s GROUP BY rate", [item_id]) 
        rates = cursor.fetchall() 

        rating = dict.fromkeys(range(1,11), 0)

        for rate in rates:
            rating[rate[0]] = rate[1]

        return rating 

    def update_event(self, user_id, item, action, value):
        events = Event.objects.filter(from_user=user_id, item=item, action=action)
        user = UserLikees.objects.get(pk=user_id)
        for event in events:
            event.delete()
        event = Event(from_user=user,item=item, action=action, value=value) 
        event.save()


    def remove_vote(self, user_id, item_id):
        
        vote = Vote.objects.filter(user=user_id,item=item_id)

        item = Item.objects.get(pk=item_id)

        if vote is not None:
            for v in vote: 
                v.delete()
                item.votes_count -= 1

        item.save()
                

    def update_rating(self, item_id):
        vote = Vote.objects.filter(item=item_id)

        rating = 0.0
        count = 0
        if vote is not None:
            for v in vote:
                count = count + 1
                rating = rating + v.rate
            item = Item.objects.get(pk=item_id)
            if count == 0:
                item.rating = None
            else:
                item.rating = rating / count
            item.save()

    # Le pasas un array de ids de items y devuelve una hashmap de item->voto, para un user_id especifico.
    def get_votes(self, user_id, item_ids):
        
        votes = Vote.objects.filter(user__exact=user_id).filter(item__in=item_ids)
        return votes

    def get_user_votes(self, user_id, num_results=None):
        votes = Vote.objects.filter(user__exact=user_id).order_by('-date')
        if num_results is not None:
            votes = votes[:num_results]
        return votes
    
    def get_user_votes_num(self, user_id):
        return len(self.get_user_votes(user_id))

    def get_last_users_voted_item(self, item_id, num_results=None, user_id=None):
        voted = Vote.objects.select_related().filter(item=item_id).order_by('-date')

        if user_id is not None:
            voted = voted.exclude(user=user_id)

        if num_results is not None:
            voted = voted[:num_results]

        return voted

    def get_last_friends_voted_item(self, friends, item_id, num_results=None):
        voted = Vote.objects.select_related().filter(item=item_id, user__in=friends).order_by('-date')
        if num_results is not None:
            voted = voted[:num_results]
        return voted
