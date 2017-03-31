from django import forms

class loginForm(forms.Form):
    username = forms.CharField(label="username", max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    widgets = {
        'password': forms.PasswordInput(),
    }

class signupForm(forms.Form):
    name = forms.CharField(label="Name", max_length=50)
    address = forms.CharField(label="Address", max_length=250)
    phoneNumber = forms.CharField(label="Phone Number", max_length=200)
    email = forms.CharField(label="Email", max_length=200)
    licence = forms.CharField(label="Licence Number", max_length=50)
    password = forms.CharField(label="Password", max_length=100)


