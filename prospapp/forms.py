from django import forms
from prospapp.models import *

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    user_type = forms.CharField(widget=forms.HiddenInput)

class SignupForm(forms.Form):
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())
    user_type = forms.CharField(widget=forms.HiddenInput)

class NewTestForm(forms.Form):
    label = forms.CharField()
    image = forms.ModelChoiceField(queryset=TestImage.objects.all(), widget=forms.Select(attrs={'class':'selector'}))
    public = forms.BooleanField(required=False)

class NewTestAuthForm(forms.Form):
    pass

class NewTestInstanceForm(forms.Form):
    pass