from django.db import models
from django.contrib.auth.models import User, UserManager
from transmeta import TransMeta
import re

class UserLikees(User):
    gender = models.CharField(max_length=10, null=True)
    birthdate = models.DateField(null=True)
    timezone = models.CharField(max_length=255, null=True, default='Europe/Madrid')
    friends = models.ManyToManyField('UserLikees', related_name='user_friend', null=True)
    image = models.ForeignKey('Image', null=True)
    itemsVoted = models.ManyToManyField('Item', through='Vote', related_name='item_vote', null=True)
    itemsCritiqued = models.ManyToManyField('Item', through='Critic', related_name='item_critic', null=True)
    
    objects = UserManager()

class Item(models.Model):
    __metaclass__ = TransMeta
    
    id = models.AutoField(primary_key=True)
    released = models.DateField(null=True, db_index=True)
    buy_links = models.CharField(max_length=100, null=True)
    rating = models.FloatField(null=True, db_index=True)
    homepage = models.CharField(max_length=150, null=True)
    votes_count = models.IntegerField(null=True)
    version = models.IntegerField(null=True)
    name = models.CharField(max_length=100, null=True, db_index=True)
    original_name = models.CharField(max_length=100, db_index=True)
    alternative_name = models.CharField(max_length=100, null=True, db_index=True)
    overview = models.TextField(null=True)
    review = models.TextField(null=True)
    parent_item = models.IntegerField(null=True)
    tagline = models.TextField(null=True)
    type = models.CharField(max_length=50, null=True)
    categories = models.ManyToManyField('Category', related_name='item_category')
    image = models.ForeignKey('Image', related_name='image_%(app_label)s_%(class)s_related', null=True)
    thumb = models.ForeignKey('Image', related_name='thumb_%(app_label)s_%(class)s_related', null=True)
    produced = models.ManyToManyField('Country')
    companies = models.ManyToManyField('Company', through = 'Role', related_name='item_company', null=True)
    deleted = models.IntegerField(db_index=True, default=0)
    priority = models.IntegerField(db_index=True, default=2)

    class Admin:
        pass

    class Meta:
        abstract = False
        translate = ('name', 'overview', 'tagline')

    def __unicode__(self):
        return self.name
    
    def normalized_name(self):
        return re.sub(r"[^a-zA-Z0-9]", "_", self.name)

"Item inheritance"
class Movie(Item):
    runtime = models.IntegerField(null=True)
    trailer = models.CharField(max_length=200, null=True)
    id_imdb = models.CharField(max_length=10, null=True)
    id_tmdb = models.IntegerField(null=True, db_index=True)

class Company(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, db_index=True)

    def __unicode__(self):
        return self.name

class Role(models.Model):
    __metaclass__ = TransMeta
    
    item = models.ForeignKey('Item')
    company = models.ForeignKey('Company')
    name = models.CharField(max_length=100, null=True)
    
    class Meta:
        translate = ('name',)
    
    def __unicode__(self):
        return self.name

class Vote(models.Model):
    user = models.ForeignKey(UserLikees)
    item = models.ForeignKey(Item)
    rate = models.IntegerField()
    date = models.DateTimeField()

class Critic(models.Model):
    user = models.ForeignKey(UserLikees)
    item = models.ForeignKey(Item)
    text = models.TextField()
    date = models.DateTimeField()

class Job(models.Model):
    __metaclass__ = TransMeta
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, db_index=True)
    
    class Meta:
        translate = ('name',)
        
    def __unicode__(self):
        return self.name

class Person(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, db_index=True)
    tmdb_id = models.IntegerField(null=True)
    image = models.ForeignKey('Image', related_name="image_person", null=True)
    item = models.ManyToManyField('Item', through='Item_Job_Cast_Person', related_name='item_person', null=True)
    
    def __unicode__(self):
        return self.name
    
    def normalized_name(self):
        return re.sub(r"[^a-zA-Z0-9]", "_", self.name)

class Item_Job_Cast_Person(models.Model):
    person = models.ForeignKey('Person')
    item = models.ForeignKey('Item')
    job = models.ForeignKey('Job')
    
    def __unicode__(self):
        return "%s, %s, %s" % (self.person.name, self.item.name, self.job.name)

class Category(models.Model):
    __metaclass__ = TransMeta
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, db_index=True)
    parent_category = models.ForeignKey('self', null=True)
    
    class Meta:
        translate = ('name',)

    def __unicode__(self):
        return self.name

class Tag(models.Model):
    __metaclass__ = TransMeta

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, null=True, blank=True)
    type = models.CharField(max_length=50)
    user = models.ForeignKey(UserLikees, null=True, blank=True)
    items = models.ManyToManyField('Item', related_name='items', through='Tag_Items')
    parent_tag = models.ForeignKey('self', null=True, blank=True)
    date_create = models.DateTimeField(auto_now_add=True)

    class Meta:
        translate = ('description',)

    def __unicode__(self):
        return self.name

class Tag_Items(models.Model):
    tag = models.ForeignKey(Tag)
    item = models.ForeignKey(Item)
    date_ini = models.DateField(null=True, blank=True)
    date_end = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = (('tag','item'),)

class Image(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=200)
    date = models.DateTimeField()

    def __unicode__(self):
        return self.url

class Country(models.Model):
    id = models.CharField(primary_key=True, max_length=2)
    name = models.CharField(max_length=100)
    flag_url = models.CharField(max_length=100, null=True)

class Event(models.Model):
    id = models.AutoField(primary_key=True)
    from_user = models.ForeignKey(UserLikees)
    item = models.ForeignKey(Item, null=True)
    action = models.CharField(max_length=250)
    value = models.CharField(max_length=250)
    when = models.DateTimeField()

class Notification(models.Model):
    __metaclass__ = TransMeta
    id = models.AutoField(primary_key=True)
    text = models.TextField(null=True)
    date_on = models.DateTimeField()
    date_off = models.DateTimeField()

    class Meta:
        abstract = False
        translate = ('text',)

    class Admin:
        pass

class User_Settings(models.Model):
    user = models.ForeignKey(UserLikees)
    key = models.CharField(max_length=50)
    value = models.CharField(max_length=50)

class Soulmates_Coef(models.Model):
    user1 = models.ForeignKey(UserLikees, related_name='user1')
    user2 = models.ForeignKey(UserLikees, related_name='user2')
    coef = models.IntegerField(null=True)

#class Book(Item):
#    isbn = models.CharField(max_length=15)
#

#class Comic(Item):
#    isbn = models.CharField(max_length=15)
#

#class Series(Item):
#    runtime = models.IntegerField()
#    trailer = models.CharField(max_length=200)

#class ReleaseDate(models.Model):
#    date = models.DateField()
#    release_on = models.CharField(max_length=10)

#class Item_ReleaseDate_Country(models.Model):
#    item = models.ForeignKey('Item')
#    releaseDate = models.ForeignKey('ReleaseDate')
#    country = models.ForeignKey('Country')

#class Cast(models.Model):
#    id = models.AutoField(primary_key=True)
#    character_default_m = models.CharField(max_length=100)
#    
#    def __unicode__(self):
#        return self.character_default_m

#class Message(models.Model):
#    id = models.AutoField(primary_key=True)
#    body = models.CharField(max_length=250)
#    date = models.DateField()
#    is_read = models.BooleanField()
##    to_user = models.ForeignKey(User, related_name='to_user')
##    parent_message = models.ManyToManyField('self', symmetrical=False)
##    from_user = models.ForeignKey('User', related_name='from_user')
##    item = models.ForeignKey('Item')
