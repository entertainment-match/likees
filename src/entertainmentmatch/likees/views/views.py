from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.conf import settings
from django.utils.translation import ugettext as _
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.utils import simplejson
from django.conf import settings
from django import forms
from django.forms.util import ErrorList
from datetime import datetime
from likees.forms.profile_forms import ChangePasswordForm 
import random
import hashlib
import re

def login_user_without_password(request, username):
    if not username is None:
        user = authenticate(username=username) 
        if user is not None:
            if user.is_active:
                login(request, user)
            else:
                return None
    return user 

def login_user(request): 
    username = None
    password = None
    if request.POST.has_key('username'):
        username = request.POST['username']
    if request.POST.has_key('password'):
        password = request.POST['password']
    if not username is None and not password is None:
        if username.find("@") > -1:
            user = request.services.user.get_profile_by_email(username)
            if user is not None:
                username = user.username
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect("/dashboard/")
            else:
                #disabled
                return render_to_response('users/login-inactive.html', {}, context_instance=RequestContext(request))
        else:
            # user/password is not valid
            return render_to_response('users/login-incorrect.html', {}, context_instance=RequestContext(request))

    return render_to_response('users/login.html', {}, context_instance=RequestContext(request))

def create_user(request):
    username = request.POST['username'].strip()
    password = request.POST['password'].strip()
    email = request.POST['mail'].strip()
    pattern = r'[^\.a-zA-Z0-9\-\_]'
    if re.search(pattern, username):
        msg = _("Username only can contain characters, numbers, '.', '-' and '_'")
        return HttpResponse(msg)
    if password is None or password == '':
        msg = _("Password too short")
        return HttpResponse(msg)
    if email is None or email == '' or email.find("@") == -1 or email.find(".") == -1:
        msg = _("E-mail address not valid")
        return HttpResponse(msg)
    #birthdate = request.POST['birthdate']
    #if birthdate == '':
    #    birthdate = None
    #name = request.POST['name'].strip()
    #surname = request.POST['surname'].strip(),
    #email, 
    #gender = request.POST['gender']
    #, birthdate,password)

    user = request.services.user.create_user(username,None,None, email, None,None,password) 
    # msg = _("Your user has been created successfully. Please, check your e-mail")

    request.services.user.init_settings(user)

    request.services.user.create_list(username, 'wishlist')
    request.services.user.create_list(username, 'ignore')
    request.services.user.create_list(username, 'fave')
    return render_to_response('users/register-sendmail.html', {'reguser': user}, context_instance=RequestContext(request))

def find_items_by_category(request, category_id):
    num_results = settings.NUM_RESULTS

    category = request.services.catalog.get_category(category_id)

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
    
    items = request.services.catalog.find_items_by_category(request.user.id,category_id,filter_from, filter_to, filter_orderby, filter_exclude_voted)
    
    item_ids = []
    votesmap = {}
 
    paginator = Paginator(items, num_results)
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
    
    itemtagsmap = request.services.user.get_user_item_lists(user)
    
    categories = request.services.catalog.get_list_categories(request.language)
    
    # Construimos el breadcrumb
    breadcrumb = []
    breadcrumb.append({'title':_('Movies'),  'url':'/movies/'})
    breadcrumb.append({'title': category.name,   'url':'/category/' + str(category_id)})

    # Mapa de retorno
    viewmap = {}
    viewmap['movies'] = itemspag
    viewmap['selected_category'] = long(category.id)
    viewmap['categories'] = categories 
    viewmap['people'] = {}
    viewmap['votes'] = votesmap
    viewmap['section'] = 'catalog'
    viewmap['tags'] = itemtagsmap
    viewmap['breadcrumb'] = breadcrumb 
    viewmap['paginatorcontext'] = '/category/' + str(category_id) + '/'
    
    return render_to_response('catalog-movies-category.html', viewmap, context_instance=RequestContext(request))

def find_items_by_person(request, person):
    num_results = settings.NUM_RESULTS
    items = request.services.catalog.find_items_by_person(person)
    
    item_ids = []
    votesmap = {}
    
    paginator = Paginator(items, num_results)
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
    
    p = request.services.catalog.get_person(person)
    
    itemtagsmap = request.services.user.get_user_item_lists(user)
    
    # Construimos el breadcrumb
    breadcrumb = []
    breadcrumb.append({'title':_('Movies'),  'url':'/movies/'})
    breadcrumb.append({'title':p.name,   'url':'/person/' + str(p.id)})

    # Mapa de retorno
    viewmap = {}
    viewmap['movies'] = itemspag
    viewmap['person'] = p
    viewmap['people'] = {}
    viewmap['votes'] = votesmap
    viewmap['section'] = 'catalog'
    viewmap['tags'] = itemtagsmap
    viewmap['breadcrumb'] = breadcrumb 
    viewmap['paginatorcontext'] = '/person/' + str(p.id) + '/'

    return render_to_response('person.html', viewmap, context_instance=RequestContext(request))


def view_validate(request):
    tokenmail = request.GET["token"]
    username = request.GET["username"]
    
    userlikees = request.services.user.get_profile(username)
    
    hash = settings.HASH_SALT + userlikees.email 
    token = hashlib.md5(hash).hexdigest()

    if tokenmail == token:
        userlikees.is_active = 1
        userlikees.save()
        return render_to_response('users/register-validationok.html', {'reguser': userlikees}, context_instance=RequestContext(request))
    else:
        return render_to_response('users/register-validationko.html', {'reguser': userlikees}, context_instance=RequestContext(request))

    return HttpResponse()

def view_mail_register(request):
    user = request.services.user.get_profile(request.user.username)
    
    username='test'
    token='test'

    link = settings.TEMPLATE_DOMAIN + 'accounts/validate/?token=' + token + '&username=' + username
    
    return render_to_response('users/mail-register.html', {'user': user, 'link': link}, context_instance=RequestContext(request))

def view_mail_remember(request):
    user = request.services.user.get_profile(request.user.username)
    
    username='test'
    token='test'

    link = settings.TEMPLATE_DOMAIN + 'accounts/remember/?token=' + token + '&username=' + username
    
    return render_to_response('users/mail-recover-password.html', {'user': user, 'link': link}, context_instance=RequestContext(request))

@login_required
def set_avatar(request):

    user = request.services.user.get_profile(request.user.username)
    if request.method == 'POST':
    
        avatarop = request.POST["avatarop"]
  
        if avatarop == 'gravatar':
            request.services.user.load_gravatar(request.user.id)
            data = {'result':'ok'}
            return HttpResponse(simplejson.dumps(data), mimetype='application/json')
        
        if avatarop == 'facebook':
            try:
                request.services.user.load_facebook_avatar(request.user.id)
                data = {'result':'ok'}
                return HttpResponse(simplejson.dumps(data), mimetype='application/json')
            except Exception as exc:
                data = {'result':'ko','msg':str(exc)}
                return HttpResponse(simplejson.dumps(data), mimetype='application/json')

        if avatarop == 'upload':
            try:
                request.services.user.load_avatar(request.user.id, request.FILES['file'])
            except Exception as exc:
                data = {'result':'ko','msg':str(exc)}
                return HttpResponse(simplejson.dumps(data), mimetype='application/json')

            data = {'result':'ok'}
            return HttpResponse(simplejson.dumps(data), mimetype='application/json')

    hash = hashlib.md5(user.email).hexdigest()
    glink = 'http://www.gravatar.com/avatar/' + hash + '.png'

    return render_to_response('users/profile-avatar.html', {'user': user, 'glink': glink}, context_instance=RequestContext(request))

@login_required
def view_user(request, username):
    num_results = settings.NUM_RESULTS
    user = request.services.user.get_profile(username)
    votesmap = {}

    uservotes = request.services.vote.get_user_votes(user)
    paginator = Paginator(uservotes, num_results)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        votespag = paginator.page(page)
    except (EmptyPage, InvalidPage):
        votespag = paginator.page(paginator.num_pages)

    for vote in votespag.object_list:
        votesmap[vote.item.id] = vote.rate 

    faves = request.services.user.get_user_faves(user)
    
    friends = request.services.user.get_friends(request.user.id)
    wishlist = request.services.user.get_user_wishlist(request.user.id)
    
    # Mapa de retorno
    viewmap = {}
    viewmap['ouser'] = user
    viewmap['votes'] = votesmap
    viewmap['uservotes'] = votespag
    viewmap['faves'] = faves
    viewmap['friends'] = friends
    viewmap['section'] = 'catalog'
    viewmap['wishlist'] = wishlist
    viewmap['searchcontext'] = '/user/' + username + '/'
    viewmap['totalvoted'] = paginator.count
    return render_to_response('userdetail.html', viewmap, context_instance=RequestContext(request))

def view_user_infotip(request, username):
    num_results = settings.NUM_RESULTS
    user = request.services.user.get_profile(username)
    votesmap = {}

    uservotes = request.services.vote.get_user_votes(user)
    paginator = Paginator(uservotes, num_results)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        votespag = paginator.page(page)
    except (EmptyPage, InvalidPage):
        votespag = paginator.page(paginator.num_pages)

    for vote in votespag.object_list:
        votesmap[vote.item.id] = vote.rate 

    faves = request.services.user.get_user_faves(user)
    
    friends = request.services.user.get_friends(request.user.id)
    wishlist = request.services.user.get_user_wishlist(request.user.id)
    
    # Mapa de retorno
    viewmap = {}
    viewmap['ouser'] = user
    viewmap['votes'] = votesmap
    viewmap['uservotes'] = votespag
    viewmap['faves'] = faves
    viewmap['friends'] = friends
    viewmap['section'] = 'catalog'
    viewmap['wishlist'] = wishlist
    viewmap['searchcontext'] = '/user/' + username + '/'
    return render_to_response('users/infotip.html', viewmap, context_instance=RequestContext(request))

def rate_detail(request, item):
    ratings = request.services.vote.get_item_ratings(item)

    # transformamos el ratings a {rate:[count:322,percent:12%]}
    total = 0
    for key in ratings.keys():
        total += ratings[key]

    ratedetail = {}
    for key in ratings.keys():
        detail = {}
        detail['count'] = ratings[key]
        if total != 0:
            detail['percent'] = ratings[key] * 100 / total
        ratedetail[key] = detail
    viewmap = {}
    viewmap['ratings'] = ratedetail

    return render_to_response('ratedetail.html', viewmap, context_instance=RequestContext(request))

@login_required
def vote_movie(request, item):
   
    rank = request.GET["vote"]
    user = request.user.id   

    movie = request.services.catalog.get(item)

    if movie is None:
        msg = _("The film you try to vote does not exists")
        raise Exception, msg
    if int(rank) > 10 or int(rank) < 0:
        msg = _("Invalid punctuation")
        raise Exception, msg

    if int(rank) == 0:
        request.services.vote.remove_vote(user,item)
        request.services.vote.update_rating(item)
        if 'total_voted' in request.session:
            request.session['total_voted'] = request.session['total_voted'] - 1

    else:
        request.services.vote.vote(user, item, rank)
        request.services.vote.update_rating(item)

        request.services.user.del_item_wishlist(user, item)
        if 'total_voted' in request.session:
            request.session['total_voted'] = request.session['total_voted'] + 1

    return HttpResponse()

def find_items_by_ids(request, item_ids):
    return catalog.find_items_by_array(item_ids)

@login_required
def get_votes(request, item_ids):
    user = request.user.id
    return request.services.vote.get_votes(user, item_ids) 

@login_required
def get_user_votes(request):
    user = request.user.id
    return request.services.vote.get_user_votes(user)

@login_required
def add_item_list(request, item):
    user = request.user.id
    tag = request.POST["value"]
    request.services.user.add_item_list(user, item, tag)

    return HttpResponse()

@login_required
def add_item_fave(request, item):
    user = request.user.id
    request.services.user.add_item_fave(user, item)

    return HttpResponse()

@login_required
def del_item_fave(request, item):
    user = request.user.id
    request.services.user.del_item_fave(user, item)
    return HttpResponse()


@login_required
def add_item_wishlist(request, item):
    user = request.user.id
    request.services.user.add_item_wishlist(user, item)
    wishlist = request.services.user.get_user_wishlist(user)
    request.session["num_wishlist"] = len(wishlist)
    return HttpResponse()

@login_required
def del_item_wishlist(request, item):
    user = request.user.id
    request.services.user.del_item_wishlist(user, item)
    wishlist = request.services.user.get_user_wishlist(user)
    request.session["num_wishlist"] = len(wishlist)
    return HttpResponse()

@login_required
def add_item_ignore(request, item):
    user = request.user.id
    request.services.user.add_item_ignore(user, item)
    return HttpResponse()

@login_required
def del_item_ignore(request, item):
    user = request.user.id
    request.services.user.del_item_ignore(user, item)
    return HttpResponse()

@login_required
def get_user_lists(request):
    user = request.user.id
    return request.services.user.get_user_lists(user)

@login_required
def del_item_list(request, item):
    user = request.user.id
    tag = request.POST["value"]
    request.services.user.del_item_list(user, item, tag)
    return HttpResponse()

@login_required
def change_password(request):
    user = request.user.id
    if request.method == 'POST': # If the form has been submitted...
        form = ChangePasswordForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            old = None
            #old = form.cleaned_data['password_old']
            new = form.cleaned_data['password_new']
            confirm = form.cleaned_data['password_confirm']
            
            try:
                request.services.user.change_password(user, old, new)
                return render_to_response('users/login-passchanged.html', {}, context_instance=RequestContext(request))
            except Exception as exc:
                form._errors["password_old"] = ErrorList([_(str(exc))])
            
    else:
        form = ChangePasswordForm() # An unbound form
    
    return render_to_response('users/change.html', { 'form': form }, context_instance=RequestContext(request))

def reset_password(request):
    if 'email' in request.POST:
        email = request.POST["email"]
        request.services.user.reset_password(email)
        return render_to_response('users/reset-ok.html', {}, context_instance=RequestContext(request))
    else:
        return render_to_response('users/reset.html', {}, context_instance=RequestContext(request))

def remember_password(request):
  
    if 'token' not in request.GET or 'username' not in request.GET:
        return render_to_response('users/reset.html', {}, context_instance=RequestContext(request))

    tokenmail = request.GET["token"]
    username = request.GET["username"]
    userlikees = request.services.user.get_profile(username)
    
    hash = settings.HASH_SALT + userlikees.email 
    token = hashlib.md5(hash).hexdigest()
    if tokenmail == token:
        login_user_without_password(request, username)
        return HttpResponseRedirect('/accounts/change_password/')
    else:
        return HttpResponse('Validation fail')

    return HttpResponse()

@login_required
def add_friend(request, friend):
    request.services.user.add_friend(request.user.id, friend)
    request.services.user.notify(friend, request.user.username)
    return HttpResponse()

@login_required
def del_friend(request, friend):
    request.services.user.del_friend(request.user.id, friend)
    return HttpResponse()

@login_required
def del_critic(request, item):
    id = request.GET["id"]
    request.services.user.del_critic(request.user.id, id)
    msg = _("Critic deleted successfully")
    return HttpResponse(msg)

@login_required
def add_critic(request, item):
    comment = request.POST["comment"]
    if comment is not None and len(comment) > settings.CRITIC_MIN_LENGHT:
        request.services.user.add_critic(request.user.id, item, comment)
        msg = _("Critic added succesfully")
    else:
        msg = _("Critic too short. Please, write a little more about this")
    return HttpResponse(msg)

@login_required
def add_moderation(request, item):
    if request.user.is_staff:
        priority = request.POST["priority"]
        delete = request.POST["deleted"]
        released = request.POST["released"]
        request.services.user.moderate(request.user.id, item, priority, delete, released)
        return HttpResponseRedirect('/movies/admin/')
    else:
        msg = _("User is not staff")
        return HttpResponse(msg)


@login_required
def add_language(request, item):
    if request.user.is_staff:
        language = request.POST["language"]
        title = request.POST["title"]
        overview = request.POST["overview"]
        request.services.user.add_language(request.user.id, item, language, title, overview)
        return HttpResponseRedirect('/movies/admin/')
    else:
        msg = _("User is not staff")
        return HttpResponse(msg)

def get_dyn_js_language(request):
    #renderjs = render_to_string('dynjs/language.html', {})
    #return HttpResponse(renderjs, mimetype="text/plain")
    viewmap = {}
    if request.user.id:
        preferences = request.services.user.get_user_settings(request.user.id)
        viewmap['preferences'] = preferences
    return render_to_response('dynjs/language.html', viewmap, context_instance=RequestContext(request), mimetype="text/javascript")

def about(request):
    return render_to_response('about.html', {}, context_instance=RequestContext(request))

def contact(request):
    if request.method == 'POST': 
        contact = {'name':request.POST['name'], 'mail':request.POST['mail'], 'type':request.POST['type'], 'query': request.POST['query']}
        try:
            request.services.user.send_contact(contact)
            data = {'result':'ok'}
        except Exception as exc:
            data = {'result':'ko', 'msg':str(exc)}

        return HttpResponse(simplejson.dumps(data), mimetype='application/json')
    else: 
        return render_to_response('contact.html', {}, context_instance=RequestContext(request))

