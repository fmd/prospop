from django.conf.urls import patterns, include, url
from django.contrib import admin

# Use the admin backend
admin.autodiscover()

# Custom 404 handler
handler404 = 'prospop.views.show_404'
handler500 = 'prospop.views.show_500'

urlpatterns = patterns('',
    
    #Frontend
    url(r'^$', 'prospapp.views.home'),
    url(r'^about/$', 'prospapp.views.about'),
    url(r'^pricing/$', 'prospapp.views.pricing'),

    #Client
    url(r'^client/$', 'prospapp.views.client'),
    url(r'^client/login/$', 'prospapp.views.view_client_login'),
    url(r'^client/signup/$', 'prospapp.views.view_client_signup'),
    url(r'^client/login_auth/$', 'prospapp.views.action_client_login'),
    url(r'^client/signup_auth/$', 'prospapp.views.action_client_signup'),
    
    #Tests
    url(r'^client/tests/$', 'prospapp.views.tests'),
    url(r'^client/test/(\d{1,15})/$', 'prospapp.views.test'),
    url(r'^client/test/new/$','prospapp.views.view_new_test'),
    url(r'^client/test/new/action/$','prospapp.views.action_new_test'),

    #Candidate
    url(r'^candidate/$', 'prospapp.views.candidate'),
    url(r'^candidate/login/$', 'prospapp.views.view_candidate_login'),
    url(r'^candidate/signup/$', 'prospapp.views.view_candidate_signup'),
    url(r'^candidate/login_auth/$', 'prospapp.views.action_candidate_login'),
    url(r'^candidate/signup_auth/$', 'prospapp.views.action_candidate_signup'),

    #Shared
    url(r'^client/logout/$', 'prospapp.views.action_logout'),

    #Admin
    url(r'^admin/', include(admin.site.urls)),
)

#Extra patterns to add:
#sign up
#log in

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
