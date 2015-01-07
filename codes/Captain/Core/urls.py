from django.conf.urls import patterns, include, url
from rest_framework import routers
from .views import UserViewSet, GroupViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('groups', GroupViewSet)

urlpatterns = patterns('',
    url(r'^bsd/$', 'Core.views.bs_demo'),#bootstrap demo
    url(r'^menu_test/$','Core.views.menu_test'),
    url(r'^rest_test/$','Core.views.rest_test'),
    url(r'^bb_test/$','Core.views.bb_test'),
    url(r'^api/', include(router.urls)),
    
)