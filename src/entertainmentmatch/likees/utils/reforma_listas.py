'''
Created on 06/02/2011

@author: dysphoria
'''
from entertainmentmatch.likees.models import Tag, UserLikees, Item_Tag_User, Tag_Items
from django.db import transaction


@transaction.commit_on_success
def main():
    tag_fave = Tag.objects.select_related().get(id=1)
    tag_wishlist = Tag.objects.select_related().get(id=3)
    tag_ignore = Tag.objects.select_related().get(id=4)

    users = UserLikees.objects.all()

    for user in users:
        tag_user_fave = Tag(name = tag_fave.name, type = tag_fave.type, user = user)
        tag_user_fave.save()

        tag_user_wishlist = Tag(name = tag_wishlist.name, type = tag_wishlist.type, user = user)
        tag_user_wishlist.save()

        tag_user_ignore = Tag(name = tag_ignore.name, type = tag_ignore.type, user = user)
        tag_user_ignore.save()


        tags_old_faves = Item_Tag_User.objects.filter(tag=tag_fave.id, user=user.id)

        print "usuario: " + str(user.id)

        for tag in tags_old_faves:
            print "tag: " + str(tag_user_fave.id) + " item: " + str(tag.item.id)
            tag_items = Tag_Items(tag=tag_user_fave, item=tag.item)
            tag_items.save()



        tags_old_wishlist = Item_Tag_User.objects.filter(tag=tag_wishlist.id, user=user.id)

        for tag in tags_old_wishlist:
            print "tag: " + str(tag_user_wishlist.id) + " item: " + str(tag.item.id)
            tag_items = Tag_Items(tag=tag_user_wishlist, item=tag.item)
            tag_items.save()



        tags_old_ignore = Item_Tag_User.objects.filter(tag=tag_ignore.id, user=user.id)

        for tag in tags_old_ignore:
            print "tag: " + str(tag_user_ignore.id) + " item: " + str(tag.item.id)
            tag_items = Tag_Items(tag=tag_user_ignore, item=tag.item)
            tag_items.save()
