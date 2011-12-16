from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.conf import settings
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from datetime import datetime

def index(request):
    language = request.language
    num_results = settings.NUM_RESULTS

    item_ids = []
    votesmap = {}
    # Filtro de fecha
    filter_from_year = None
    try:
        filter_from_year = int(request.GET.get('from',1900))
    except ValueError:
        filter_from_year = 1900
    filter_to_year = None
    try:
        filter_to_year = int(request.GET.get('to',3000))
    except ValueError:
        filter_to_year = 3000
    filter_category = request.GET.get('category')
    filter_orderby = request.GET.get('orderby')
    filter_exclude_voted = request.GET.get('excludevoted')
    
    filter_from = datetime.strptime("01/01/"+str(filter_from_year), "%d/%m/%Y")
    filter_to = datetime.strptime("31/12/"+str(filter_to_year), "%d/%m/%Y")
    list = request.services.catalog.get_last_items(request.user.id, filter_from, filter_to, filter_category, filter_orderby, filter_exclude_voted)
    paginator = Paginator(list, num_results)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        itemspag = paginator.page(page)
    except (EmptyPage, InvalidPage):
        itemspag = paginator.page(paginator.num_pages)

   
    for item in itemspag.object_list: 
        item_ids.append(item.id)
   
    user = request.user.id
    votes = request.services.vote.get_votes(user, item_ids) 
    
    for vote in votes: 
        votesmap[vote.item.id] = vote.rate

    categories = request.services.catalog.get_list_categories(request.language)
    totalitems = request.session['total_items']

    itemtagsmap = request.services.user.get_user_item_lists(user)

    # Construimos el breadcrumb
    breadcrumb = []
    breadcrumb.append({'title':_('Movies'),  'url':'/movies/'})

    # Mapa de retorno
    viewmap = {}
    viewmap['movies'] = itemspag
    viewmap['votes'] = votesmap
    viewmap['categories'] = categories
    viewmap['totalitems'] = totalitems 
    viewmap['tags'] =  itemtagsmap
    
    viewmap['breadcrumb'] = breadcrumb 
    viewmap['section'] = 'movies'
    viewmap['subsection'] = 'explore'

    return render_to_response('catalog-movies.html', viewmap, context_instance=RequestContext(request))



@login_required
def get_ignored(request):
    search_num_results = settings.DASHBOARD_MAX_ITEMS
    votesmap = {}
    
    user = request.user.id

    ignored = request.services.user.get_user_ignored_list_item(user)
    ignored_l = request.services.user.get_user_ignored(user)
    paginator = Paginator(ignored, search_num_results)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        ignoredpag = paginator.page(page)
    except (EmptyPage, InvalidPage):
        ignoredpag = paginator.page(paginator.num_pages)
    
    itemtagsmap = request.services.user.get_user_item_lists(user)

    # Construimos el breadcrumb
    breadcrumb = []
    breadcrumb.append({'title':_('Movies'),      'url':'/movies/'})
    breadcrumb.append({'title':_('Ignored'),  'url':'/ignored/'})
 
    # Mapa de retorno
    viewmap = {}
    viewmap['movies'] = ignoredpag
    viewmap['wishlist'] = {}
    viewmap['tags'] = itemtagsmap
    viewmap['ignored'] = ignored_l
    viewmap['breadcrumb'] = breadcrumb 
    viewmap['section'] = 'movies'
    viewmap['subsection'] = 'ignored'

    return render_to_response('catalog-movies-ignored.html', viewmap, context_instance=RequestContext(request))


@login_required
def get_favourites(request):
    search_num_results = settings.DASHBOARD_MAX_ITEMS
    votesmap = {}
    
    user = request.user.id

    faved = request.services.user.get_user_faved_list_item(user)
    ignored_l = request.services.user.get_user_ignored(user)
    paginator = Paginator(faved, search_num_results)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        favedpag = paginator.page(page)
    except (EmptyPage, InvalidPage):
        favedpag = paginator.page(paginator.num_pages)
    
    itemtagsmap = request.services.user.get_user_item_lists(user)

    # Construimos el breadcrumb
    breadcrumb = []
    breadcrumb.append({'title':_('Movies'),      'url':'/movies/'})
    breadcrumb.append({'title':_('Favourites'),  'url':'/favourites/'})
 
    # Mapa de retorno
    viewmap = {}
    viewmap['movies'] = favedpag
    viewmap['tags'] = itemtagsmap
    viewmap['ignored'] = ignored_l
    viewmap['breadcrumb'] = breadcrumb 
    viewmap['section'] = 'movies'
    viewmap['subsection'] = 'favourites'

    # Hashmap para los botones y demas
    faves = {}
    
    for f in favedpag.object_list:
        faves[f.id] = f
    
    viewmap['faves'] = faves 

    return render_to_response('catalog-movies-favourites.html', viewmap, context_instance=RequestContext(request))

@login_required
def get_voted(request):
    num_results = settings.DASHBOARD_MAX_ITEMS
    votesmap = {}
    
    user = request.user.id
    uservotes = request.services.vote.get_user_votes(user)
    
    paginator = Paginator(uservotes, num_results)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        uservotespag = paginator.page(page)
    except (EmptyPage, InvalidPage):
        uservotespag = paginator.page(paginator.num_pages)
 
    list = []
    for vote in uservotes: 
        votesmap[vote.item.id] = vote.rate
        
    itemtagsmap = request.services.user.get_user_item_lists(user)

    # Construimos el breadcrumb
    breadcrumb = []
    breadcrumb.append({'title':_('Movies'),      'url':'/movies/'})
    breadcrumb.append({'title':_('Last voted'),  'url':'/votes/'})

    # Mapa de retorno
    viewmap = {}
    viewmap['uservotes'] = uservotespag # Aqui no pasamos 'movies' pq accederemos desde Vote
    viewmap['votes'] = votesmap
    viewmap['tags'] = itemtagsmap
    viewmap['breadcrumb'] = breadcrumb 
    viewmap['section'] = 'movies'
    viewmap['subsection'] = 'votes'
    
    return render_to_response('catalog-movies-votes.html', viewmap, context_instance=RequestContext(request))

@login_required
def get_recommendations(request):
    num_results = settings.NUM_RESULTS
    item_ids = []
    votesmap = {}
 
    # Filtro de fecha
    filter_from_filter = None
    try:
        filter_from_year = int(request.GET.get('from',1900))
    except ValueError:
        filter_from_year = 1900
    filter_to_year = None
    try:
        filter_to_year = int(request.GET.get('to',3000))
    except ValueError:
        filter_to_year = 3000
    filter_category = request.GET.get('category')
    filter_orderby = request.GET.get('orderby')
    
    filter_from = datetime.strptime("01/01/"+str(filter_from_year), "%d/%m/%Y")
    filter_to = datetime.strptime("31/12/"+str(filter_to_year), "%d/%m/%Y")
    
    filter_exclude_voted = request.GET.get('excludevoted')
    
    list = request.services.catalog.get_recommendations(request.user.id, filter_from,filter_to,filter_category,filter_orderby,filter_exclude_voted)
    paginator = Paginator(list, num_results)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        itemspag = paginator.page(page)
    except (EmptyPage, InvalidPage):
        itemspag = paginator.page(paginator.num_pages)

   
    for item in itemspag.object_list: 
        item_ids.append(item.id)
   
    user = request.user.id
    votes = request.services.vote.get_votes(user, item_ids) 
    
    for vote in votes: 
        votesmap[vote.item.id] = vote.rate

    totalitems = request.session['total_items']

    itemtagsmap = request.services.user.get_user_item_lists(user)
    categories = request.services.catalog.get_list_categories(request.language)
    
    # Construimos el breadcrumb
    breadcrumb = []
    breadcrumb.append({'title':_('Movies'),      'url':'/movies/'})
    breadcrumb.append({'title':_('Recommendations'),  'url':'/recommendations/'})

    # Mapa de retorno
    viewmap = {}
    viewmap['movies'] = itemspag
    viewmap['votes'] = votesmap
    viewmap['totalitems'] = totalitems 
    viewmap['tags'] = itemtagsmap
    viewmap['categories'] = categories
    viewmap['breadcrumb'] = breadcrumb
    viewmap['section'] = 'movies'
    viewmap['subsection'] = 'recommendations'

    return render_to_response('catalog-movies-recommendations.html', viewmap, context_instance=RequestContext(request))

def get_estrenos(request):
    num_results = settings.NUM_RESULTS
    item_ids = []
    
    votesmap = {}
    name_list = 'cartelera_es'
    estrenos = request.services.catalog.find_items_release_by_public_list(name_list, 'cartelera')
    
    user = request.user.id
    
    # Construimos el breadcrumb
    breadcrumb = []
    breadcrumb.append({'title':_('Movies'),      'url':'/movies/'})
    breadcrumb.append({'title':_('Now playing in cinemas'),  'url':'/new/'})

    wishlist = []
    if user is not None:
        wishlist = request.services.user.get_user_wishlist(user)
    
    # Mapa de retorno
    viewmap = {}
    viewmap['estrenos'] = estrenos
    viewmap['votes'] = {}
    viewmap['wishlist'] = wishlist
    viewmap['ignored'] = {}
    viewmap['tags'] = {}
    viewmap['breadcrumb'] = breadcrumb
    viewmap['section'] = 'movies'
    viewmap['subsection'] = 'now playing in cinemas'

    return render_to_response('catalog-movies-estrenos.html', viewmap, context_instance=RequestContext(request))


@login_required 
def get_wishlist(request):
    num_results = settings.NUM_RESULTS
    item_ids = []
    votesmap = {}
    
    list = request.services.user.get_user_wishlist_list(request.user.id)
    request.session["num_wishlist"] = len(list)    
    paginator = Paginator(list, num_results)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        itemspag = paginator.page(page)
    except (EmptyPage, InvalidPage):
        itemspag = paginator.page(paginator.num_pages)
   
    for item in itemspag.object_list: 
        item_ids.append(item.id)
   
    user = request.user.id
    
    itemtagsmap = request.services.user.get_user_item_lists(user)
    
    # Construimos el breadcrumb
    breadcrumb = []
    breadcrumb.append({'title':_('Movies'),      'url':'/movies/'})
    breadcrumb.append({'title':_('I want to watch'),  'url':'/wishlist/'})

    wishlist = request.services.user.get_user_wishlist(user)
    
    # Mapa de retorno
    viewmap = {}
    viewmap['movies'] = itemspag
    viewmap['votes'] = {}
    viewmap['wishlist'] = wishlist
    viewmap['ignored'] = {}
    viewmap['tags'] = itemtagsmap
    viewmap['breadcrumb'] = breadcrumb
    viewmap['section'] = 'movies'
    viewmap['subsection'] = 'wishlist'

    return render_to_response('catalog-movies-wishlist.html', viewmap, context_instance=RequestContext(request))

def search(request):
    search_num_results = settings.SEARCH_NUM_RESULTS
    num_results = settings.NUM_RESULTS
    search = request.GET["search"]

    list = []
    people = []
    
    if search is not None and search != '':
        list = request.services.catalog.find_movies(search)
        people = request.services.catalog.find_people_l(search, search_num_results)
    
    item_ids = []
    votesmap = {}
 
    paginator = Paginator(list, search_num_results)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        itemspag = paginator.page(page)
    except (EmptyPage, InvalidPage):
        itemspag = paginator.page(paginator.num_pages)

   
    for item in itemspag.object_list: 
        item_ids.append(item.id)
  
    totalitems = len(list) 

    user = request.user.id
    votes = request.services.vote.get_votes(user, item_ids) 
    
    for vote in votes: 
        votesmap[vote.item.id] = vote.rate
    
    itemtagsmap = request.services.user.get_user_item_lists(user)
    
    # Construimos el breadcrumb
    breadcrumb = []
    breadcrumb.append({'title':_('Movies'),      'url':'/movies/'})
    breadcrumb.append({'title':_('Search'),  'url':'/search/'})
    
    # Mapa de retorno
    viewmap = {}
    viewmap['movies'] = itemspag
    viewmap['people'] = people
    viewmap['totalitems'] = totalitems 
    viewmap['votes'] = votesmap
    viewmap['search'] = search
    viewmap['tags'] = itemtagsmap
    viewmap['breadcrumb'] = breadcrumb 
    viewmap['section'] = 'catalog'

    return render_to_response('search.html', viewmap, context_instance=RequestContext(request))

def view_movie(request, item):
    item = request.services.catalog.get(item)

    votesmap = {}
    
    item_ids = []
    item_ids.append(item.id)    

    user = request.user.id
    
    votes = request.services.vote.get_votes(user, item_ids) 
    
    for vote in votes: 
        votesmap[vote.item.id] = vote.rate

    trailerurl = ''

    if item.trailer:
        trailerurl = item.trailer.split('=')[0]

    cast = request.services.catalog.get_cast(item.id)
    itemtagsmap = request.services.user.get_user_item_lists(user)
    critics = request.services.catalog.get_critics(item.id)

    usersvoted = request.services.vote.get_last_users_voted_item(item.id,settings.ITEM_DETAIL_MAX_USERS,user)
    
    friendsvoted = {}
    if user is not None:
        friends = request.services.user.get_friends(user)
        friendsvoted = request.services.vote.get_last_friends_voted_item(friends,item.id,settings.ITEM_DETAIL_MAX_USERS)
    
    mytags = request.services.user.get_user_lists(user)
    
    # Construimos el breadcrumb
    breadcrumb = []
    breadcrumb.append({'title':_('Movies'),  'url':'/movies/'})
    breadcrumb.append({'title':item.name,   'url':'/item/' + str(item.id) + '/title/' + item.normalized_name()})
   
    # Mapa de retorno
    viewmap = {}
    viewmap['item'] = item
    viewmap['critics'] = critics
    viewmap['trailerurl'] = trailerurl
    viewmap['votes'] = votesmap
    viewmap['cast'] = cast
    viewmap['section'] = 'catalog'

    # TODO: Mejorar el servicio para que solo reciba el id de la peli
    if itemtagsmap.has_key(item.id):
        viewmap['tags'] = {item.id:itemtagsmap[item.id]}
        viewmap['tagsitem'] = itemtagsmap[item.id]
    viewmap['usersvoted'] = usersvoted
    viewmap['friendsvoted'] = friendsvoted
    viewmap['breadcrumb'] = breadcrumb 

    viewmap['mytags'] = mytags 

    return render_to_response('detail.html', viewmap, context_instance=RequestContext(request))

def view_trailer(request, item):
    item = request.services.catalog.get(item)

    trailerurl = '' 

    if item.trailer:
        trailerurl = 'http://www.youtube.com/embed/' + item.trailer.split('=')[1] + '?autoplay=1&amp;start=1' 

    # Mapa de retorno
    viewmap = {}
    viewmap['link'] = trailerurl

    return render_to_response('youtube-trailer.html', viewmap, context_instance=RequestContext(request))


