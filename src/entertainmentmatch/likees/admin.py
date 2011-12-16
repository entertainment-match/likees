from django.contrib import admin
from django import forms
from entertainmentmatch.likees.models import Notification, Movie, Person, Category, Item_Job_Cast_Person, Tag, Critic, UserLikees, Image, Tag_Items, Item

def overview_es_isnull(obj):
    if obj.overview_es is None or obj.overview_es == '':
        return True
    else:
        return False

class NotificationAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.save()

class TagItemsInline(admin.TabularInline):
    model = Tag_Items
    raw_id_fields = ('item',) 
    extra = 1

class MovieAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating', overview_es_isnull)
    list_filter = ('deleted', 'priority')
    fields = ('original_name', 'name_en', 'name_es', 'name_fr', 'overview_en', 'overview_es', 'overview_fr', 'id_imdb', 'id_tmdb')
    search_fields = ['name_en', 'name_es']

    def save_model(self, request, obj, form, change):
        obj.save()

class TagAdmin(admin.ModelAdmin):
    inlines = (TagItemsInline,)
    list_display = ('name', 'user')
    list_filter = ('type',)
    ordering = ('id',)

class ItemAdmin(admin.ModelAdmin):
    search_fields = ['name_es', 'name_en']

admin.site.register(Notification, NotificationAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Item, ItemAdmin)
