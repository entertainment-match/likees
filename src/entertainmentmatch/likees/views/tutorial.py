# Create your views here.
from entertainmentmatch.likees.services import CatalogService
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.utils.translation import activate, get_language
from django.conf import settings
from datetime import datetime
from django.utils.translation import ugettext as _
from django.core.paginator import Paginator, InvalidPage, EmptyPage

def index(request):
    return render_to_response('tutorial.html', {'section':'tutorial','subsection':'help'}, context_instance=RequestContext(request))

def tour(request):
    num_results = settings.NUM_RESULTS
    name_list = None
    if 'list' in request.GET:
        name_list = request.GET["list"]
    item_ids = []
    votesmap = {}

    if name_list is None:    
        tours = request.services.catalog.find_public_lists('tour')
        viewmap = {}
        viewmap['tours'] = tours

        return render_to_response('list-tours.html', viewmap, context_instance=RequestContext(request))

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
    
    filter_exclude_voted = True
    
    list = request.services.catalog.find_items_by_public_list(name_list, 'tour')
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

    faves = request.services.user.get_user_faves(user)
    ignored = request.services.user.get_user_ignored(user)
    wishlist = request.services.user.get_user_wishlist(user)
    
    breadcrumb = []
    breadcrumb.append({'title':_('Getting started'),      'url':'/tutorial/'})
    breadcrumb.append({'title':_('Tour'),  'url':'/tutorial/tour/?list='+name_list})

    # Mapa de retorno
    viewmap = {}
    viewmap['movies'] = itemspag
    viewmap['votes'] = votesmap
    viewmap['totalitems'] = totalitems 
    viewmap['tags'] = itemtagsmap
    viewmap['faves'] = faves
    viewmap['ignored'] = ignored
    viewmap['wishlist'] = wishlist
    viewmap['breadcrumb'] = breadcrumb
    viewmap['paginatorcontext'] = '/tutorial/tour/'
    viewmap['section'] = 'tutorial'
    viewmap['subsection'] = 'tours'

    return render_to_response('catalog-movies-tour.html', viewmap, context_instance=RequestContext(request))

