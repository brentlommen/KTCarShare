from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect

import mysql.connector

# Create your views here.

def admin(request):
    return render(request,'admin_user/index.html',{})