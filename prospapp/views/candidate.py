#########################################
##### ----- Candidate Section ----- #####
#########################################

# Django Imports
from django.shortcuts import render, redirect
from django.core.context_processors import csrf
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login

# Our Imports
from prospapp.models import *
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
    context = {
        'authenticated' : auth,
    }
    context.update(csrf(request))
    return render(request, 'candidate/login.html',context)

### Candidate Login Action ###

def do_login(request, onsuccess='/candidate/', onfail='/candidate/login/'):
    user = authenticate(username=request.POST['email'], password=request.POST['password'])
    auth = authenticate_type(user,"CANDIDATE")
    if not auth:

        # TODO
        # Error message: Invalid username or password,

        return redirect("/candidate/login/")

    if user is not None:
        auth_login(request, user)
        return redirect(onsuccess)
    else:

        # TODO
        # Error message: This is not an active user.

        return redirect(onfail) 

### Candidate Signup View ###

def signup(request):
    auth = authenticate_type(request.user,"CANDIDATE")
    context = {
        'authenticated' : auth,
    }
    context.update(csrf(request))
    return render(request, 'candidate/signup.html', context)

### Candidate Signup Action ###

def do_signup(request, onsuccess='/candidate/login/', onfail='/candidate/signup/'):
    post = request.POST

    # TODO
    # Validate candidate signup

    if not user_exists(post['email']): 
        user = create_user(username=post['email'], email=post['email'], password=post['password'], type="CANDIDATE")
        return redirect(onsuccess)
    else:

        # TODO
        # Error message: A user with this email address already exists.

        return redirect(onfail)