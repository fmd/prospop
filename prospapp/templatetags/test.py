from django import template

register = template.Library()

@register.inclusion_tag('partial/test_show.html')
def show_test(test):
    return {'test': test}

@register.inclusion_tag('partial/forms/test_edit.html')
def edit_test(form):
    return {'form': form}

@register.inclusion_tag('partial/forms/test_auth_edit.html')
def edit_test_auth(test_auth):
    return {'test_auth': test_auth}
