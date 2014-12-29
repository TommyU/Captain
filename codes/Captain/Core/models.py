from django.db import models
from django.contrib.auth.models impor User

# Create your models here.
class ModelBase(models.Model):
    created_date = models.DateTimeField(auto_add=True)
    creator = models.ForeignKey(User)
    updated_date = models.DateTimeField(auto_now=True)
    updator = models.ForeignKey(User)

    class Meta:
        abstract=True

    def save(self, uid, ids, force_insert=False, force_update=False, using=None,update_fields=None):
	#TODO:do some validation here
        super(ModelBase,self).save(self, force_insert, force_update, using,update_fields)
