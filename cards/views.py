import logging

from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.

from cards.models import CardList, Card

@login_required
def index(request):

    # Find out about the current user and his groups
    current_user_groups = request.user.groups.all()
    current_user_id = request.user.id

    current_user_group_ids = current_user_groups.values_list('id', flat=True)

    if request.user.is_superuser or request.user.is_staff:
         cardlist_list = CardList.objects.all()
    else:
        # find all cardlists which groups match current_user_group_ids OR which users match current_user_id
        # OR which owner match current_user_id
        # http://stackoverflow.com/questions/7740356/logical-or-of-django-many-to-many-queries-returns-duplicate-results
        cardlist_list = CardList.objects.filter(
            Q(groups__in=list(current_user_group_ids)) |
            Q(users__exact=current_user_id) |
            Q(owner__exact=current_user_id)
        ).distinct().order_by('-created_date')

    context = {'cardlist_list': cardlist_list,}
    return render(request, 'cards/cardlist_list.html', context)


def cardlist(request, cardlist_id):
    cardlist = CardList.objects.get(id=cardlist_id)
    cardlist_name = cardlist.cardlist_name
    if not (request.user.is_superuser or request.user.is_staff):
        if cardlist.owner != request.user.id:
            return HttpResponseForbidden()

    cards = Card.objects.filter(cardlist__exact=cardlist_id)
    logger.debug(cards.all)
    context = {'card_list' : cards, 'cardlist_name': cardlist_name}
    return render(request, 'cards/card_list.html', context)

def card(request):
    pass