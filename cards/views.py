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

from cards.models import CardList, Card, CardListGroup, CardListUser


@login_required
def cardlist_index(request):

    if request.user.is_superuser:
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

@login_required
def new_cardlist(request):
    try:
        cardlist_name = request.POST['cardlist_name']
    except(StandardError):
        error_msg = 'Post request for card creation is lacking mandatory values.'
        logger.error(error_msg)
        context = {'error_msg' : error_msg}
        return render(request, 'cards/card_list.html', context)

    # write the new (empty) card list to the database
    new_cardlist = CardList(cardlist_name=cardlist_name, owner_id=request.user.id)
    new_cardlist.save()

    # Then redirect to the active cardlist
    return redirect('cards:cardlist_index')


@login_required
def cardlist(request, cardlist_id):
    cardlist = CardList.objects.get(id=cardlist_id)
    cardlist_name = cardlist.cardlist_name

    # Check user & group permissions for the card deck
    # The higher permissions trump the lower
    # a group the user is a member of can have 'r' and the user itself can have 'ru'
    # owner or admin always wins.
    user_and_group_access = get_user_and_group_access_level(request, cardlist_id)

    if cardlist.owner.pk == request.user.id:
        is_owner = True
    else:
        is_owner = False

    # Check access permissions to this stack, if either one of the conditions is true
    # allow access.
    if not (request.user.is_superuser or
        request.user.is_staff or
        is_owner or
        user_and_group_access):
            return HttpResponseForbidden()

    cards = cardlist.cards.all()
    logger.debug(cards.all)


    # Flag for the template that decides whether UI for add new card should be visible
    show_newcard = False
    show_cardlist_crud = False

    if is_owner or request.user.is_superuser or request.user.is_staff:
        show_newcard = True
        show_cardlist_crud = True

    if user_and_group_access:
        if user_and_group_access=='crud' or user_and_group_access=='cr':
            show_newcard = True
            show_cardlist_crud = True

    context = {'card_list' : cards,
               'cardlist_name': cardlist_name,
               'cardlist_id': cardlist_id,
               'show_newcard': show_newcard,
               'show_cardlist_crud': show_cardlist_crud,
    }
    return render(request, 'cards/card_list.html', context)



@login_required
def get_user_and_group_access_level(request, cardlist_id):
    """

    :param cardlist_id: the id of the current cardlist
    :return: the highest access level the current user has access to either to his group or user access
    """
    modes = []
    for po in CardListUser.objects.filter(cardlist__pk=cardlist_id, users__pk=request.user.id).distinct():
        modes.append(po.mode)

    for po in CardListGroup.objects.filter(cardlist__pk=cardlist_id, groups__in=list(request.user.groups.all())).distinct():
        modes.append(po.mode)

    # Iterates over a list and finds the highest access level
    trumping_access_level = 'r'
    for mode in modes:
        # if it is the highest permission, we can return right away
        if mode == 'crud':
            return trumping_access_level
        # if its the perm in between, there might later on still be a higher permission
        elif mode == 'cr':
            trumping_access_level = mode
    # we can now safely use the highest perm. At this point it is either 'cr' or it stayed 'r'
    return trumping_access_level


@login_required
def add_card_to_cardlist(request, cardlist_id):
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
    current_cardlist.cards.add(newcard)
    newcard.save()

    # Then redirect to the active cardlist
    return redirect('cards:cardlist', cardlist_id)

@login_required
def delete_cardlist(request, cardlist_id):
    cardlist = CardList.objects.filter(id=cardlist_id)
    cardlist.delete()

     # Then redirect to the active cardlist
    return redirect('cards:cardlist_index')


@login_required
def card(request):
    pass