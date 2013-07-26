### Django Imports ###
from django.core.context_processors import csrf
from django.shortcuts import render_to_response, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.template import Template, Context
from django.http import HttpResponse

import logging
logger = logging.getLogger(__name__)

### Our Imports ###
from prospapp.models import *
from docker import *

################################
##### ----- Frontend ----- #####
################################

#################
### Root Page ###
#################

def root(request):
    if request.user.is_authenticated():
        if request.user.type == "CANDIDATE":
            return redirect("/candidate/")
        elif request.user.type == "CLIENT":
            return redirect("/client/")
    return home(request)

#################
### Home Page ###
#################

def home(request):
    return render(request, 'frontend/home.html', {})

##################
### About Page ###
##################

def about(request):
    return render(request, 'frontend/about.html', {})

####################
### Pricing Page ###
####################

def pricing(request):
    return render(request, 'frontend/pricing.html', {})

######################################
##### ----- Client Section ----- #####
######################################

###########################
### Client Account Page ###
###########################

### Client Account View ###

def client(request):
    auth = authenticate_type(request.user,"CLIENT")
    if not auth:
        return redirect("/client/login/")

    context = {
        'authenticated' : auth,
        'email' : request.user.email,
    }  
    return render(request, 'client/home.html', context)

########################
### Client Test Page ###
########################

def test(request, id):
    auth = authenticate_type(request.user,"CLIENT")
    if not auth:
        return redirect("/client/login/")

    test = request.user.tests.get(id=id)
    context = {
        'authenticated' : auth,
        'test'          : test,
    }
    return render(request, 'client/test.html', context)

#########################
### Client Tests Page ###
#########################

### Tests View ###

def tests(request):
    auth = authenticate_type(request.user,"CLIENT")
    if not auth:
        return redirect("/client/login/")

    images = request.user.tests.all()
    for image in images:
        image.url = "hello"
    context = {
        'authenticated' : auth,
        'images'        : images,
    }
    return render(request, 'client/tests.html', context)

############################
### Client New Test Page ###
############################

### New Test View ###

def view_new_test(request):
    auth = authenticate_type(request.user,"CLIENT")
    if not auth:
        return redirect("/client/login/")

    images = TestImage.objects.all()
    context = {
        'authenticated' : auth,
        'images'        : images,
    }
    return render(request, 'client/new_test.html', context)

### New Test Action ###

def action_new_test(request, onsuccess='/client/tests/', onfail='/test/new/'):
    post = request.POST

    label = post['label']
    image = post['image']
    owner = request.user
    
    # TODO
    # Validate Test Information

    test = Test(label=label, owner=owner, image=TestImage.objects.get(id=image))
    test.save()
    return redirect(onsuccess)

#########################
### Client Login Page ###
#########################

### Login View ###

def view_client_login(request):
    auth = authenticate_type(request.user,"CLIENT")
    context = {
        'authenticated' : auth,
    }
    context.update(csrf(request))
    return render(request, 'client/login.html',context)

### Login Action ###

def action_client_login(request, onsuccess='/client/', onfail='/client/login/'):
    user = authenticate(username=request.POST['email'], password=request.POST['password'])
    auth = authenticate_type(user,"CLIENT")
    if not auth:
        return redirect("/client/login/")

    if user is not None:
        login(request, user)
        return redirect(onsuccess)
    else:
        return redirect(onfail)

##########################
### Client Signup Page ###
##########################

### Signup View ###

def view_client_signup(request):
    auth = authenticate_type(request.user,"CLIENT")
    context = {
        'authenticated' : auth,
    }
    context.update(csrf(request))
    return render(request, 'client/signup.html', context)

### Signup Action ###

def action_client_signup(request, onsuccess='/client/login/', onfail='/client/signup/'):
    post = request.POST

    # TODO
    # Validate client signup

    if not user_exists(post['email']): 
        user = create_user(username=post['email'], email=post['email'], password=post['password'], type="CLIENT")
        return redirect(onsuccess)
    else:
        return redirect(onfail)

#########################################
##### ----- Candidate Section ----- #####
#########################################

### Candidate Account View ###

def candidate(request):
    auth = authenticate_type(request.user,"CANDIDATE")
    if not auth:
        return redirect("/candidate/login/")
    context = {
        'authenticated' : auth,
        'email'         : request.user.email,
    }  
    return render(request, 'candidate/home.html', context)

############################
### Candidate Login Page ###
############################

### Login View ###

def view_candidate_login(request):
    auth = authenticate_type(request.user,"CANDIDATE")
    context = {
        'authenticated' : auth,
    }
    context.update(csrf(request))
    return render(request, 'candidate/login.html',context)

### Login Action ###

def action_candidate_login(request, onsuccess='/candidate/', onfail='/candidate/login/'):
    user = authenticate(username=request.POST['email'], password=request.POST['password'])
    auth = authenticate_type(user,"CANDIDATE")
    if not auth:
        return redirect("/candidate/login/")

    if user is not None:
        login(request, user)
        return redirect(onsuccess)
    else:
        return redirect(onfail) 

##########################
### Client Signup Page ###
##########################

### Signup View ###

def view_candidate_signup(request):
    auth = authenticate_type(request.user,"CANDIDATE")
    context = {
        'authenticated' : auth,
    }
    context.update(csrf(request))
    return render(request, 'candidate/signup.html', context)

### Signup Action ###

def action_candidate_signup(request, onsuccess='/candidate/login/', onfail='/candidate/signup/'):
    post = request.POST

    # TODO
    # Validate candidate signup

    if not user_exists(post['email']): 
        user = create_user(username=post['email'], email=post['email'], password=post['password'], type="CANDIDATE")
        return redirect(onsuccess)
    else:
        return redirect(onfail)

#######################################################
##### ----- Candidate/Client Shared Section ----- #####
#######################################################

### Logout Action ###

def action_logout(request):
    logout(request)
    return redirect('/')

######################
### Shared Helpers ###
######################

def create_user(username, email, password, type):
    user = Account(username=username, email=email, type=type)
    user.set_password(password)
    user.save()
    return user

def user_exists(username):
    user_count = Account.objects.filter(username=username).count()
    if user_count == 0:
        return False
    return True

def authenticate_type(user, type):
    if not hasattr(user, 'type'):
        return False

    if (user.is_authenticated() and user.type == type):
        return True
    return False
