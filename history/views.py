from django.shortcuts import render
import mysql.connector
from django.http import HttpResponse
from django.http import HttpResponseRedirect

def index(request, mem_num):
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='ktcsdb')
    cursor = conn.cursor()
    cursor.execute("SELECT name, memNum FROM members WHERE memNum = " +mem_num)
    member = cursor.fetchall()

    cursor.execute("SELECT vin,make, model, pickupDate, dropOffDate, dailyRentalFee FROM cars NATURAL JOIN rentalhistory WHERE memNum ="+ mem_num )
    car_history = cursor.fetchall()

    cursor.execute("SELECT * FROM comments WHERE memNum ='"+ mem_num +"'OR replyTo = "+ mem_num)
    all_comments = cursor.fetchall()

    context = {
        "member" : member,
        "car_history" : car_history,
        'all_comments' : all_comments
    }
    return(render(request, 'history/index.html', context))

def comments(request, mem_num, vin_num):
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='ktcsdb')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM comments WHERE memNum = '" + mem_num+ "' AND vin = '"+ vin_num +"'OR (vin = '"+vin_num+"' AND replyTo = '"+ mem_num +"') " )
    all_comments = cursor.fetchall()
    context = {
        'all_comments' : all_comments
    }
    return render(request, 'history/userComments.html', context)
