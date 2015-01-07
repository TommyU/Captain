from django.shortcuts import render,render_to_response
from Core.models import Menu,Page
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import UserSerializer, GroupSerializer
# Create your views here.

def bs_demo(req):
    return render_to_response('bootstrap.all.html',{})

def menu_test(req):
    pages = Menu.objects.all()[0].get_data()
    return render_to_response('menu_test.html',{'res':pages})

def rest_test(req):
	return render_to_response('rest_test.html',{})

def bb_test(req):
	return render_to_response('backbone_test.html',{})

class UserViewSet(viewsets.ModelViewSet):
	"""
	api endpoint that allows users to be viewed or edited
	"""
	queryset = User.objects.all()
	serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
	queryset = Group.objects.all()
	serializer_class = GroupSerializer