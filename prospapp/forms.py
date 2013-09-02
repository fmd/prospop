from django import forms

class LoginForm(forms.Form):
	email = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput())
	user_type = forms.CharField(widget=forms.HiddenInput)

class SignupForm(forms.Form):
	email = forms.CharField()
	password1 = forms.CharField(widget=forms.PasswordInput())
	password2 = forms.CharField(widget=forms.PasswordInput())
	user_type = forms.CharField(widget=forms.HiddenInput)