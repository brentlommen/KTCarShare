from django.http import HttpResponse
from django.shortcuts import render
import mysql.connector
import datetime

from django.http import HttpResponseRedirect

from .form import bookingForm
def index(request,mem_num):
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='ktcsdb')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cars")
    all_cars = cursor.fetchall()

    cursor.execute("SELECT name, memNum FROM members WHERE memNum =" + str(mem_num))
    name = cursor.fetchall()
    context = {
        "all_cars" : all_cars,
        "name" : name
    }
    conn.close()
    cursor.close()
    return render(request, 'cars/index.html', context)

def details(request, mem_num, car_id):
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='ktcsdb')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM cars WHERE vin = "+str(car_id))
    car = cursor.fetchall()

    cursor.execute("SELECT * FROM parkinglocations WHERE " + str(car[0][7]) + "= locationNumber")
    location = cursor.fetchall()

    cursor.execute("SELECT * FROM comments WHERE vin =" + str(car[0][0]))
    comment = cursor.fetchall()

    cursor.execute("SELECT name, memNum FROM members WHERE memNum =" + str(mem_num))
    member = cursor.fetchall()

    cursor.execute("SELECT startDate, endDate FROM reservation WHERE vin = "+ str(car_id))
    the_reservations = cursor.fetchall()



    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = bookingForm(request.POST)
        # check whether it's valid:

        if form.is_valid():
            # process the data in form.cleaned_data as required
            data = form.cleaned_data
            start_date = data["start_date"]
            end_date = data["end_date"]

            cursor.execute("SELECT * FROM reservation WHERE vin ="+ car_id)
            current_reservations = cursor.fetchall()
            # inserts reservation if there is no conflict with current reservations
            print "overlapped"
            overlap = 0
            conflict = ""
            for reservation in current_reservations:
                print type(reservation[5])
                if start_date <= reservation[5] and end_date >= reservation[3]:
                    overlap = 1
                    conflict = "Error!"

            if len(current_reservations)==0 or overlap == 0:
                print"here"
                conflict = "Success!"
                cursor.execute("INSERT INTO reservation(vin, memNum, startDate, accessCode, endDate) "+
                                "VALUES ("+ car_id + "," + mem_num+",'" + str(start_date) + "',321,'" + str(end_date) + "')")
            # end of reservation insertion

            # fetch reservations to get updated list
            cursor.execute("SELECT startDate, endDate FROM reservation WHERE vin = " + str(car_id))
            the_reservations = cursor.fetchall()

            conn.commit()
            cursor.close()
            form = bookingForm()
            context = {
                "member": member,
                "the_car": car,
                "the_location": location,
                "the_comment": comment,
                "the_reservations": the_reservations,
                "conflict" : conflict,
                "form": form
            }


            return (render(request, 'cars/details.html', context))



    # if a GET (or any other method) we'll create a blank form
    else:
        form = bookingForm()

    context = {
        "member" : member,
        "the_car" : car,
        "the_location" : location,
        "the_comment" : comment,
        "the_reservations": the_reservations,
        "form" :form
    }
    return(render(request, 'cars/details.html', context))

def booking(request, mem_num, car_id):

    return(render(request, 'cars/bookings.html', {}))