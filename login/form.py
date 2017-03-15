from django import forms

class loginForm(forms.Form):
    username = forms.CharField(label="username", max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    widgets = {
        'password': forms.PasswordInput(),
    }
