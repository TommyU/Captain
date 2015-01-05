from django.contrib import admin
from .models import Page,Tag,ContentType,Menu
from django.core.exceptions import *

class AdminBase(admin.ModelAdmin):
	def save_model(self, request, obj, form, change):
		#user = User
		obj.save(request.user.id) 

	def delete_model(self, request, obj):
		"""
		Given a model instance delete it from the database.
		"""
		obj.delete(request.user.id)

	def get_search_results(self, request, queryset, search_term):
		user = request.user
		if user.has_perm('can_read_%s'%self.__class__.__name__.lower()):
			queryset, use_distinct = super(AdminBase, self).get_search_results(request, queryset,search_term)
			return queryset, use_distinct
		else:
			raise PermissionDenied

# Register your models here.
class PageAdmin(AdminBase):
	list_display =('title','author','created_date','state')

admin.site.register(Page, PageAdmin)

class TagAdmin(AdminBase):
	list_display =('name','parent','created_date','creator')

admin.site.register(Tag, TagAdmin)

class ContentTypeAdmin(AdminBase):
	list_display =('name','parent','created_date','creator')

admin.site.register(ContentType, ContentTypeAdmin)

class MenuAdmin(AdminBase):
	list_display =('name','parent','created_date','creator')

admin.site.register(Menu, MenuAdmin)
