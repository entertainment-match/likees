from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.conf import settings
from django.core.paginator import Paginator, InvalidPage, EmptyPage

@login_required
def index(request):
    search_num_results = settings.DASHBOARD_MAX_ITEMS
    users_num_results = settings.DASHBOARD_MAX_USERS
    votesmap = {}
    
    user = request.user.id
    timezone = request.user.timezone

    # FIXME uservotes = request.services.vote.get_user_votes(user, search_num_results)
    uservotes = request.services.vote.get_user_votes(user)

    for vote in uservotes: 
        votesmap[vote.item.id] = vote.rate

    friends = request.services.user.get_friends(user)
   
    friend_list = request.services.user.get_friends_list(user,users_num_results)

    ignored = request.services.user.get_user_ignored(user,search_num_results)
    
    latestusers = request.services.user.get_latest_users(user, users_num_results)

    events = request.services.user.get_events(user, timezone, search_num_results)
   
    if events is None or len(events) == 0:
        return HttpResponseRedirect('/tutorial/')

    notifications = request.services.user.get_notifications(timezone)
    
    soulmates = request.services.soulmates.get_soulmates(user, settings.SOULMATE_LIMIT)
    
    # Mapa de retorno
    viewmap = {}
    viewmap['movies'] = list
    viewmap['friends'] = friends
    viewmap['friend_list'] = friend_list
    viewmap['uservotes'] = uservotes
    viewmap['votes'] = votesmap
    viewmap['ignored'] = ignored
    viewmap['latestusers'] = latestusers
    viewmap['events'] = events
    viewmap['notifications'] = notifications
    viewmap['soulmates'] = soulmates
    viewmap['section'] = 'dashboard'

    return render_to_response('dashboard.html', viewmap, context_instance=RequestContext(request))

@login_required
def events(request):
    num_results = settings.DASHBOARD_MAX_ITEMS
    votesmap = {}
   
    events = request.services.user.get_events(request.user.id, request.user.timezone)

    paginator = Paginator(events, num_results)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        eventspag = paginator.page(page)
    except (EmptyPage, InvalidPage):
        eventspag = paginator.page(paginator.num_pages)
 
    viewmap = {}
    viewmap['events'] = eventspag
    viewmap['section'] = 'dashboard'
    viewmap['subsection'] = 'events'
    
    return render_to_response('events.html', viewmap, context_instance=RequestContext(request))

@login_required
def friends(request):
    users_num_results = settings.DASHBOARD_MAX_USERS
    search_num_results = settings.DASHBOARD_MAX_ITEMS
    votesmap = {}
    
    user = request.user.id

    friends = request.services.user.get_friends(user)
    

    # Mapa de retorno
    viewmap = {}
    viewmap['movies'] = list
    viewmap['friends'] = friends
    viewmap['section'] = 'dashboard'
    viewmap['subsection'] = 'friends'

    return render_to_response('dashboard-friends.html', viewmap, context_instance=RequestContext(request))

@login_required
def search_user(request):
    users_num_results = settings.DASHBOARD_MAX_USERS
    search_num_results = settings.DASHBOARD_MAX_ITEMS
    votesmap = {}
    
    user = request.user.id
    friends = request.services.user.get_friends(user)
    username = request.POST["username_search"]
   
    users = []
    if not username == '': 
        users = request.services.catalog.find_user(user, username, True) 
    # Mapa de retorno
    viewmap = {}
    viewmap['movies'] = list
    viewmap['friends'] = friends
    viewmap['results'] = users
    viewmap['section'] = 'dashboard'
    viewmap['subsection'] = 'friends'
    
    return render_to_response('dashboard-friends.html', viewmap, context_instance=RequestContext(request))

@login_required
def soulmates(request):
    users_num_results = settings.DASHBOARD_MAX_USERS
    
    user = request.user.id

    friends = request.services.user.get_friends(user)
    soulmates = request.services.soulmates.get_soulmates(user, users_num_results)

    # Mapa de retorno
    viewmap = {}
    viewmap['soulmates'] = soulmates 
    viewmap['friends'] = friends
    viewmap['section'] = 'dashboard'
    viewmap['subsection'] = 'soulmates'

    return render_to_response('dashboard-soulmates.html', viewmap, context_instance=RequestContext(request))

@login_required
def lists(request):
    search_num_results = settings.DASHBOARD_MAX_ITEMS
    votesmap = {}
    
    user = request.user.id
    
    mytags = request.services.user.get_user_lists(user)

    itemstag = request.services.user.get_user_item_lists_by_list(user)
    wishlist = request.services.user.get_user_wishlist(user,search_num_results)

    # Mapa de retorno
    viewmap = {}
    viewmap['movies'] = list
    viewmap['itemstag'] = itemstag
    viewmap['wishlist'] = wishlist 
    viewmap['mytags'] = mytags 
    
    viewmap['section'] = 'dashboard'
    viewmap['subsection'] = 'lists'
    #TODO
    viewmap['votes'] = {}
    viewmap['tags'] = {}
    viewmap['ignored'] = {}
    viewmap['faves'] = {}
    
    return render_to_response('dashboard-lists.html', viewmap, context_instance=RequestContext(request))

@login_required
def add_facebook_id(request):
    id = request.GET['id']

    user_id = request.user.id
    preferences = request.services.user.get_user_settings(user_id)
    preferences['facebook_id'] = id
    request.services.user.update_settings(user_id,preferences)

    return HttpResponseRedirect('/accounts/profile')


@login_required
def del_facebook_id(request):
    user_id = request.user.id
    request.services.user.delete_setting(user_id,'facebook_id')

    return HttpResponseRedirect('/accounts/profile')

@login_required
def update_profile(request):
    name = None
    if 'name' in request.GET:
        name = request.GET['name']
    surname = None
    if 'surname' in request.GET:
        surname = request.GET['surname']
    gender = None
    if 'gender' in request.GET:
        gender = request.GET['gender']
    birthdate = None
    if 'birthdate' in request.GET:
        birthdate = request.GET['birthdate']
    if 'language' in request.GET:
        language = request.GET['language']
    if 'timezone' in request.GET:
        timezone = request.GET['timezone']
    if 'events' in request.GET:
        events = request.GET['events']
    if 'mail' in request.GET:
        mail = request.GET['mail']
    if 'facebook_post_votes' in request.GET:
        facebook_post_votes = request.GET['facebook_post_votes']
    if 'facebook_post_faves' in request.GET:
        facebook_post_faves = request.GET['facebook_post_faves']

    user_id = request.user.id

    request.services.user.update_profile(user_id,name,surname,gender,birthdate)

    if language == '':
        language = settings.DEFAULT_USER_LANGUAGE

    oldprefs = request.services.user.get_user_settings(user_id)

    preferences = {}
    preferences['language'] = language
    preferences['timezone'] = timezone
    preferences['events'] = events
    preferences['mail'] = mail
    preferences['facebook_post_votes'] = facebook_post_votes
    preferences['facebook_post_faves'] = facebook_post_faves
    if 'facebook_id' in oldprefs:
        preferences['facebook_id'] = oldprefs['facebook_id']

    request.services.user.update_settings(user_id, preferences)
    request.session.preferences = preferences    

    return HttpResponseRedirect('/accounts/profile/?saved=1')

@login_required
def view_profile(request):
    updated = False
    if 'saved' in request.GET:
        updated = True

    user = request.services.user.get_profile(request.user.username)
    user_id = request.user.id
    
    preferences = request.services.user.get_user_settings(user_id)

    viewmap = {}
    languages = [['',_('Default')], ['en',_('English')], ['es',_('Spanish')], ['fr',_('French')], ['rh',_('Reshulon')]]
    timezones = [['gmt-2','GMT-2'], ['gmt-1','GMT-1'], ['gmt+0','GMT+0'], ['gmt+1','GMT+1 Madrid'], ['gmt+2','GMT+2'], ['gmt+3','GMT+3'], ['gmt+4','GMT+4'], ['gmt+5','GMT+5'], ['gmt+6','GMT+6'], ['gmt+7','GMT+7']]

    viewmap['user'] = user
    viewmap['section'] = 'dashboard'
    viewmap['subsection'] = 'profile'
    viewmap['languages'] = languages
    viewmap['timezones'] = timezones 
    viewmap['updated'] = updated
    viewmap['preferences'] = preferences

    return render_to_response('dashboard-profile.html', viewmap, context_instance=RequestContext(request))


