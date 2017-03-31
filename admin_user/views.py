from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect

import mysql.connector
from .form import addCarForm
from .form import reservationForm
from .form import invoiceForm
# Create your views here.

def adminCars(request):
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='ktcsdb')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cars")
    all_cars = cursor.fetchall()
    context = {
        "all_cars": all_cars,
    }
    conn.close()
    cursor.close()
    return render(request,'admin_user/index.html',context)

def adminMembers(request):
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='ktcsdb')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM members WHERE admin = 0")
    all_members = cursor.fetchall()
    context = {
        'all_members' : all_members
    }
    return render(request, 'admin_user/members.html',context)

def statement(request, mem_num):
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='ktcsdb')
    cursor = conn.cursor()
    cursor.execute("SELECT rentalhistory.vin, make, model, pickupDate, dropOffDate, reservationNum, dailyRentalFee FROM rentalhistory NATURAL JOIN cars WHERE memNum= " + mem_num)
    all_transactions = cursor.fetchall()
    context = {
        'all_transactions' : all_transactions
    }
    return render(request, 'admin_user/statement.html', context)

def rentalHistory(request, car_num):
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='ktcsdb')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM rentalhistory WHERE vin = "+ car_num)
    car_history = cursor.fetchall()
    context = {
        'car_history' : car_history
    }
    return render(request, 'admin_user/rentalHistory.html', context)

def addCar(request):
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='ktcsdb')
    cursor = conn.cursor()
    form = addCarForm()
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = addCarForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as
            data = form.cleaned_data
            cursor.execute("INSERT INTO cars VALUES ('"+str(data["vin"])+"','"+ data["make"]+"','"+ data["model"]+"','"+ str(data["year"])+ "','"+ str(data["dailyRentalFee"])+ "','normal',1,'"+ str(data["locationNumber"])+"','"+ data["picture"]+"','"+ str(data["odometer"])+"')")
            conn.commit()
            return HttpResponseRedirect('/admin_user/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = addCarForm()

    context = {
        'form' : form
    }
    return render(request, 'admin_user/addCar.html', context)

def reservations(request):
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='ktcsdb')
    cursor = conn.cursor()
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = reservationForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as
            data = form.cleaned_data
            date = data["date"]
            cursor.execute("SELECT * FROM reservation WHERE startDate <='" + str(data["date"]) + "'AND endDate >='"+ str(data["date"])+"'")
            all_reservations = cursor.fetchall()
            context = {
                'date' : date,
                'form' : form,
                'all_reservations' : all_reservations
            }
            return render(request, 'admin_user/reservations.html', context)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = reservationForm()
    context = {
        'form' : form
    }
    return render(request, 'admin_user/reservations.html', context)

def invoices(request):
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='ktcsdb')
    cursor = conn.cursor()
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = invoiceForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as
            data = form.cleaned_data
            cursor.execute("SELECT memNum, TotalRentalFee, MonthlyMembershipFee, (TotalRentalFee + MonthlyMembershipFee) as TotalMonthlyFee FROM (SELECT memNum, SUM(MonthlyRentalFee) as TotalRentalFee, (anualFee/12) as MonthlyMembershipFee FROM (SELECT memNum, vin, (days*dailyRentalFee) as MonthlyRentalFee FROM (SELECT memNum, vin, datediff(dropOffDate,pickUpDate) as days FROM rentalhistory WHERE dropOffDate >= '" + str(data["start_date"]) + "' and dropOffDate <='" + str(data["end_date"])+"' GROUP BY memNum, vin )as T1 NATURAL JOIN cars)as T2 NATURAL JOIN members GROUP BY memNum) as T3")
            all_invoices = cursor.fetchall()
            form = invoiceForm()
            context = {
                'form': form,
                'all_invoices': all_invoices
            }
            return render(request, 'admin_user/invoices.html', context)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = invoiceForm()
    context = {
        'form' : form
    }
    return render(request, 'admin_user/invoices.html', context)

def damaged(request):
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='ktcsdb')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cars WHERE carStatus = 'damaged' OR carStatus = 'not running'")
    all_damaged = cursor.fetchall()
    context = {
        'all_damaged' : all_damaged
    }
    return render(request, 'admin_user/damaged.html', context)

def sortByRentals(request):
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='ktcsdb')
    cursor = conn.cursor()
    cursor.execute("SELECT vin, make, model, year, COUNT(*) as numRents FROM rentalhistory NATURAL RIGHT OUTER JOIN cars GROUP BY vin ORDER BY numRents")
    all_cars = cursor.fetchall()
    context = {
        'all_cars' : all_cars
    }
    return render(request, 'admin_user/sortByRentals.html', context)

def searchByLocation(request):
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='ktcsdb')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM parkinglocations ")
    all_locations = cursor.fetchall()
    context = {
        'all_locations' : all_locations
    }
    return render(request, 'admin_user/searchByLocation.html', context)

def carsByLocation(request, location_num):
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='ktcsdb')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cars WHERE locationNumber = " + location_num)
    carsAtLocation = cursor.fetchall()
    cursor.execute("SELECT Address FROM parkinglocations WHERE locationNumber = "+ location_num)
    address = cursor.fetchall()
    context = {
        'address' : address,
        'carsAtLocation' : carsAtLocation
    }
    return render(request, 'admin_user/carsAtLocation.html', context)