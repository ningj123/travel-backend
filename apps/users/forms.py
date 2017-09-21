from django import forms
from django.core import validators


class UsernameValidator(validators.RegexValidator):
    regex = '^[0-9]{11}$'


class LoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=11, min_length=11, validators=[UsernameValidator])
    password = forms.CharField(required=True)


class SignupForm(forms.Form):
    username = forms.CharField(required=True, max_length=11, min_length=11, validators=[UsernameValidator])
    password = forms.CharField(required=True)