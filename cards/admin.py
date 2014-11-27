from django.contrib import admin

# Register your models here.

from django.contrib import admin

from cards.models import CardList, Card, CardListGroup, CardListUser

# Manage cards
class CardAdmin(admin.ModelAdmin):
    list_display = ('card_question', 'card_answer', 'created_date')

admin.site.register(Card, CardAdmin)


# Manage group rights for stacks of cards
class CardListGroupAdmin(admin.ModelAdmin):
    # This activates the SelectBox.js which renders many-to-many nicely
    filter_horizontal = ('groups',)

admin.site.register(CardListGroup)

# Manage user rights for stacks of cards
class CardListUserAdmin(admin.ModelAdmin):
    # This activates the SelectBox.js which renders many-to-many nicely
    filter_horizontal = ('users',)

admin.site.register(CardListUser)


# Managed stacks of cards
class CardListAdminUserInline(admin.TabularInline):
    model = CardListUser
    extra = 1 # how many rows to show

class CardListAdminGroupInline(admin.TabularInline):
    model = CardListGroup
    extra = 1 # how many rows to show

class CardListAdmin(admin.ModelAdmin):
    # This activates the SelectBox.js which renders many-to-many nicely
    filter_horizontal = ('cards', )
    inlines = (CardListAdminUserInline, CardListAdminGroupInline)
    list_display = ('cardlist_name', 'owner')

admin.site.register(CardList, CardListAdmin)