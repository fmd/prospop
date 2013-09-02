######################################
##### ----- Client Section ----- #####
######################################

# Django Imports
from django.shortcuts import render, redirect
from django.core.context_processors import csrf
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login

# Our Imports
from prospapp.models import *
from helpers import *

### Client Account Page ###

def home(request):
    auth = authenticate_type(request.user,"CLIENT")
    if not auth:

        # TODO
        # Error message: You must be logged in to continue.

        return redirect("/client/login/")

    context = {
        'authenticated' : auth,
        'email' : request.user.email,
    }  
    return render(request, 'client/home.html', context)

### Client Test Page ###

def test(request, id):
    auth = authenticate_type(request.user,"CLIENT")
    if not auth:

        # TODO
        # Error message: You must be logged in to continue.

        return redirect("/client/login/")

    test = Test.objects.get(id=id)
    auth = authenticate_test(request.user, test)
    if not test:

        # TODO
        # Error message: No such test.

        return redirect("client/tests/")

    if not auth:

        # TODO
        # Error message: You do not own this test.

        return redirect("/client/tests/")

    context = {
        'authenticated' : auth,
        'test'          : test,
    }
    return render(request, 'client/test.html', context)

### Client Tests Page ###

def tests(request):
    auth = authenticate_type(request.user,"CLIENT")
    if not auth:

        # TODO
        # Error message: You must be logged in to continue.

        return redirect("/client/login/")

    images = request.user.tests.all()
    for image in images:
        image.url = "hello"
    context = {
        'authenticated' : auth,
        'images'        : images,
    }
    return render(request, 'client/tests.html', context)

### Client New Test Page ###

def new_test(request):
    auth = authenticate_type(request.user,"CLIENT")
    if not auth:

        # TODO
        # Error message: You must be logged in to continue.

        return redirect("/client/login/")

    images = TestImage.objects.all()
    context = {
        'authenticated' : auth,
        'images'        : images,
    }
    return render(request, 'client/new_test.html', context)

### Client New Test Action ###

def create_test(request, onsuccess='/client/tests/', onfail='/test/new/'):
    post = request.POST

    label = post['label']
    image = post['image']
    
    is_public = False
    if 'public' in post:
        is_public = True


    owner = request.user
    
    # TODO
    # Validate Test Information

    test = Test(label=label, owner=owner, is_public=is_public, image=TestImage.objects.get(id=image))
    test.save()
    return redirect(onsuccess)

### Client Login View ###

def login(request):
    response = ensure_unauthorized(request)
    if response:
        return response
    
    auth = authenticate_type(request.user,"CLIENT")
    context = {
        'authenticated' : auth,
    }
    context.update(csrf(request))
    return render(request, 'client/login.html',context)

### Client Login Action ###

def do_login(request, onsuccess='/client/', onfail='/client/login/'):
    user = authenticate(username=request.POST['email'], password=request.POST['password'])
    auth = authenticate_type(user,"CLIENT")
    if not auth:

        # TODO
        # Error message: Invalid username or password.

        return redirect("/client/login/")

    if user is not None:
        auth_login(request, user)
        return redirect(onsuccess)
    else:
        return redirect(onfail)

### Client Signup View ###

def signup(request):
    auth = authenticate_type(request.user,"CLIENT")
    context = {
        'authenticated' : auth,
    }
    context.update(csrf(request))
    return render(request, 'client/signup.html', context)

### Client Signup Action ###

def do_signup(request, onsuccess='/client/login/', onfail='/client/signup/'):
    post = request.POST

    # TODO
    # Validate client signup

    if not user_exists(post['email']): 
        user = create_user(username=post['email'], email=post['email'], password=post['password'], type="CLIENT")
        return redirect(onsuccess)
    else:
        return redirect(onfail)