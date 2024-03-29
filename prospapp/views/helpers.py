###############################
##### ----- Helpers ----- #####
###############################

#Python Imports
import logging
logger = logging.getLogger(__name__)

# Django Imports 
from django.contrib.auth import logout, login, authenticate
from django.shortcuts import redirect

# Our Imports
from prospapp.models import *
from prospapp.forms import *

# Auth helpers
def do_login(request):
    post = request.POST
    form = LoginForm(post)
    user_type = post['user_type']
    on_success = '/'+user_type+'/'
    on_fail = '/'+user_type+'/login/'

    user = authenticate(username=post['email'], password=post['password'])
    auth = authenticate_type(user,user_type.upper())

    login_data = {}
    login_data['user_type'] = post['user_type']
    login_data['email']     = post['email']

    request.session['login_data'] = login_data
    request.modified = True

    if not auth:

        # TODO
        # Error message: Invalid username or password.
        logger.error("Bad username/password")
        return redirect(on_fail)

    if not user:
        logger.error("No user.")
        return redirect(on_fail)
    
    login(request, user)

    # We no longer need this session data because the request succeeded.
    request.session.pop('login_data')
    return redirect(on_success)

def do_signup(request):
    post = request.POST
    form = SignupForm(post)

    if post['password1'] != post['password2']:
        return redirect(onfail)

    if not user_exists(post['email']): 
        user = create_user(username=post['email'], email=post['email'], password=post['password1'], type="CLIENT")
        return redirect(onsuccess)
    else:

        # TODO
        # Error message: User already exists with this email address.

        return redirect(onfail)

def do_logout(request):
    logout(request)
    return redirect('/')

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

def user_exists_by_email(email):
    user_count = Account.objects.filter(email=email).count()
    if user_count == 0:
        return False
    return True

def authenticate_type(user, type):
    if not hasattr(user, 'type'):
        logger.error("User has no type.")
        return False

    if (user.is_authenticated() and user.type == type):
        return True
        
    return False

def ensure_unauthorized(request):
    if request.user.is_authenticated():
        if request.user.type == "CANDIDATE":
            return redirect("/candidate/")
        elif request.user.type == "CLIENT":
            return redirect("/client/")
    return False

# Test Helpers
def authenticate_test(user, test):
    if test.is_public:
        return True

    if test.owner == user:
        return True

    return False

def authenticate_test_owner(user, test):
    if test.owner == user:
        return True

    return False