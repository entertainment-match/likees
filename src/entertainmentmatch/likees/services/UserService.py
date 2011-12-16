from django.contrib.auth.models import User
from django.contrib.auth.models import UserManager
from django.core.files.images import get_image_dimensions
from django.utils.translation import ugettext as _
from django.core.mail import EmailMultiAlternatives, send_mail
from django.conf import settings
from django.db.models import Q
from django.template.loader import render_to_string
from entertainmentmatch.likees.models import Tag_Items, User_Settings, Notification, UserLikees, Tag, Movie, Item, Critic, Image, Event
from entertainmentmatch.likees.services import Service, VoteService
import hashlib
import pytz
from pytz import timezone
from datetime import datetime

class UserService(Service.Service):
    def get(self, user_id):
        return UserLikees.objects.get(pk=user_id)

    def get_profile(self, username):
        return UserLikees.objects.get(username__iexact=username)

    def get_profile_by_email(self, mail):
        return UserLikees.objects.get(email__iexact=mail)
    
    def get_user_soulmates(self, id):
        pass

    def get_latest_users(self, user_id, num_results=None):
        users = UserLikees.objects.select_related().all().exclude(pk=user_id).order_by('-id')
        if num_results is not None:
             users = users[:num_results]
        return users


    def get_friends(self, id, num_results=None):
        friendsuser = self.get_friends_list(id,num_results)
        friends = {}
        for frienduser in friendsuser:        
            friends[frienduser.id] = frienduser

        return friends

    def get_friends_list(self, id, num_results=None):
        
        friendsuser = UserLikees.objects.select_related().get(pk=id).user_friend.all()
        friendsuser = friendsuser.order_by('-id')
        if num_results is not None:
            friendsuser = friendsuser[:num_results]
        
        return friendsuser

    def add_friend(self, id_from, username):
        voteservice = VoteService.VoteService()
        user = UserLikees.objects.select_related().get(pk=id_from)
        friend = UserLikees.objects.get(username__iexact=username)
        if not friend is None and friend.id != id_from:
            user.user_friend.add(friend)
            user.save()
            #add to Event
            voteservice.update_event(user,None,'add_friend',friend)


    def del_friend(self, id_from, username):
        user = UserLikees.objects.select_related().get(pk=id_from)
        friend = UserLikees.objects.get(username__iexact=username)
        if not friend is None:
            user.user_friend.remove(friend)
            user.save()

    def add_critic(self, user_id, item_id, comment):
        critic = Critic(user_id = user_id, item_id = item_id, text = comment)
        critic.save()
        #add to Event
        item = Item.objects.get(pk=item_id)
        user = UserLikees.objects.get(pk=user_id)
        voteservice = VoteService.VoteService()
        voteservice.update_event(user,item,'add_critic',comment)

    def add_language(self, user_id, item_id, language, title, overview):
        item = Movie.objects.get(pk=item_id)

        item.name_es = title
        item.overview_es = overview
        item.save()
            
    def moderate(self, user_id, item_id, priority, delete, released):
        item = Movie.objects.get(pk=item_id)
        item.priority = priority
        item.deleted = delete
        item.released = released
        item.save()

    def del_critic(self, user_id, id):
        critic = Critic.objects.get(pk=id, user=user_id)
        critic.delete()

    def load_facebook_avatar(self, id):
        userlikees = UserLikees.objects.get(pk=id)
        
        prefs = self.get_user_settings(id)
        facebook_id = prefs['facebook_id']

        url = 'https://graph.facebook.com/' + facebook_id + '/picture'

        if userlikees.image is None:
            gravatar = Image(url = url)
            gravatar.save()
            userlikees.image_id = gravatar.id
            userlikees.save()
        else:
            userlikees.image.url = url
            userlikees.image.save()

    def load_gravatar(self, id):
        userlikees = UserLikees.objects.get(pk=id)

        hash = hashlib.md5(userlikees.email).hexdigest()
        url = 'http://www.gravatar.com/avatar/' + hash + '.png'

        if userlikees.image is None:
            gravatar = Image(url = url)
            gravatar.save()
            userlikees.image_id = gravatar.id
            userlikees.save()
        else:
            userlikees.image.url = url
            userlikees.image.save()

    def load_avatar(self, id, f):

        sub = ''

        if not f.content_type is None:
            main, sub = f.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'gif', 'png']):
                raise Exception(_('JPEG, PNG, GIF only.'))
        
        filename = str(id) + '.' + sub 
        filepath_temp = settings.AVATAR_PATH  + 'temp/' + filename
        filepath = settings.AVATAR_PATH + filename
        destination = open(filepath_temp, 'wb+')
        
        for chunk in f.chunks():
            destination.write(chunk)
        
        destination.close()
        import os
        import Image as ImagePIL
        
        img = None
        
        try:
            img = ImagePIL.open(filepath_temp)
            x, y = img.size
        except:
            os.remove(filepath_temp)
            raise Exception('Error al obtener la imagen.')
     
        # Checkeamos que el GIF no es animado
        if sub == 'gif':

            is_ani = True 

            try:
                img.seek(1)
            except EOFError:
                is_ani = False

            if is_ani:
                raise Exception('No se aceptan animaciones GIF.')

        if y > 100 or x > 100:
            os.remove(filepath_temp)
            raise Exception('Imagen demasiado grande, tamanyo maximo 100x100.')
       
        import shutil
        shutil.copy(filepath_temp, filepath)
        os.remove(filepath_temp)

        url = '/avatar/' + filename

        userlikees = UserLikees.objects.get(pk=id)

        if userlikees.image is None:
            avatar = Image(url = url)
            avatar.save()
            userlikees.image_id = avatar.id
            userlikees.save()
        else:
            userlikees.image.url = url
            userlikees.image.save()

    def add_item_list(self, user_id, item_id, name_list):
        lists = self.get_user_lists(user_id)
        item = Item.objects.get(pk=item_id)
        user = UserLikees.objects.get(pk=user_id)
        tags = Tag.objects.filter(user=user, name=name_list)
        if not name_list in lists:
            tag_ = Tag(name=name_list, user=user)
            tag_.save()
        else:
            self.del_item_list(user_id,item_id,name_list)
            tag_ = tags[0]
            ti = Tag_Items(tag=tag_, item=item)
            ti.save()

    def add_item_fave(self, user_id, item_id):
        self.add_item_list(user_id, item_id, 'fave')
        #add to Event
        voteservice = VoteService.VoteService()
        user = UserLikees.objects.get(pk=user_id)
        item = Item.objects.get(pk=item_id)
        voteservice.update_event(user,item,'add_fave',None)

    def del_item_fave(self, user_id, item_id):
        self.del_item_list(user_id, item_id, 'fave')

    def add_item_wishlist(self, user_id, item_id):
        self.add_item_list(user_id, item_id, 'wishlist')
        #add to Event
        voteservice = VoteService.VoteService()
        user = UserLikees.objects.get(pk=user_id)
        item = Item.objects.get(pk=item_id)
        voteservice.update_event(user,item,'add_wishlist',None)

    def del_item_wishlist(self, user_id, item_id):
        self.del_item_list(user_id, item_id, 'wishlist')

    def add_item_ignore(self, user_id, item_id):
        self.add_item_list(user_id, item_id, 'ignore')

    def del_item_ignore(self, user_id, item_id):
        self.del_item_list(user_id, item_id, 'ignore')

    def get_user_lists_tag(self, user_id):
        return Tag.objects.select_related().filter(user=user_id)

    def get_user_lists(self, user_id):
        tags = self.get_user_lists_tag(user_id)
        taglist = []
        for tag in tags:
            taglist.append(tag.name)
        return sorted(set(taglist))            

    def get_user_item_lists_by_list(self, user_id):
        itemstaguser = Tag.objects.select_related().filter(user=user_id).order_by('name')
        itemtagsmap = {}
        for itemtaguser in itemstaguser:    
            itemtagsmap[itemtaguser.name] = itemtaguser.items.all()
        return itemtagsmap            

    def get_user_ignored(self, user_id, num_results=None):
        ignored = self.get_user_list(user_id,'ignore',num_results)
        userignored = {}
        i = 0
        for item in ignored:        
            userignored[item.id] = item
            i = i + 1
            if not num_results is None and i == num_results:
                break

        return userignored

    def get_user_ignored_list_item(self, user_id):
        return self.get_user_list(user_id,'ignore')

    def get_user_faved_list_item(self, user_id):
        return self.get_user_list(user_id,'fave')

    def get_user_ignored_list(self, user_id):
        return self.get_user_list(user_id, 'ignore')

    def count_wishlist(self, user_id):
        return len(Tag.objects.select_related().get(user=user_id, type='wishlist').items.all())


    def get_user_list(self, user_id, list_name, num_results=None):
        tag = Tag.objects.select_related().get(user=user_id, type=list_name)
        return tag.items.all()

    def get_user_wishlist(self, user_id, num_results=None):
        wishlist = self.get_user_list(user_id,'wishlist',num_results)
        userwishlist = {}
        i = 0

        for item in wishlist:
            userwishlist[item.id] = item
            i = i + 1
            if not num_results is None and i == num_results:
                break

        return userwishlist

    def get_user_wishlist_list(self, user_id):
        return self.get_user_list(user_id,'wishlist')
           
    def get_user_faves(self, user_id, num_results=None):
        faves = self.get_user_list(user_id,'fave',num_results)
        userfaves = {}
        i = 0

        for item in faves:
            userfaves[item.id] = item
            i = i + 1
            if not num_results is None and i == num_results:
                break

        return userfaves

    def get_user_item_lists(self, user_id):
        lists = self.get_user_lists_tag(user_id) 
        itemtagsmap = {}
        for tag in lists:
            for item in tag.items.all():
                if item.id not in itemtagsmap.keys():
                    itemtagsmap[item.id] = []
                itemtagsmap[item.id].append(tag.name)
        return itemtagsmap            


    def del_item_list(self, user_id, item_id, name_list):
        user = User.objects.get(pk=user_id)
        item = Item.objects.get(pk=item_id)
        tag = Tag.objects.get(user=user,name=name_list)
        ti = Tag_Items.objects.filter(item=item, tag=tag)
        for t in ti:
            t.delete()

    def update_profile(self, user_id, name, surname, gender, birthdate):
        userlikees = UserLikees.objects.get(pk=user_id)        
        
        if name is not None:
            userlikees.first_name = name
        
        if surname is not None:
            userlikees.last_name = surname

        if gender is not None:
            userlikees.gender = gender
        
        if birthdate is not None:
            userlikees.birthdate = birthdate
        userlikees.save()
        

    def create_user(self, username, name, surname, mail, gender, birthdate, password):
        #user = User.objects.create_user(username, mail, password)
        
        userlikees = User.objects.filter(email__iexact = mail)
        if userlikees:
            msg = _("There is an existing user with this email.")
            raise Exception(msg)


        userlikees = User.objects.filter(username__iexact = username)
        if userlikees:
            msg = _("This username is already in use. Please, pick another one")
            raise Exception(msg)

        passwd = password
        userlikees = UserLikees.objects.create_user(username, mail, passwd)
      
        hash = settings.HASH_SALT + userlikees.email 
        token = hashlib.md5(hash).hexdigest()

        # Contruccion del link de validacion
        link = settings.TEMPLATE_DOMAIN + 'accounts/validate/?token=' + token + '&username=' + username

        subject = _("Welcome to likees!")
        fro = "register@likees.org"
        msg = render_to_string('users/mail-register.html', { 'user': userlikees, 'link': link, 'password': passwd, 'TEMPLATE_DOMAIN': settings.TEMPLATE_DOMAIN})
        
        m = EmailMultiAlternatives(subject, msg, fro, [mail])
        m.content_subtype = "html"
        m.send()

        if name is not None:
            userlikees.first_name = name
        
        if surname is not None:
            userlikees.last_name = surname
        userlikees.is_active = 0
        userlikees.save()

        if gender is not None:
            userlikees.gender = gender
        
        if birthdate is not None:
            userlikees.birthdate = birthdate
        userlikees.save()
        return userlikees   

    def change_password(self, user_id, old, new):
        u = User.objects.get(id = user_id)
        if old is None or u.check_password(old):
            u.set_password(new)
            u.save()
        else:
            msg = ("The password is incorrect. Please, try again.")
            raise Exception(msg)
            
    def reset_password(self, mail):
        userlikees = User.objects.get(email__iexact = mail)
        if userlikees:

            hash = settings.HASH_SALT + userlikees.email 
            token = hashlib.md5(hash).hexdigest()

            # Contruccion del link de validacion
            link = settings.TEMPLATE_DOMAIN + 'accounts/remember/?token=' + token + '&username=' + userlikees.username
            
            subject = _("Password recover on Likees")
            fro = "no_reply@likees.org"
        
            msg = render_to_string('users/mail-recover-password.html', { 'user': userlikees, 'link': link, 'TEMPLATE_DOMAIN': settings.TEMPLATE_DOMAIN})

            m = EmailMultiAlternatives(subject, msg, fro, [mail])
            m.content_subtype = "html"
            m.send()
            
            # Activamos el user por si acaso no esta activado

            userlikees.is_active = 1
            userlikees.save()

    def get_notifications(self, user_timezone):
        now = datetime.now()
        notifications = Notification.objects.filter(date_on__lte=now,date_off__gte=now).order_by('-id')
        return notifications

    def get_events(self, user_id, user_timezone, num=None):
        friends = self.get_friends(user_id)        
        events = Event.objects.filter(Q(from_user=user_id) | (Q(from_user__in=friends) & ~Q(action='add_wishlist')))
        events = events.order_by('-when')
        if num is not None: 
            events = events[:num]

        for event in events:
            if user_timezone is not None:
                event.when = event.when.replace(tzinfo=pytz.utc).astimezone(timezone(user_timezone))

        return events
        
    def init_settings(self, user):
        setting = User_Settings(user_id=user.id, key='timezone',value=settings.DEFAULT_USER_TIMEZONE)
        setting.save()
        setting = User_Settings(user_id=user.id, key='events',value=settings.DEFAULT_USER_PUBLISH_EVENTS)
        setting.save()
        setting = User_Settings(user_id=user.id, key='language',value=settings.DEFAULT_USER_LANGUAGE)
        setting.save()
        setting = User_Settings(user_id=user.id, key='mail',value=settings.DEFAULT_USER_NOTIFY_MAIL)
        setting.save()
        setting = User_Settings(user_id=user.id, key='facebook_post_votes',value=settings.DEFAULT_FACEBOOK_PUBLISH_VOTES)
        setting.save()
        setting = User_Settings(user_id=user.id, key='facebook_post_faves',value=settings.DEFAULT_FACEBOOK_PUBLISH_FAVES)
        setting.save()

    def delete_setting(self, user_id, key):
        prefs = User_Settings.objects.filter(user=user_id, key=key)
        for pref in prefs:
            pref.delete()

    def delete_settings(self, user_id):
        settings = User_Settings.objects.filter(user=user_id) 
        for setting in settings:
            setting.delete()
    
    def update_settings(self, user_id, setts):

        user = UserLikees.objects.get(pk=user_id)
        self.delete_settings(user_id)

        for key,value in setts.items():
            sett = User_Settings(user=user, key=key, value=value)
            sett.save()
        #language = User_Settings(user=user, key='language', value=language)
        #language.save()
        #timezone = User_Settings(user=user, key='timezone', value=timezone)
        #timezone.save()
        #events = User_Settings(user=user, key='events', value=events)
        #events.save()
        #mail = User_Settings(user=user, key='mail', value=mail)
        #mail.save()
    
    def get_user_settings(self, user_id):
        prefs = User_Settings.objects.filter(user=user_id)
        preferences = {}
        for pref in prefs:
            preferences[pref.key] = pref.value
        return preferences

    def notify(self, to, friend):
        to = self.get_profile(to)
        
        # check permissions
        setts = self.get_user_settings(to.id)
        notify = setts['mail']

        if notify == '1':
            subject = _("You have a new follower on Likees")
            fro = "register@likees.org"
            msg = render_to_string('users/mail-newfollow.html', { 'username': to.username, 'friend': friend, 'TEMPLATE_DOMAIN': settings.TEMPLATE_DOMAIN})
            
            m = EmailMultiAlternatives(subject, msg, fro, [to.email])
            m.content_subtype = "html"
            m.send()

    def send_contact (self, contact):

        mail = 'seekil.nimda@gmail.com'
        subject = _("New query from: ") + contact['name']
        fro = contact['mail']
        msg = 'Type: ' + contact['type']+ '\nQuery: ' + contact['query']
        
        send_mail(subject, msg, fro, [mail])
            
    def create_list(self, username, name):
        user = self.get_profile(username)
        tag = Tag(name=name, type=name,user=user)
        tag.save()

    # Checks user's privacy options and post the message on facebook, twitter, etc. 
    def publish_social_networks(self, user, item, action, message):
        # Facebook
        preferences = self.get_user_settings(user.id)
        # User is connected to facebook
        result = {}
        if 'facebook_id' in preferences:
            permission = 'ask'
            if 'add_fave' == action and 'facebook_post_faves' in preferences:
                permission = preferences['facebook_post_faves']
            if 'vote' == action and 'facebook_post_votes' in preferences:
                permission = preferences['facebook_post_votes']
            result['facebook'] = permission

        return result
            



