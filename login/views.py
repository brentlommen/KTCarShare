from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect

import mysql.connector
from .form import loginForm
from .form import signupForm

def get_login(request):
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='ktcsdb')
    cursor = conn.cursor()
    cursor.execute("SELECT name, password, memNum,admin FROM members")
    all_members = cursor.fetchall()
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = loginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            data = form.cleaned_data
            for member in all_members:
                if member[0] == data["username"] and str(member[1]) == data["password"]:
                    memNum = member[2]
                    if member[3] == 1:
                        return HttpResponseRedirect('/admin_user/')
                    else:
                        return HttpResponseRedirect('/cars/'+str(memNum))




    # if a GET (or any other method) we'll create a blank form
    else:
        form = loginForm()

    return render(request, 'login/index.html', {'form': form})

def signUp(request):
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='ktcsdb')
    cursor = conn.cursor()
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = signupForm(request.POST)
        # check whether it's valid:
        print form.is_valid()
        if form.is_valid():
            # process the data in form.cleaned_data as required
            data = form.cleaned_data
            cursor.execute("INSERT INTO members( name, address, phoneNumber,email, licience, password) "+
                                "VALUES ('"+ data["name"] + "','" + data["address"]+"','" + data["phoneNumber"] + "','" + data["email"] +"','" + data["licence"] + "','" + data["password"]+ "')")
            conn.commit()
            form = loginForm()
            return HttpResponseRedirect('/login/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = signupForm()
    return render(request, 'login/signup.html',{'form': form})