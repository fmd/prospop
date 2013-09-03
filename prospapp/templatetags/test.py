from django import template

register = template.Library()

@register.inclusion_tag('partial/test_show.html')
def show_test(test):
    return {'test': test}

@register.inclusion_tag('partial/test_auths_show.html')
def show_test_auths(test):

    # Simplify the authorizations object for printing.
    auths = []
    for auth in test.authorizations.all():
        row = {'email':None,'key':None,'id':0}
        if auth.user:
            row['email'] = auth.user.email
            row['id']    = auth.user.id
        else:
            row['email'] = auth.email
            row['key']   = auth.key
        auths.append(row)
    return {'auths' : auths, 'count' : len(auths)}


@register.inclusion_tag('partial/forms/test_edit.html')
def edit_test(form):
    return {'form': form}

@register.inclusion_tag('partial/forms/test_auth_edit.html')
def edit_test_auth(form):

    return {'form': form}
