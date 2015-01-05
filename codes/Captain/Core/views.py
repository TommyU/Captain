from django.shortcuts import render,render_to_response

# Create your views here.

def bs_demo(req):
	return render_to_response('bootstrap.all.html',{})