from django.utils.translation import activate, get_language
from entertainmentmatch.likees.models import User_Settings
from entertainmentmatch.likees.services import CatalogService, UserService, VoteService, SoulmatesService
from django.conf import settings

class LazyServices(): 
    pass

class LikeesMiddleware(object):
    def process_view(self,request,view_func,view_args,view_kwargs):
       
        # Initialize basic services
        request.__class__.services = LazyServices
        
        request.services.catalog = CatalogService.CatalogService()
        request.services.user = UserService.UserService()
        request.services.vote = VoteService.VoteService()
        request.services.soulmates = SoulmatesService.SoulmatesService()
        
        language = settings.DEFAULT_USER_LANGUAGE
        timezone = settings.DEFAULT_USER_TIMEZONE
        events = str(settings.DEFAULT_USER_PUBLISH_EVENTS)
        mail = str(settings.DEFAULT_USER_NOTIFY_MAIL)

        default_language = True
        if 'language' in request.GET:
            default_language = False
            language = request.GET['language']
        elif request.user.id is not None and request.session is not None:
            # si no hay language en la sesion hay que recargar todo
            if 'preferences' not in request.session:
                #Load default values
                preferences = {}
                preferences['language'] = language
                preferences['timezone'] = timezone
                preferences['events'] = events
                preferences['mail'] = mail

                prefs = request.services.user.get_user_settings(request.user.id)    
                for key,value in prefs.items():
                    preferences[key] = value
                language = preferences['language']
                default_language = 'default' == language
                request.session['preferences'] = preferences
            else:
                language = request.session['preferences']['language']
                default_language = 'default' == language
         # Activate the correct language 
        if default_language:
            language = get_language() 
            if request.META.has_key('HTTP_ACCEPT_LANGUAGE'):
                # Part the accepted language
                languages = []
                if request.META['HTTP_ACCEPT_LANGUAGE'].find(',') > -1:
                    languages = request.META['HTTP_ACCEPT_LANGUAGE'].split(',')
                else:
                    languages.append(request.META['HTTP_ACCEPT_LANGUAGE'])
                language = languages[0]
                if language.find('-') > -1:
                    language = language.split('-')[0]
        activate(language)
        request.__class__.language = ''
        request.language = language
       
        if request.session is not None:
            # Force expire user's session cookie when user's web browser is closed
            request.session.set_expiry(0)
            if not 'total_items' in request.session:
                request.session['total_items'] = request.services.catalog.count_items()
    
            if request.user.id is not None:
                user_id = request.user.id
                if not 'num_wishlist' in request.session and user_id is not None:
                    request.session['num_wishlist'] = request.services.user.count_wishlist(user_id)


            if not 'language' in request.session:
                request.session['language'] = language

            #if not 'timezone' in request.session:
            #    request.session['timezone'] = timezone

            #if not 'events' in request.session:
            #    request.session['events'] = events

            #if not 'mail' in request.session:
            #    request.session['mail'] = mail
