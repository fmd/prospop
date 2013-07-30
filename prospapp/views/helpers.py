####################################
##### ----- View Helpers ----- #####
####################################

def action_logout(request):
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

def authenticate_type(user, type):
    if not hasattr(user, 'type'):
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