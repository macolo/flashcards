from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView
from django.contrib.auth.views import logout_then_login, password_change, password_change_done, password_reset, \
    password_reset_confirm, password_reset_complete, password_reset_done

urlpatterns = [
    # this one redirects to the cards app
    url(r'^$', RedirectView.as_view(pattern_name='cards:cardlist_index')),
    url(r'^cardlists/', include('flashcards.urls', namespace='cards')),
    url(r'^admin/', include(admin.site.urls)),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^accounts/', include('usermgmt.urls', namespace='accounts')),
    url(r'^auth/', include('usermgmt.urls_auth')),
]
