 ######################################
##### ----- Client Section ----- #####
######################################

# Django Imports
from django.shortcuts import render, redirect
from django.core.context_processors import csrf

# Our Imports
from prospapp.models import *
from prospapp.forms import *
from helpers import *

### Client Account Page ###

def home(request):
    auth = authenticate_type(request.user,'CLIENT')
    if not auth:

        # TODO
        # Error message: You must be logged in to continue.

        return redirect('/client/login/')

    context = {
        'authenticated' : auth,
        'email' : request.user.email,
    }  
    return render(request, 'client/home.html', context)

### Client Test Page ###

def test(request, id):
    auth = authenticate_type(request.user,'CLIENT')
    if not auth:

        # TODO
        # Error message: You must be logged in to continue.

        return redirect('/client/login/')

    test = Test.objects.get(id=id)
    auth = authenticate_test(request.user, test)
    if not test:

        # TODO
        # Error message: No such test.

        return redirect('client/tests/')

    if not auth:

        # TODO
        # Error message: You do not own this test.

        return redirect('/client/tests/')

    context = {
        'authenticated' : auth,
        'test'          : test,
    }
    return render(request, 'client/test.html', context)

### Client Tests Page ###

def tests(request):
    auth = authenticate_type(request.user,'CLIENT')
    if not auth:

        # TODO
        # Error message: You must be logged in to continue.

        return redirect('/client/login/')

    images = request.user.tests.all()
    for image in images:
        image.url = 'hello'
    context = {
        'authenticated' : auth,
        'images'        : images,
    }
    return render(request, 'client/tests.html', context)

### Client New Test Page ###

def new_test(request):
    auth = authenticate_type(request.user,'CLIENT')
    if not auth:

        # TODO
        # Error message: You must be logged in to continue.

        return redirect('/client/login/')

    form = NewTestForm(initial = {'public': True})

    context = {
        'authenticated' : auth,
        'form'          : form,
    }
    return render(request, 'client/new_test.html', context)

### Client New Test Action ###

def do_new_test(request):
    on_fail='/client/test/new/'
    auth = authenticate_type(request.user, 'CLIENT')
    if not auth:

        # TODO
        # Error message: You must be logged in to continue.

        return redirect(on_fail)

    post = request.POST
    form = NewTestForm(post)
    
    if not form.is_valid():

        # TODO
        # Message: Reason it wasn't valid.

        return render(on_fail)

    test = Test(label=form.cleaned_data['label'], owner=request.user, is_public=form.cleaned_data['public'], image=form.cleaned_data['image'])
    test.save()
    return redirect('/client/test/'+test.id+'/')

### Client Login View ###

def login(request):
    response = ensure_unauthorized(request)
    if response:
        return response
    
    auth = authenticate_type(request.user,'CLIENT')
    form = LoginForm(initial = {'user_type': 'client'})

    context = {
        'authenticated' : auth,
        'form'          : form,
    }
    context.update(csrf(request))
    return render(request, 'client/login.html',context)

### Client Signup View ###

def signup(request):
    auth = authenticate_type(request.user,'CLIENT')
    form = SignupForm(initial = {'user_type': 'client'})

    context = {
        'authenticated' : auth,
        'form'          : form,
    }
    context.update(csrf(request))
    return render(request, 'client/signup.html', context)