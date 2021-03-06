from django.http import HttpResponse
from django.shortcuts import render
import mysql.connector
import datetime

from django.http import HttpResponseRedirect
from .form import dateForm
from .form import bookingForm
def index(request,mem_num):
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='ktcsdb')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cars")
    all_cars = cursor.fetchall()

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = dateForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as

            data = form.cleaned_data
            cursor.execute("SELECT * FROM cars WHERE vin NOT IN (SELECT DISTINCT vin FROM reservation WHERE startDate <='"+ str(data["start_date"]) + "' AND endDate >='"+ str(data["start_date"])+"')")
            all_cars = cursor.fetchall()
            form = dateForm()
            cursor.execute("SELECT name, memNum FROM members WHERE memNum =" + str(mem_num))
            name = cursor.fetchall()
            context={
                "all_cars" : all_cars,
                "form" : form,
                "name" : name
            }
            return render(request, 'cars/index.html', context)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = dateForm()

    cursor.execute("SELECT name, memNum FROM members WHERE memNum =" + str(mem_num))
    name = cursor.fetchall()
    context = {
        "form" : form,
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
            overlap = 0
            conflict = ""
            for reservation in current_reservations:
                if start_date <= reservation[5] and end_date >= reservation[3]:
                    overlap = 1
                    conflict = "Error!"

            if len(current_reservations)==0 or overlap == 0:
                conflict = "Success!"
                cursor.execute("INSERT INTO reservation(vin, memNum, startDate, accessCode, endDate) "+
                                "VALUES ("+ car_id + "," + mem_num+",'" + str(start_date) + "',321,'" + str(end_date) + "')")
                conn.commit()
                cursor.execute("SELECT odometer, carStatus FROM cars WHERE vin="+ car_id)
                carInfo = cursor.fetchall()
                cursor.execute("SELECT reservationNum FROM reservation WHERE vin='"+car_id+"'AND memNum= '"+ mem_num+ "'AND startDate ="+ str(start_date))
                resNum = cursor.fetchall()
                cursor.execute("INSERT INTO rentalhistory(vin, memNum, pickupDate, pickupOdometer, pickupStatus,dropOffDate,dropOffOdometer,dropOffStatus)"+
                               "VALUES ("+ car_id + "," + mem_num + ",'" + str(start_date) + "','"+ str(carInfo[0][0]) + "','"+ str(carInfo[0][1]) + "','NULL','NULL','NULL'" +")")
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