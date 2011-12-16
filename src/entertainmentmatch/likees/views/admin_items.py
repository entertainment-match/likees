from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.utils.translation import ugettext as _
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.utils.translation import activate, get_language
import random
from datetime import datetime
from django.utils.translation import ugettext as _

def admin(request):
    item_ids = []
    votesmap = {}
    catalog = request.services.catalog

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
    list = catalog.get_last_items(request.user.id, filter_from, filter_to, filter_category, filter_orderby)

    paginator = Paginator(list, 20)
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

    categories = {}


    # Mapa de retorno
    viewmap = {}
    viewmap['movies'] = itemspag
    viewmap['categories'] = categories 
    viewmap['section'] = 'admin'
    viewmap['ignored'] = {}
    viewmap['votes'] = {}
    viewmap['tags'] = {}
    viewmap['faves'] = []
    viewmap['wishlist'] = []
    return render_to_response('admin.html', viewmap, context_instance=RequestContext(request))


