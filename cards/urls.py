from django.conf.urls import url

from cards import views

# /cardlists/...
urlpatterns = [
    url(r'^$', views.cardlist_index, name='cardlist_index'),
    url(r'^(?P<cardlist_id>[0-9]+)/$', views.cardlist, name='cardlist'),
    url(r'^new$', views.create_cardlist, name='newcardlist'),
    url(r'^(?P<cardlist_id>[0-9]+)/(?P<card_id>[0-9]+)/$', views.card, name='card'),
    url(r'^(?P<cardlist_id>[0-9]+)/createcard$', views.create_card, name='createcard'),
    url(r'^(?P<original_cardlist_id>[0-9]+)/copy/(?P<card_id>[0-9]+)/to/(?P<new_cardlist_id>[0-9]+)', views.copycardto, name='copycardto'),
    url(r'^(?P<cardlist_id>[0-9]+)/deletecardlist$', views.delete_cardlist, name='deletecardlist'),
    url(r'^(?P<cardlist_id>[0-9]+)/removecardlist$', views.remove_cardlist, name='removecardlist'),
    url(r'^(?P<cardlist_id>[0-9]+)/share$', views.share_cardlist, name='sharecardlist'),
    url(r'^import/(?P<secret>[0-9a-z]+)$', views.import_cardlist, name='importcardlist'),
    url(r'^import/(?P<secret>[0-9a-z]+)/done$', views.import_cardlist_confirmed, name='importcardlistconfirmed'),
    url(r'^notifications$', views.notifications_list, name='notificationslist'),
]