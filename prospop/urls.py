# Imports
from django.conf.urls import patterns, include, url
from django.contrib import admin

#Prospapp imports
import prospapp.views

# Use the admin backend
admin.autodiscover()

# Custom 404 handler
handler404 = 'prospop.views.show_404'

# Custom 500 handler
handler500 = 'prospop.views.show_500'

urlpatterns = patterns('prospapp.views.frontend',
    
    #Frontend
    url(r'^$',         'root'),
    url(r'^home/$',    'home'),
    url(r'^about/$',   'about'),
    url(r'^pricing/$', 'pricing'),

    #Frontend - Functional
    url(r'^tests/$',                  'tests'),
    url(r'^test/(\d{1,15})/$',        'test'),
    url(r'^test/(\d{1,15})/create/$', 'create_test'),
)

urlpatterns += patterns('prospapp.views.client',

    #Client
    url(r'^client/$',           'home'),
    url(r'^client/login/$',     'login'),
    url(r'^client/signup/$',    'signup'),
    url(r'^client/do/login/$',  'do_login'),
    url(r'^client/do/signup/$', 'do_signup'),

    #Client - Tests
    url(r'^client/tests/$',           'tests'),
    url(r'^client/test/(\d{1,15})/$', 'test'),
    url(r'^client/test/new/$',        'new_test'),
    url(r'^client/test/create/$',     'create_test'),

)

urlpatterns += patterns('prospapp.views.candidate',

    #Candidate
    url(r'^candidate/$',           'home'),
    url(r'^candidate/login/$',     'login'),
    url(r'^candidate/signup/$',    'signup'),
    url(r'^candidate/do/login/$',  'do_login'),
    url(r'^candidate/do/signup/$', 'do_signup'),

)

urlpatterns += patterns('prospapp.views.helpers',

    #Shared
    url(r'^logout/$', 'do_logout'),

)

urlpatterns += patterns('',

    #Admin
    url(r'^admin/', include(admin.site.urls)),
)


from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
