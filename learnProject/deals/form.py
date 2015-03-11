from django import forms

class LoginForm(forms.Form):
    default_errors = {
    'required': 'This field is required',
    'invalid': 'Enter a valid value'
    }
    username = forms.CharField(max_length=100,error_messages=default_errors)
    password = forms.CharField(max_length=100,error_messages=default_errors)