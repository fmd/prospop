################################
##### ----- Frontend ----- #####
################################

# Django Imports
from django.shortcuts import render, redirect

# Our Imports
from prospapp.models import *
from helpers import *

#########################
### Frontend - Public ###
#########################

### Root Page ###

def root(request):
    response = ensure_unauthorized(request)
    if not response:
        return home(request)

    return response

### Home Page ###

def home(request):
    return render(request, 'frontend/home.html', {})

### About Page ###

def about(request):
    return render(request, 'frontend/about.html', {})

### Pricing Page ###

def pricing(request):
    return render(request, 'frontend/pricing.html', {})

#############################
### Frontend - Functional ###
#############################

### Browse Tests ###

def tests(request):
    context = {
        'tests' : Test.objects.filter(is_public = True)
    }
    return render(request, 'frontend/tests.html',context)

### Single Test ###

def test(request, id):
    context = {
        'test' : Test.objects.get(id=id)
    }
    return render(request, 'frontend/test.html',context)