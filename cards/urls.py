from django.conf.urls import url

from cards import views

# /cardlists/...
urlpatterns = [
    url(r'^$', views.cardlist_index, name='cardlist_index'),
    url(r'^(?P<cardlist_id>[0-9]+)/$', views.cardlist, name='cardlist'),
    url(r'^new$', views.new_cardlist, name='newcardlist'),
    url(r'^(?P<cardlist_id>[0-9]+)/(?P<card_id>[0-9]+)/$', views.card, name='card'),
    url(r'^(?P<cardlist_id>[0-9]+)/addcard$', views.add_card_to_cardlist, name='addcard'),
    url(r'^(?P<cardlist_id>[0-9]+)/deletecardlist$', views.delete_cardlist, name='deletecardlist'),

]