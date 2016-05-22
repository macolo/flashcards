from django.conf.urls import url

from django.contrib.auth.views import login
from usermgmt import views
from django.contrib.auth.views import logout_then_login, password_change, password_change_done, password_reset, \
    password_reset_confirm, password_reset_complete, password_reset_done
# The urls for the usermgmt unfortunately cannot be placed here
# due to django does not accept namespaces in a redirect in django.contrib.auth.views.password_change
# please see urls.py of the site package

# /accounts/...
urlpatterns = [
    # Can' use these in the usermgmt namespace
    # https://groups.google.com/forum/#!topic/django-users/tmnDcp8t6WM
    # django does not accept namespaces in a redirect in django.contrib.auth.views.password_change
    url(r'^password_change/$', password_change, name='password_change'),
    url(r'^password_change/done/$', password_change_done, name='password_change_done'),
    url(r'^password_reset/$', password_reset, name='password_reset'),
    url(r'^password_reset/done/$', password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        password_reset_confirm, name='password_reset_confirm'),
    url(r'^accounts/reset/done/$', password_reset_complete, name='password_reset_complete'),
]


