from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView

urlpatterns = [
    # this one redirects to the cards app
    url(r'^$', RedirectView.as_view(pattern_name='cards:cardlist_index')),
    url(r'^cardlists/', include('flashcards.urls', namespace='cards')),
    path('admin/', admin.site.urls),
    url('', include('social_django.urls', namespace='social')),
    url(r'^accounts/', include('usermgmt.urls', namespace='accounts')),
    url(r'^', include('django.contrib.auth.urls')),
]
