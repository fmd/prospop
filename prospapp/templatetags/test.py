from django import template

register = template.Library()

@register.inclusion_tag('partial/test_show.html')
def show_test(test):
    return {'test': test}

@register.inclusion_tag('partial/test_edit.html')
def edit_test(test):
    return {'test': test}