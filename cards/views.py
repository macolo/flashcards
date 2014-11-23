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

from django.shortcuts import redirect

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
    context = {'card_list' : cards, 'cardlist_name': cardlist_name, 'cardlist_id': cardlist_id}
    return render(request, 'cards/card_list.html', context)

def add_cart_to_cardlist(request, cardlist_id):
    # Here we will store the new card
    try:
        question = request.POST['card_question']
        answer = request.POST['card_answer']
    except(StandardError):

        error_msg = 'Post request for card creation is lacking mandatory values.'
        logger.error(error_msg)
        context = {'error_msg' : error_msg}
        return render(request, 'cards/card_list.html', context)

    current_cardlist = CardList.objects.get(pk=cardlist_id)
    newcard = Card.objects.create(card_question=question,card_answer=answer)
    newcard.cardlist.add(current_cardlist)
    newcard.save()

    # Then redirect to the active cardlist
    return redirect('cards:cardlist',cardlist_id)

def card(request):
    pass