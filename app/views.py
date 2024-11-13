from django.shortcuts import render
from django.http import HttpResponse,request
# Create your views here.

def login_successful(request):
    if request.user.is_authenticated:
        return HttpResponse(f"200 ok {request.user.username}")
    else:
        return HttpResponse(f"403 ")


