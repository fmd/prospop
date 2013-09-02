from django import forms

class LoginForm(forms.Form):
  email = forms.CharField()
  password = forms.CharField(widget=forms.PasswordInput())

class SignupForm(forms.Form):
  email = forms.CharField()
  password1 = forms.CharField(widget=forms.PasswordInput())
  password2 = forms.CharField(widget=forms.PasswordInput())