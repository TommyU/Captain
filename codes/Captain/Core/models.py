from django.db import models
from django.contrib.auth.models impor User
from mptt.models import MPTTModel,TreeForeignKey

# base classes for most of the classes
class BaseModel(models.Model):
    """base class for class which need to be under CRUD control"""
    created_date = models.DateTimeField(auto_add=True)
    creator = models.ForeignKey(User)
    updated_date = models.DateTimeField(auto_now=True)
    updator = models.ForeignKey(User)

    class Meta:
        abstract=True

    def save(self, user, force_insert=False, force_update=False, using=None,update_fields=None):
	#TODO:do some validation here
        super(ModelBase,self).save(self, force_insert, force_update, using,update_fields)

    def delete(self, user, using=None):
        #TODO:do some validation here
        super(ModelBase,self).delete(using)

    #TODO:query validation 

class TreeModelBase(MPTTModel,BaseModel):
    """base class for all tree style class"""
    name = models.CharField(max_length=64, unique=True)
    parent= TreeForeignKey('self', null=True, blank=True, related_name='children')
    
    class MPTTMeta:
        order_insertion_by=['name']
        abstract=True

#base class for exceptions
class AccessDenied(Exception):
    """base class for Exception of access"""
    pass

    
