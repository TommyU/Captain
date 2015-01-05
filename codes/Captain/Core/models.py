from django.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel,TreeForeignKey
import logging
from django.core.exceptions import *

# base classes for most of the classes
class BaseModel(models.Model):
    """base class for class which need to be under CRUD control"""
    created_date = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, related_name='creator_%(class)s_set')
    updated_date = models.DateTimeField(auto_now=True)
    updator = models.ForeignKey(User, related_name='updator_%(class)s_set')

    class Meta:
        abstract=True

    def save(self, uid, force_insert=False, force_update=False, using=None,update_fields=None):
        """do some validation before save"""
        user_obj = User.objects.get(id=uid)
        if self.id:#update
            method = 'change'          
        else:#create
            method = 'add'
        if user_obj and user_obj.has_perm('can_%s_%s'%(method,self.__class__.__name__.lower())):
            super(BaseModel,self).save(force_insert, force_update, using,update_fields)
        else:
            raise PermissionDenied
        

    def delete(self, uid, using=None):
        user_obj = User.objects.get(id=uid)
        raise PermissionDenied
        method='delete'
        if user_obj and user_obj.has_perm('can_%s_%s'%(method,self.__class__.__name__.lower())):
            super(BaseModel,self).delete(using)
        else:
            raise PermissionDenied

    #TODO:query validation 


class TreeModelBase(MPTTModel,BaseModel):
    """base class for all tree style class"""
    name = models.CharField(max_length=64, unique=True)
    parent= TreeForeignKey('self', null=True, blank=True, related_name='children')
    
    class MPTTMeta:
        order_insertion_by=['name']

    class Meta:
        abstract=True

    def __unicode__(self):
        return self.name

#base class for exceptions
class AccessDenied(Exception):
    """base class for Exception of access"""
    pass


#concret classes below down
class Tag(TreeModelBase):
    pass

class ContentType(TreeModelBase):
    pass

class Menu(TreeModelBase):
    state=models.CharField(max_length=32, choices=[('draft','draft'),('confirmed','confirmed'),('cancel','cancel')])
    url=models.URLField()

class Page(BaseModel):
    title = models.CharField(max_length=256)
    content = models.TextField()
    author = models.ForeignKey(User, related_name='user_page_set')
    content_type = models.ForeignKey(ContentType, related_name='page_set')
    tags = models.ManyToManyField(Tag)
    state = models.CharField(max_length=32, choices=[('draft','draft'),('published','published'),('cancel','cancel')])
    publisher = models.ForeignKey(User, related_name='publisher_page_set',blank=True,null=True)  

    def __unicode__(self):
        return self.title
