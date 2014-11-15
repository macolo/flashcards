from django.contrib import admin

# Register your models here.

from django.contrib import admin

from cards.models import CardList
from cards.models import Card

admin.site.register(CardList)
admin.site.register(Card)