from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import mysql.connector
from .form import dropOffForm
def index(request, mem_num):
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='ktcsdb')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM members WHERE memNum = " + mem_num)
    member = cursor.fetchall()
    cursor.execute("SELECT make, model, dailyRentalFee, startDate, endDate, Address, picture, reservationNum FROM (reservation NATURAL JOIN cars) NATURAL JOIN parkinglocations WHERE memNum = " + mem_num)
    reservations = cursor.fetchall()

    context = {
        "member" : member,
        "reservations" : reservations
    }


    return (render(request , 'my_profile/index.html', context))

def dropOff(request, res_num):
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='ktcsdb')
    cursor = conn.cursor()
    cursor.execute("SELECT make, model FROM cars")
    reservation = cursor.fetchall()
    form = dropOffForm()
    context= {
        'res_num' : res_num,
        'make' : reservation[0],
        'model' : reservation[1],
        'form' : form
    }
    return render(request, 'my_profile/dropOffForm.html', context)
