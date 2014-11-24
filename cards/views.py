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

    if request.user.is_superuser or request.user.is_staff:
         cardlist_list = CardList.objects.all()
    else:
        # find all cardlists which groups match current_user_group_ids OR which users match current_user_id
        # OR which owner match current_user_id
        # http://stackoverflow.com/questions/7740356/logical-or-of-django-many-to-many-queries-returns-duplicate-results
        cardlist_list = CardList.objects.filter(
            Q(groups__in=list(request.user.groups.all())) |
            Q(users__exact=request.user.id) |
            Q(owner__exact=request.user.id)
        ).distinct().order_by('-created_date')

    context = {'cardlist_list': cardlist_list,}
    return render(request, 'cards/cardlist_list.html', context)


def cardlist(request, cardlist_id):
    cardlist = CardList.objects.get(id=cardlist_id)
    cardlist_name = cardlist.cardlist_name


    # Current users permission ids
    cardlist.groups.values_list('id', flat=True)

    has_user_access = CardList.objects.filter(users__exact=request.user.id).filter(id=cardlist_id)
    has_group_access = CardList.objects.filter(groups__in=list(request.user.groups.all())).filter(id=cardlist_id)

    # Check access permissions to this cardlist
    if not (request.user.is_superuser or
        request.user.is_staff or
        cardlist.owner == request.user.id or
        has_user_access or
        has_group_access):
            return HttpResponseForbidden()

    cards = Card.objects.filter(cardlist__exact=cardlist_id)
    logger.debug(cards.all)

    # Check add permissions

    if request.user.has_perm('cards.add_card'):
        show_newcard = True
    else:
        show_newcard = False

    context = {'card_list' : cards,
               'cardlist_name': cardlist_name,
               'cardlist_id': cardlist_id,
               'show_newcard': show_newcard
    }
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