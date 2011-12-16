from django.conf import settings
from django.contrib import admin
from django.views.generic.simple import direct_to_template
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^entertainmentmatch/', include('entertainmentmatch.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    #(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.STATIC_DOC_ROOT}),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_DOC_ROOT, 'show_indexes': True}),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    # Likees urls
    (r'^robots\.txt$', direct_to_template, {'template': 'robots/' + settings.LIKEES_ENVIROMENT + '.txt'}),
    #(r'^sitemap\.xml$', direct_to_template, {'template': 'sitemap/sitemap.xml'}),

    (r'^home/$', 'likees.views.home.index'),
    (r'^tutorial/$', 'likees.views.tutorial.index'),
    (r'^tutorial/tour/$', 'likees.views.tutorial.tour'),
    (r'^$', 'likees.views.home.index'),

    # Dashboard
    (r'^dashboard/$', 'likees.views.dashboard.index'),
    (r'^dashboard/friends/$', 'likees.views.dashboard.friends'),
    (r'^dashboard/soulmates/$', 'likees.views.dashboard.soulmates'),
    (r'^dashboard/lists/$', 'likees.views.dashboard.lists'),
    (r'^events/$', 'likees.views.dashboard.events'),
    
    # Catalog
    (r'^movies/', 'likees.views.catalog.index'),
    (r'^movies/admin/', 'likees.views.admin_items.admin'),
    (r'^votes/$', 'likees.views.catalog.get_voted'),
    (r'^ignored/$', 'likees.views.catalog.get_ignored'),
    (r'^favourites/$', 'likees.views.catalog.get_favourites'),
    (r'^recommendations/', 'likees.views.catalog.get_recommendations'),
    (r'^wishlist/', 'likees.views.catalog.get_wishlist'),
    (r'^new/', 'likees.views.catalog.get_estrenos'),
    (r'^search/', 'likees.views.catalog.search'),
    (r'^item/(?P<item>\d+)/$', 'likees.views.catalog.view_movie'),
    (r'^item/(?P<item>\d+)/trailer/$', 'likees.views.catalog.view_trailer'),
    (r'^item/(?P<item>\d+)/title/.*/$', 'likees.views.catalog.view_movie'),
    
    (r'^item/(?P<item>\d+)/rate/$', 'likees.views.views.rate_detail'),
    (r'^item/(?P<item>\d+)/vote/$', 'likees.views.views.vote_movie'),
    (r'^item/(?P<item>\d+)/fave/add/$', 'likees.views.views.add_item_fave'),
    (r'^item/(?P<item>\d+)/fave/delete/$', 'likees.views.views.del_item_fave'),
    (r'^item/(?P<item>\d+)/wishlist/add/$', 'likees.views.views.add_item_wishlist'),
    (r'^item/(?P<item>\d+)/wishlist/delete/$', 'likees.views.views.del_item_wishlist'),
    (r'^item/(?P<item>\d+)/ignore/add/$', 'likees.views.views.add_item_ignore'),
    (r'^item/(?P<item>\d+)/ignore/delete/$', 'likees.views.views.del_item_ignore'),
    (r'^item/(?P<item>\d+)/tag/add/$', 'likees.views.views.add_item_list'),
    (r'^item/(?P<item>\d+)/tag/delete/$', 'likees.views.views.del_item_list'),
    (r'^item/(?P<item>\d+)/critic/add/$', 'likees.views.views.add_critic'),
    (r'^item/(?P<item>\d+)/language/add/$', 'likees.views.views.add_language'),
    (r'^item/(?P<item>\d+)/moderate/add/$', 'likees.views.views.add_moderation'),
    (r'^item/(?P<item>\d+)/critic/delete/$', 'likees.views.views.del_critic'),

    (r'^user/search/$', 'likees.views.dashboard.search_user'),
    (r'^user/(?P<username>[\-\.\w]+)/$', 'likees.views.views.view_user'),
    (r'^user/(?P<username>[\-\.\w]+)/infotip/$', 'likees.views.views.view_user_infotip'),
    (r'^friend/add/(?P<friend>[\-\.\w]+)/$', 'likees.views.views.add_friend'),
    (r'^friend/delete/(?P<friend>[\-\.\w]+)/$', 'likees.views.views.del_friend'),
    #(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'users/login.html'}),
    (r'^accounts/login/$', 'likees.views.views.login_user'),
    (r'^accounts/logout/', 'django.contrib.auth.views.logout_then_login'), 
    (r'^accounts/register/$', 'likees.views.views.create_user'),
    (r'^accounts/validate/', 'likees.views.views.view_validate'),
    (r'^accounts/change_password/', 'likees.views.views.change_password'),
    #(r'^accounts/loadgravatar/', 'likees.views.views.load_gravatar'),
    (r'^accounts/reset/', 'likees.views.views.reset_password'),
    (r'^accounts/remember/', 'likees.views.views.remember_password'),
    (r'^accounts/profile/$', 'likees.views.dashboard.view_profile'),
    (r'^accounts/profile/avatar/', 'likees.views.views.set_avatar'),
    (r'^accounts/update_profile/', 'likees.views.dashboard.update_profile'),
    (r'^accounts/mailregister/', 'likees.views.views.view_mail_register'),
    (r'^accounts/mailrememberpassword/', 'likees.views.views.view_mail_remember'),
    (r'^accounts/add_facebook_id/$', 'likees.views.dashboard.add_facebook_id'),
    (r'^accounts/del_facebook_id/$', 'likees.views.dashboard.del_facebook_id'),
    (r'^category/(?P<category_id>\d+)/$', 'likees.views.views.find_items_by_category'),
    (r'^person/(?P<person>\d+)/', 'likees.views.views.find_items_by_person'),
    (r'^person/(?P<person>\d+)/title/.*/$', 'likees.views.views.find_items_by_person'),
    (r'^tag/add/(?P<item>\d+)/$', 'likees.views.views.add_item_list'),
    (r'^tag/delete/(?P<item>\d+)/$', 'likees.views.views.del_item_list'),
    (r'^tag/list', 'likees.views.views.get_user_lists'),
    (r'^dynjs/language.js$','likees.views.views.get_dyn_js_language'),
    (r'^contact/', 'likees.views.views.contact'),
    (r'^about/', 'likees.views.views.about'),
    # socialauth
    #(r'^accounts/', include('socialauth.urls')),
    #(r'^$', 'socialauth.views.signin_complete'),

)

if 'entertainmentmatch.rosetta' in settings.INSTALLED_APPS:
        urlpatterns += patterns('', (r'^rosetta/', include('entertainmentmatch.rosetta.urls')),)
