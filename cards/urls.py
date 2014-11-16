from django.conf.urls import url

from cards import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]