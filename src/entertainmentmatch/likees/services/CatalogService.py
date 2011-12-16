from django.db.models import Q
from entertainmentmatch.likees.models import Tag_Items, Movie, Person, Category, Item_Job_Cast_Person, Tag, Critic, UserLikees
from entertainmentmatch.likees.services import Service, SoulmatesService, UserService, VoteService
import datetime
from stabledict import StableDict

class CatalogService(Service.Service):
    def get_movies_filtered(self, user_id, from_date, to_date, category, orderby, excludevoted, min_votes, movies=None):
        if movies is None:
            movies = Movie.objects.filter(deleted=0,priority__lt=10)
        if not min_votes == 0:
            movies = movies.filter(votes_count__gte=min_votes)
        # exclude user ignored
        if user_id is not None:
            userservice = UserService.UserService()
            ignored = userservice.get_user_ignored_list(user_id)
            movies = movies.exclude(id__in=ignored)
        # filters
        if from_date is not None:
            movies = movies.filter(released__gte=from_date)
        if to_date is not None:
            movies = movies.filter(released__lte=to_date)
        if category is not None and category != '':
            movies = movies.filter(categories=category)
        if excludevoted is not None:
            voteservice = VoteService.VoteService()
            votes = voteservice.get_user_votes(user_id)
            item_ids = []
            for vote in votes:
                item_ids.append(vote.item.id)
            movies = movies.exclude(id__in=item_ids)
        if orderby is not None:
            if orderby == 'brate':
                movies = movies.order_by('-rating','-votes_count')
            elif orderby == 'wrate':
                movies = movies.order_by('rating','-votes_count')
            elif orderby == 'news':
                movies = movies.order_by('-released')    
            elif orderby == 'olds':
                movies = movies.order_by('released')    
            elif orderby == 'recommendations':
                movies = movies.order_by('-priority','-rating','-votes_count')
            elif orderby == 'default_last_items':
                movies = movies.order_by('-priority','-released')
        else:
            movies = movies.order_by('-priority','-votes_count','-rating')
        return movies
    def get_last_items(self, user_id, from_date, to_date, category, orderby, excludevoted=False):
        return self.get_movies_filtered(user_id, from_date, to_date, category, orderby, excludevoted,0)
    def get_recommendations(self, user_id, from_date, to_date, category, orderby, excludevoted):
        if orderby is None:
            orderby = 'recommendations'
        service = SoulmatesService.SoulmatesService()
        movies_soulmates = service.get_soulmate_movies(user_id)
        movies = self.get_movies_filtered(user_id, from_date, to_date, category, orderby, 'True',3, movies_soulmates)
        return movies.exclude(Q(rating=None))
    def find_movies(self, token):
        movies = list([])
        
        q_name_equal = Q(name_es=token)
        q_original_name_equal = Q(original_name=token)
        q_alternative_name_equal = Q(alternative_name=token)
        
        movies_equal = Movie.objects.filter((q_name_equal) | (q_original_name_equal) | (q_alternative_name_equal)).order_by('-rating')
        
        movies.extend(movies_equal)
        
        found_equal = []
        
        for movie in movies:
            found_equal.append(movie.id)
            
        q_name_starts = Q(name_es__istartswith=token)
        q_original_name_starts = Q(original_name__istartswith=token)
        q_alternative_name_starts = Q(alternative_name__istartswith=token)
        
        movies_starts = Movie.objects.filter(((q_name_starts) | (q_original_name_starts) | (q_alternative_name_starts))  & ~Q(id__in=found_equal)).order_by('-rating')
        
        movies.extend(movies_starts)
        
        found = []
        for movie in movies:
            found.append(movie.id)
        
        words = token.split()
        
        q_name_es = Q(name_es__icontains=words[0])
        q_name_en = Q(name_en__icontains=words[0])
        q_name_fr = Q(name_fr__icontains=words[0])
        q_original_name = Q(original_name__icontains=words[0])
        q_alternative_name = Q(alternative_name__icontains=words[0])
        i = 1
        
        while i < words.__len__():
            q_name_es = q_name_es & Q(name_es__icontains=words[i])
            q_name_en = q_name_en & Q(name_en__icontains=words[i])
            q_name_fr = q_name_fr & Q(name_fr__icontains=words[i])
            q_original_name = q_original_name & Q(original_name__icontains=words[i])
            q_alternative_name = q_alternative_name & Q(alternative_name__icontains=words[i])
            
            i += 1
            
        # movies that contains all words
        movies_all = Movie.objects.filter(((q_name_es) | (q_name_en) | (q_name_fr) | (q_original_name) | (q_alternative_name)) & ~Q(id__in=found)).order_by('-rating')
        
        movies.extend(movies_all)
        
        return (movies)
    def find_people(self, token):
        self.find_people_l(token, None)
    def find_people_l(self, token, limit):
        people = Person.objects.filter(Q(name__icontains=token))
        if limit is not None:
            people = people[:limit]
        return people
    def get(self, id):
        return Movie.objects.get(id=id)
    def get_category(self, id):
        return Category.objects.get(pk=id)
    def get_person(self, id):
        return Person.objects.get(pk=id)
    def find_user(self, user_id, username, exclude_friends=True):
        users = UserLikees.objects.filter(Q(username__icontains=username) & Q(is_active=1))
        if exclude_friends:
            userservice = UserService.UserService()
            friends = userservice.get_friends(user_id)
            users = users.exclude(id__in=friends)
        return users
    def get_cast(self, item):
        return Item_Job_Cast_Person.objects.select_related().filter(item = item)
    def get_critics(self, item):
        return Critic.objects.select_related().filter(item=item).order_by('-date')
    def count_items(self):
        return Movie.objects.filter(Q(deleted=0) & Q(priority__lt=10)).count()
    def get_newest_items(self, limit=10):
        return Movie.objects.filter(Q(deleted=0) & Q(priority__lt=10)).order_by('-priority','-id')[:limit]
    def find_items_by_person(self, id_person):
        itemsperson = Item_Job_Cast_Person.objects.select_related().filter(person=id_person)
        items = []
        for itemperson in itemsperson:
            if not itemperson.item in items:
                items.append(itemperson.item.id)
        return CatalogService.find_items_by_array(self, items)
    def find_items_by_array(self, ids_item):
        return Movie.objects.select_related().filter(id__in=ids_item).order_by('-released')
 
    def find_items_by_company(self, id_company):
        return None
    def find_items_by_category(self, user_id, id_category, from_date, to_date, orderby, excludevoted):
        if orderby is None:
            orderby = 'default_last_items'
        return self.get_movies_filtered(user_id, from_date, to_date, id_category, orderby, excludevoted,0)

    def find_public_lists(self, type_):
        tag = Tag.objects.filter(type=type_)
        return tag

    def find_items_by_public_list(self, name_list, type_, order_by=None):
        tag = Tag.objects.get(name=name_list, type=type_)
        
        if tag is None:
            return None
        
        list = []
        
        if order_by is None:
            items = tag.items.all()
        else:
            items = tag.items.all().order_by(order_by)

        for item in items:    
            list.append(item)
            
        return list          
      
    def find_items_release_by_public_list(self, name_list, type_):
        tag = Tag.objects.get(name=name_list, type=type_)
        
        if tag is None:
            return None
        
        itemsrel = StableDict()
        now = datetime.datetime.now()

        itemstag = Tag_Items.objects.filter(tag=tag, date_ini__lte=now).exclude(date_end__lte=now).order_by('-date_ini')

        for item in itemstag:    
            date = item.date_ini
            if itemsrel.has_key(date):
                itemsrel[date].append(item.item)
            else:
                itemsrel[date] = [item.item]
        
        #al introducir los items ordenados en un hash se pierde el orden
        #hay que pensar otra manera de enviar los datos a la vista
#        new_item = {}
#        sorted_keys = itemsrel.keys()
#        sorted_keys.sort()
#
#        for key in sorted_keys:
#            new_item[key] = []
#            for item in itemsrel[key]:
#                new_item[key].append(item)

        return itemsrel

    def find_items_by_user_list(self, id_user, name_list):
        return None  
    def get_list_categories(self, language):
        if language == 'fr':
            return Category.objects.all().order_by('name_fr')        
        elif language == 'es':
            return Category.objects.all().order_by('name_es')        
        else:    
            return Category.objects.all().order_by('name_en')        
        
