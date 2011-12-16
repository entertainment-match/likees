# Create your views here.
from entertainmentmatch.likees.services import CatalogService
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.utils.translation import activate, get_language

def index(request):
    if not request.user.id is None:
        return HttpResponseRedirect('/likees/dashboard')
    # Cargar datos de la home
    else: 
        # TODO: hacer una cartelera por pais
        name_list = 'cartelera_es'
        itemlist = request.services.catalog.find_items_release_by_public_list(name_list, 'cartelera')
        items = []
        for iteml in itemlist:
            for it in itemlist[iteml]:
                items.append(it)
        # Mapa de retorno
        viewmap = {}
        viewmap['movies'] = items
        viewmap['section'] = 'home' 

        return render_to_response('home.html', viewmap, context_instance=RequestContext(request))

def test():
    return 'hello'
