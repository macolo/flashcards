from django.conf.urls import url

from django.contrib.auth.views import login
from usermgmt import views
from django.contrib.auth.views import logout_then_login

# The urls for the usermgmt unfortunately cannot be placed here
# due to django does not accept namespaces in a redirect in django.contrib.auth.views.password_change
# please see urls.py of the site package

# /accounts/...
urlpatterns = [
    url(r'^logout/$', logout_then_login, name='logout'),
    url(r'^login/$', views.login, name='login'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^validate-email/(?P<code>.*)/$', views.validate_email, name='validate_email'),
    url(r'^set-password/$', views.set_password, name='password_set'),
]
