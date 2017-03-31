from django import forms
from functools import partial
DateInput = partial(forms.DateInput, {'class': 'datepicker'})
class addCarForm(forms.Form):
    vin = forms.IntegerField(label="Vin")
    make = forms.CharField(label="Make", max_length=250)
    model = forms.CharField(label="Model", max_length=200)
    year = forms.IntegerField(label="Year")
    dailyRentalFee = forms.IntegerField(label="Daily Rental Fee")
    locationNumber = forms.IntegerField(label="Location Number")
    picture = forms.CharField(label="Picture", max_length=500)
    odometer = forms.IntegerField(label="Odometer")

class reservationForm(forms.Form):
    date = forms.DateField(label="Date:", widget=DateInput())

class invoiceForm(forms.Form):
    start_date = forms.DateField(label="Start Date:", widget=DateInput())
    end_date = forms.DateField(label="End Date", widget=DateInput())

class locationForm(forms.Form):
    location = forms