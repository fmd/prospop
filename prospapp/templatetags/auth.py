from django import template

register = template.Library()

@register.inclusion_tag('partial/login_form.html')
def show_login(type):
    if type == 'client':
      action = 'prospapp.views.client.do_login'
    else:
      action = 'prospapp.views.candidate.do_login'

    return { 'action' : action }

@register.inclusion_tag('partial/signup_form.html')
def show_signup(type):
  if type == 'client':
    action = 'prospapp.views.client.do_signup'
  else:
    action = 'prospapp.views.candidate.do_signup'

  return { 'action' : action }


