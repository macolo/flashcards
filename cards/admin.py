from django.contrib import admin

# Register your models here.

from django.contrib import admin

from cards.models import CardList
from cards.models import Card

class CardListAdmin(admin.ModelAdmin):
    # This activates the SelectBox.js which renders many-to-many nicely
    filter_horizontal = ('users', 'groups')

class CardAdmin(admin.ModelAdmin):
    # This activates the SelectBox.js which renders many-to-many nicely
    filter_horizontal = ('cardlist',)

admin.site.register(CardList, CardListAdmin)
admin.site.register(Card, CardAdmin)