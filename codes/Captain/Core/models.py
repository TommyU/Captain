from django.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel,TreeForeignKey
import logging
from django.core.exceptions import *
_logger = logging.getLogger(__name__)

class Pool(object):
    classes = {}
    @classmethod 
    def register(self,res_model , res_class):
        self.classes.update({res_model:res_class})
    
    @classmethod 
    def get(self,res_model):
        self.classes.get(res_model,None)


class BaseModelManager(models.Manager):
    def get_queryset(self):
        return super(BaseModelManager,self).get_queryset()

    def filter(self,uid,*args,**kwargs):
        user_obj = User.objects.get(id=uid)
        method='read'
        if user_obj and user_obj.has_perm('can_%s_%s'%(method,self.__class__.__name__.lower())):
            return super(BaseModelManager, self).filter(*args,**kwargs)
        else:
            raise PermissionDenied

    def get(self,uid,*args,**kwargs):
        user_obj = User.objects.get(id=uid)
        method='read'
        if user_obj and user_obj.has_perm('can_%s_%s'%(method,self.__class__.__name__.lower())):
            return super(BaseModelManager, self).get(*args,**kwargs)
        else:
            raise PermissionDenied

# base classes for most of the classes
class BaseModel(models.Model):
    """base class for class which need to be under CRUD control"""
    created_date = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, related_name='creator_%(class)s_set')
    updated_date = models.DateTimeField(auto_now=True)
    updator = models.ForeignKey(User, related_name='updator_%(class)s_set')
    objects = BaseModelManager()#TODO:query validation 

    def __init__(self, *args, **kwargs):
        Pool.register(('%s.%s'%(self.__module__,self.__class__.__name__)), self.__class__)
        _logger.debug('%s registered'%('%s.%s'%(self.__module__,self.__class__.__name__),))
        models.Model.__init__(self, *args, **kwargs)

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
        """do some validation before delete"""
        user_obj = User.objects.get(id=uid)
        method='delete'
        if user_obj and user_obj.has_perm('can_%s_%s'%(method,self.__class__.__name__.lower())):
            super(BaseModel,self).delete(using)
        else:
            raise PermissionDenied

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
Tag()#register the Tag class

class ContentType(TreeModelBase):
    pass
ContentType()#register the ContentType class

class Menu(TreeModelBase):
    order = models.IntegerField()
    state=models.CharField(max_length=32, choices=[('draft','draft'),('confirmed','confirmed'),('cancel','cancel')])
    url=models.URLField(blank=True)
    res_model = models.CharField(max_length=256, blank=True)

    def get_data(self):
        mod = Pool.classes.get(self.res_model,None)
        #print 'res model:%s, pool clses:%s, mod is none:%s'%(self.res_model,Pool.classes,(not mod))
        if mod:
            return mod.objects.all()
Menu()#register the Menu class

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
Page()#register the Page class
