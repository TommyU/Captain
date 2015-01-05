from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^bsd/$', 'Core.views.bs_demo'),
)