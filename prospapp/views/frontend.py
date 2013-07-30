################################
##### ----- Frontend ----- #####
################################

### Imports ###

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

def fe_tests(request):
    context = {
        'tests' : Test.objects.all()
    }
    return render(request, 'frontend/tests.html',context)

### Single Test ###

def fe_test(request, id):
    context = {
        'test' : Test.objects.get(id=id)
    }
    return render(request, 'frontend/test.html',context)

### New Test Instance ###

def action_new_test_instance(request, id):

    if not request.user.is_authenticated():

        # TODO
        # Error message: You must be logged in to start this test.
        # Redirect the candidate back to the test page after login via session variable.

        return redirect("/candidate/login/")
    if not request.user.type == "CANDIDATE":

        # TODO
        # Error message: Clients cannot attempt tests.

        return redirect("/test/"+id+"/")

    test = Test.objects.get(id=id)

    user_has_test = TestInstance.objects.filter(test=test,owner=request.user).exists()
    if not user_has_test:
        instance = TestInstance(test=test, owner=request.user)
        instance.save()
    else:

        # TODO
        # Redirect to the currently open test
        pass
    
    return redirect("/test/"+id+"/")