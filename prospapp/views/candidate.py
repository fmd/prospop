#########################################
##### ----- Candidate Section ----- #####
#########################################

# Django Imports
from django.shortcuts import render, redirect
from django.core.context_processors import csrf

# Our Imports
from prospapp.models import *
from prospapp.forms import *
from helpers import *

### Candidate Account View ###

def home(request):
    auth = authenticate_type(request.user,"CANDIDATE")
    if not auth:

        # TODO
        # Error message: You must be logged in to continue.

        return redirect("/candidate/login/")

    context = {
        'authenticated' : auth,
        'email'         : request.user.email,
        'instances'     : request.user.instances.all(),
    }  
    return render(request, 'candidate/home.html', context)

### Candidate Login View ###

def login(request):
    response = ensure_unauthorized(request)
    if response:

        # TODO
        # Error message: You must be logged in to continue.

        return response
    
    auth = authenticate_type(request.user,"CANDIDATE")
    form = LoginForm(initial = {'user_type': 'candidate'})
    context = {
        'authenticated' : auth,
        'form' : form,
    }
    context.update(csrf(request))
    return render(request, 'candidate/login.html',context)

### Candidate Signup View ###

def signup(request):
    auth = authenticate_type(request.user,"CANDIDATE")
    form = SignupForm(initial = {'user_type': 'candidate'})
    context = {
        'authenticated' : auth,
        'form'          : form,
    }
    context.update(csrf(request))
    return render(request, 'candidate/signup.html', context)