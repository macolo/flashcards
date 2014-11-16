from django.conf.urls import url

from cards import views

# /cardlists/...
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<cardlist_id>[0-9]+)/$', views.cardlist, name='cardlist'),
    url(r'^(?P<cardlist_id>[0-9]+)/(?P<card_id>[0-9]+)$', views.card, name='card'),
]