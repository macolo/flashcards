from django.contrib import admin

# Register your models here.

from django.contrib import admin

from flashcards.models import CardList, Card, CardListGroup, CardListUser, ShareCardList


# Manage cards
class CardAdmin(admin.ModelAdmin):
    list_display = ('card_question', 'card_answer', 'created_date')

    search_fields = (
        'card_question',
        'card_answer',
    )


admin.site.register(Card, CardAdmin)


# Manage group rights for stacks of cards
class CardListGroupAdmin(admin.ModelAdmin):
    search_fields = (
        'cardlist__cardlist_name',
        'groups__name',
    )

    list_filter = (
        'cardlist',
    )


admin.site.register(CardListGroup, CardListGroupAdmin)


# Manage user rights for stacks of cards
class CardListUserAdmin(admin.ModelAdmin):

    search_fields = (
        'cardlist__cardlist_name',
        'users__first_name',
        'users__last_name',
        'users__username',
    )

    list_filter = (
        'cardlist',
        'users',
    )


admin.site.register(CardListUser, CardListUserAdmin)


# Managed stacks of cards
class CardListAdminUserInline(admin.TabularInline):
    model = CardListUser
    extra = 1  # how many rows to show


class CardListAdminGroupInline(admin.TabularInline):
    model = CardListGroup
    extra = 1  # how many rows to show


class CardListAdmin(admin.ModelAdmin):
    # This activates the SelectBox.js which renders many-to-many nicely
    # filter_horizontal = ('cards', )
    fields = (
        'cardlist_name',
        'owner',
    )
    inlines = (CardListAdminUserInline, CardListAdminGroupInline)
    list_display = ('cardlist_name', 'owner')

    search_fields = (
        'cardlist_name',
    )

    list_filter = (
        'users',
    )


admin.site.register(CardList, CardListAdmin)

admin.site.register(ShareCardList)
