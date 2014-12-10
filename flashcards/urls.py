from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView

urlpatterns = patterns('',
    # this one redirects to the cards app
    url(r'^$', RedirectView.as_view(pattern_name='cards:cardlist_index')),
    url(r'^cardlists/', include('cards.urls', namespace='cards')),
    url(r'^admin/', include(admin.site.urls)),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^accounts/', include('usermgmt.urls', namespace='accounts')),
    # Can' use these in the usermgmt app because of
    # https://groups.google.com/forum/#!topic/django-users/tmnDcp8t6WM
    # django does not accept namespaces in a redirect in django.contrib.auth.views.password_change
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
    url(r'^accounts/password_change/$', 'django.contrib.auth.views.password_change', name='password_change'),
    url(r'^accounts/password_change/done/$', 'django.contrib.auth.views.password_change_done', name='password_change_done'),
    url(r'^accounts/password_reset/$', 'django.contrib.auth.views.password_reset', name='password_reset'),
    url(r'^accounts/password_reset/done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
    url(r'^accounts/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'django.contrib.auth.views.password_reset_confirm', name='password_reset_confirm'),
    url(r'^accounts/reset/done/$', 'django.contrib.auth.views.password_reset_complete', name='password_reset_complete'),

)
