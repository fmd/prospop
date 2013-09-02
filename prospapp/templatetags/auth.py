from django import template

register = template.Library()

@register.inclusion_tag('partial/login_form.html')
def show_login(form, type):
    if type == 'client':
        action = 'prospapp.views.client.do_login'
    else:
        action = 'prospapp.views.candidate.do_login'

    context = {
        'form'   : form,
    }

    return context

@register.inclusion_tag('partial/signup_form.html')
def show_signup(form, type):
    form.user_type = type
    context = {
        'form'   : form,
    }

    return context


