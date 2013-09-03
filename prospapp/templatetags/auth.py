from django import template

register = template.Library()

@register.inclusion_tag('partial/forms/login.html')
def show_login(form):
    context = {
        'form'   : form,
    }
    return context

@register.inclusion_tag('partial/forms/signup.html')
def show_signup(form):
    context = {
        'form'   : form,
    }
    return context


