from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect

import mysql.connector
from .form import loginForm

def get_login(request):
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='ktcsdb')
    cursor = conn.cursor()
    cursor.execute("SELECT name, password, memNum FROM members")
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
                    return HttpResponseRedirect('/cars/'+str(memNum))



    # if a GET (or any other method) we'll create a blank form
    else:
        form = loginForm()

    return render(request, 'login/index.html', {'form': form})
