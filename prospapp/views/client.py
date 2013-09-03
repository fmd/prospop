 ######################################
##### ----- Client Section ----- #####
######################################

#Python Imports
import logging
logger = logging.getLogger(__name__)

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
        logger.error("You must be logged in to continue.")
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
    auth = authenticate_test_owner(request.user, test)
    if not test:

        # TODO
        # Error message: No such test.

        return redirect('client/tests/')

    if not auth:

        # TODO
        # Error message: You do not own this test.

        return redirect('/client/tests/')


    if 'new_test_auth_data' in request.session.keys():
        form = NewTestAuthForm(initial = request.session['new_test_auth_data'])
        request.session.pop('new_test_auth_data')
        request.session.modified = True
    else:
        form = NewTestAuthForm(initial = {'test' : test.id})

    context = {
        'authenticated' : auth,
        'test'          : test,
        'auth_form'     : form,
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

    form = None
    if 'new_test_data' in request.session.keys():
        form = NewTestForm(initial = request.session['new_test_data'])
        request.session.pop('new_test_data')
        request.session.modified = True
    else:
        form = NewTestForm(initial = {'public': True})

    context = {
        'authenticated' : auth,
        'form'          : form,
    }
    return render(request, 'client/new_test.html', context)


### Client Delete Test Action ###
def do_delete_test(request, id):
    auth = authenticate_type(request.user, 'CLIENT')
    if not auth:

        # TODO
        # Error message: You must be logged in to continue.
        return redirect('/client/login/')   

    test = Test.objects.get(id=id)
    if not test:

        # TODO
        # Message: No such test exists.
        logger.error('No such test exists.')
 
    can_edit_test = authenticate_test_owner(request.user, test)
    if not can_edit_test:

        # TODO
        # Message: You are not authorized to edit this test.
        logger.error('You are not authorized to edit this test.')

        return redirect('/client/tests/')

    test.fe_delete()
    return redirect('/client/tests/')

### Client New Test Action ###

def do_new_test(request):
    on_fail='/client/test/new/'
    post = request.POST
    form = NewTestForm(post)
    auth = authenticate_type(request.user, 'CLIENT')

    # Store the posted form data in the session for next time.
    request.session['new_test_data'] = post
    request.session.modified = True

    if not auth:

        # TODO
        # Error message: You must be logged in to continue.
        return redirect('/client/login/')
    
    if not form.is_valid():

        # TODO
        # Message: Reason it wasn't valid.
        logger.error("Form is not valid.")
        return redirect(on_fail)

    image = form.cleaned_data['image']
    label = form.cleaned_data['label']
    is_public = form.cleaned_data['public']

    test_exists = Test.objects.filter(owner=request.user, label=label, image=image).exists()
    if test_exists:

        # TODO
        # Message: You already have a test called [label].
        logger.error('You already have a test called '+label+' using image '+image.label)
        return redirect(on_fail)

    test = Test(label=label, owner=request.user, is_public=is_public, image=image)
    test.save()

    # It was sucessful, so we don't need the data anymore.
    request.session.pop('new_test_data')
    request.session.modified = False

    return redirect('/client/test/'+str(test.id)+'/')

### Client New Test Auth Action ###

def do_new_test_auth(request):

    auth = authenticate_type(request.user, 'CLIENT')
    post = request.POST
    form = NewTestAuthForm(post)

    # Store the posted form data in the session for next time.
    request.session['new_test_auth_data'] = post
    request.session.modified = True

    if not auth:

        # TODO
        # Error message: You must be logged in to continue.
        logger.error('You must be logged in to continue.')

        return redirect('/client/login/')

    if not form.is_valid():

        # TODO
        # Message: Reason it isn't valid.
        logger.error('Form was not valid.')

        if 'test' in post.keys():
            test_id = post['test']
        else:
            return redirect('/client/tests/')

        if test_id > 0:
            return redirect('/client/test/'+test_id+'/')
        else:
            return redirect('/client/tests/')

    test = Test.objects.get(id=form.cleaned_data['test'])
    if not test:

        # TODO
        # Message: No such test exists.
        logger.error('No such test exists.')

        return redirect('/client/tests/')

    can_edit_test = authenticate_test_owner(request.user, test)
    if not can_edit_test:

        # TODO
        # Message: You are not authorized to edit this test.
        logger.error('You are not authorized to edit this test.')

        return redirect('/client/tests/')

    email = form.cleaned_data['email']
    if email in test.authorizations.all().values_list('email', flat = True):

            # TODO
            # Message: This user already has permission to access this test!
            logger.error('You have already sent this person an invite.')
            return redirect('/client/test/'+str(test.id)+'/')

    user = None
    if user_exists_by_email(email):
        user = Account.objects.get(email=email)
        if not user.type == 'CANDIDATE':

            # TODO 
            # Message: This user is not a candidate!
            logger.error('This user is not a candidate!')
            return redirect('/client/test/'+str(test.id)+'/')

        authorized_users = test.authorizations.all().values_list('user', flat=True)
        if user.id in authorized_users:

            # TODO
            # Message: This user already has permission to access this test!
            logger.error('This user already has permission to access this test!')
            return redirect('/client/test/'+str(test.id)+'/')
        email = ''

    test_auth = TestAuth.objects.create(test=test, email=email, user=user)
    test.authorizations.add(test_auth)

    # If we're successful, we don't need the session data anymore.
    request.session.pop('new_test_auth_data')
    request.session.modified = False

    return redirect('/client/test/'+str(test.id)+'/')


### Client Login View ###

def login(request):
    response = ensure_unauthorized(request)
    if response:
        return response
    
    auth = authenticate_type(request.user,'CLIENT')
    
    
    if 'login_data' in request.session.keys():
        form = LoginForm(initial = request.session['login_data'])
        request.session.pop('login_data')
        request.session.modified = True
    else:
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