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

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = dropOffForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            data = form.cleaned_data

            cursor.execute("UPDATE rentalHistory SET dropOffDate = '" + str(data["dropOffDate"]) + "', dropOffOdometer ='"+ str(data["dropOffOdometer"])+ "', dropOffStatus='"+ data["dropOffStatus"] +
                           "' WHERE rentalhistory.reservationNum ="+ res_num)
            conn.commit()
            cursor.execute("SELECT vin, memNum FROM rentalhistory WHERE reservationNum="+ res_num)
            theVin = cursor.fetchall()
            cursor.execute("UPDATE cars SET carStatus = '" + str(data["dropOffStatus"]) + "', odometer ='" + str(
                    data["dropOffOdometer"]) + "' WHERE cars.vin =" + str(theVin[0][0]))
            conn.commit()

            cursor.execute("DELETE FROM reservation WHERE reservation.reservationNum = "+ res_num)
            conn.commit()
            cursor.execute(("INSERT INTO comments(vin, memNum, date, rating, comment) "+
                                "VALUES ('"+ str(theVin[0][0]) + "','" + str(theVin[0][1]) +"','" + str(data["dropOffDate"]) + "','" + str(data["rating"])+ "','" + str(data["comment"]) +"')"))
            conn.commit()
            return HttpResponseRedirect('/my_profile/'+ str(theVin[0][1])+'/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = dropOffForm()


    context= {
        'res_num' : res_num,
        'form' : form
    }
    return render(request, 'my_profile/dropOffForm.html', context)
