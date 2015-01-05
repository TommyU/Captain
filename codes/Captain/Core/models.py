from django.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel,TreeForeignKey

# base classes for most of the classes
class BaseModel(models.Model):
    """base class for class which need to be under CRUD control"""
    created_date = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, related_name='creator_%(class)s_set')
    updated_date = models.DateTimeField(auto_now=True)
    updator = models.ForeignKey(User, related_name='updator_%(class)s_set')

    class Meta:
        abstract=True

    def save(self, user, force_insert=False, force_update=False, using=None,update_fields=None):
	#TODO:do some validation here
        super(BaseModel,self).save(force_insert, force_update, using,update_fields)

    def delete(self, user, using=None):
        #TODO:do some validation here
        super(BaseModel,self).delete(using)

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
