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

    user_access = CardListUser.objects.filter(cardlist__pk=cardlist_id, users__pk=request.user.id).distinct()
    group_access = CardListGroup.objects.filter(cardlist__pk=cardlist_id, groups__in=list(request.user.groups.all())).distinct()

    if cardlist.owner.pk == request.user.id:
        is_owner = True
    else:
        is_owner = False

    # Check access permissions to this stack, if either one of the conditions is true
    # allow access.
    if not (request.user.is_superuser or
        request.user.is_staff or
        is_owner or
        user_access or
        group_access):
            return HttpResponseForbidden()

    cards = cardlist.cards.all()
    logger.debug(cards.all)


    # Check permissions for the card deck
    # The higher permissions trump the lower
    # a group the user is a member of can have 'r' and the user itself can have 'ru'
    # owner or admin always wins.

    permissions = get_access_levels_from_cardlist_queryset(user_access)
    permissions += get_access_levels_from_cardlist_queryset(group_access)



    highest_perm = get_trumping_access_level(permissions)


    if is_owner or highest_perm=='crud' or highest_perm=='cr':
        show_newcard = True
    else:
        show_newcard = False

    context = {'card_list' : cards,
               'cardlist_name': cardlist_name,
               'cardlist_id': cardlist_id,
               'show_newcard': show_newcard
    }
    return render(request, 'cards/card_list.html', context)

def get_access_levels_from_cardlist_queryset(queryset):
    permissions = []
    for query in queryset:
        permissions.append(query.mode)
    return permissions

def get_trumping_access_level(perms):
    """
    Iterates over a list and finds the highest access level
    :return: highest access level as a string (either 'r', 'rc' or 'crud')
    """
    highest_perm_so_far = 'r'
    for perm in perms:
        # if it is the highest permission, we can return right away
        if perm == 'crud':
            return perm
        # if its the perm in between, there might later on still be a higher permission
        elif perm == 'cr':
            highest_perm_so_far = perm
    # we can now safely return the highest perm. At this point it is either 'cr' or it stayed 'r'
    return highest_perm_so_far

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
    current_cardlist.cards.add(newcard)
    newcard.save()

    # Then redirect to the active cardlist
    return redirect('cards:cardlist',cardlist_id)

def card(request):
    pass