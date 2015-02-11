# -*- coding: UTF-8 -*-

import logging

from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseServerError
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
from django.contrib import messages
from flashcards import settings

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.
import datetime
from django.shortcuts import redirect

from cards.models import CardList, Card, CardListGroup, CardListUser, ShareCardList


@login_required
def cardlist_index(request):
    # let' retrieve all the cardlists where the user has at least 'r' (read) access
    # this includes lists with 'cr' (read and create) and 'crud' (full) access.
    cardlist_list = get_list_of_allowed_cardlists(request, 'r')

    if not cardlist_list.exists():
        message = "You haven't got any card stacks! " \
                  "How about creating one?"
        logger.debug(request.user.get_username()+" has no stacks.")
        messages.add_message(request, messages.INFO, message)


    context = {'cardlist_list': cardlist_list, }
    return render(request, 'cards/cardlist_list.html', context)


@login_required
def create_cardlist(request):
    try:
        cardlist_name = request.POST['cardlist_name']
    except StandardError:
        return redirect('cards:cardlist_index')

    if cardlist_name == "":
        message = 'Cannot create a stack with empty name. Please type in a name.'
        logger.warning(message)
        messages.add_message(request, messages.WARNING, message)
    else:
        # write the new (empty) card list to the database
        new_cardlist = CardList(cardlist_name=cardlist_name, owner_id=request.user.id)
        new_cardlist.save()
        message = 'Created a new stack!'
        logger.debug(message)
        messages.add_message(request, messages.SUCCESS, message)

    # Then redirect back to the index
    return redirect('cards:cardlist_index')


@login_required
def cardlist(request, cardlist_id):

    # hmm django checks arguments in as strings, however this needs to be compared to a number in the template later on
    cardlist_id = int(cardlist_id)

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

    _cards = cardlist.cards.all().order_by('-created_date')

    # # show a special 'new' tag if the card has been created / edited <24h from now
    cards = [];
    now = timezone.now()
    for c in _cards:
        created = c.created_date
        timediff = (now - created)
        timediff_in_min = timediff.total_seconds() / 60
        max_timediff_in_min = 1440
        if timediff_in_min < max_timediff_in_min:
            # This card is 'recent'!
            c.is_new = True
        cards.append(c)

    # Flag for the template that decides whether UI for add new card should be visible
    show_newcard = False
    can_delete = False

    if is_owner or request.user.is_superuser or request.user.is_staff:
        show_newcard = True
        can_delete = True

    if user_and_group_access:
        if user_and_group_access == 'crud':
            show_newcard = True
        elif user_and_group_access == 'cr':
            show_newcard = True


    # This gets us all cardlists where a user can read and create cards (and above)
    # This is needed in order to display a list of cardlists the user can copy a card to.
    _modifiable_cardlists = get_list_of_allowed_cardlists(request, 'cr')

    # remove active cardlist
    modifiable_cardlists = []
    modifiable = False
    for cl in _modifiable_cardlists:
        if cl.id != cardlist_id:
            modifiable_cardlists.append(cl)
        else:
            modifiable = True


    context = {'card_list': cards,
               'cardlist_name': cardlist_name,
               'cardlist_id': cardlist_id,
               'show_newcard': show_newcard,
               'can_delete': can_delete,
               'can_share' : can_delete,
               'modifiable': modifiable,
               'modifiable_cardlists': modifiable_cardlists,
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

    for po in CardListGroup.objects.filter(cardlist__pk=cardlist_id,
                                           groups__in=list(request.user.groups.all())).distinct():
        modes.append(po.mode)

    # If there aren't any access records it means that there is no access at all.
    if not modes:
        return False

    # Iterates over a list and finds the highest access level
    trumping_access_level = 'r'
    for mode in modes:
        # if it is the highest permission, we can return right away
        if mode == 'crud':
            return mode
        # if its the perm in between, there might later on still be a higher permission
        elif mode == 'cr':
            trumping_access_level = mode
    # we can now safely use the highest perm. At this point it is either 'cr' or it stayed 'r'
    return trumping_access_level


@login_required
def create_card(request, cardlist_id):
    # Here we will store the new card
    try:
        question = request.POST['card_question']
        answer = request.POST['card_answer']
    except(StandardError):
        error_msg = 'Post request for card creation is lacking mandatory values.'
        logger.error(error_msg)
        context = {'error_msg': error_msg}
        return render(request, 'cards/card_list.html', context)

    current_cardlist = CardList.objects.get(pk=cardlist_id)

    # we have take care here that we don't add duplicates within one card list and to the database
    # if the question exists in db however is not added yet to the card list, add that one
    # if the question exists in db and is already added to the card list, do nothing

    existing_card_in_db = Card.objects.filter(card_question=question)
    existing_card_in_cardlist = current_cardlist.cards.filter(card_question=question)
    if existing_card_in_db:
        if existing_card_in_cardlist:
            # do nothing
            messages.add_message(request, messages.INFO, 'A card like this is already part of this stack!')
            logger.error('A card like this is already part of this stack!')
            return redirect('cards:cardlist', cardlist_id)
        if not existing_card_in_cardlist:
            # add card from db, there shouldnt be multiple cards with the same question in the DB (hopefully)
            newcard = existing_card_in_db[0]
            logger.error('Found an existing card in the DB and added it!')
    else:
        # nothing found, create card
        newcard = Card.objects.create(card_question=question, card_answer=answer)
        newcard.save()
    current_cardlist.cards.add(newcard)
    messages.add_message(request, messages.SUCCESS, 'Your card has been added to this stack!')

    # Then redirect to the active cardlist
    return redirect('cards:cardlist', cardlist_id)

def copycardto(request, original_cardlist_id, new_cardlist_id, card_id):

    card = Card.objects.get(pk=card_id)
    cardlist = CardList.objects.get(pk=new_cardlist_id)

    if cardlist.owner.pk == request.user.id:
        is_owner = True
    else:
        is_owner = False

    user_and_group_access = get_user_and_group_access_level(request, new_cardlist_id)

    # Check access permissions to this stack, if either one of the conditions is true
    # allow access.
    if not (request.user.is_superuser or
                request.user.is_staff or
                is_owner or
                user_and_group_access == 'cr' or
                user_and_group_access == 'crud'):
        return HttpResponseForbidden()

    cardlist.cards.add(card)
    message = 'Added '+card.card_question+' to '+cardlist.cardlist_name+'!'
    messages.add_message(request, messages.SUCCESS, message)
    logger.debug(message)

    # Then redirect to the active cardlist
    return redirect('cards:cardlist', original_cardlist_id)



@login_required
def delete_cardlist(request, cardlist_id):
    cardlist = CardList.objects.get(id=cardlist_id)
    # we need to find out whether the current user is allowed to delete!
    # this is the case if the user is the owner, staff, superuser or if either group or user mode is 'crud'

    if cardlist.owner.pk == request.user.id:
        is_owner = True
    else:
        is_owner = False

    # Check access permissions to this stack, if either one of the conditions is true
    # allow access.
    if request.user.is_superuser or is_owner:
        messages.add_message(request, messages.INFO, 'The stack has been deleted.')
        cardlist.delete()
    else:
        messages.add_message(request, messages.ERROR, 'You are not allowed to delete this stack!')

        # Then redirect to the active cardlist
    return redirect('cards:cardlist_index')


@login_required
def remove_cardlist(request, cardlist_id):
    """
    Of course a cardlist can only be removed if it is in the list of the user
    and that only happens if there is user or group level access, or the user is the owner of the cardlist
    :param request:
    :param cardlist_id:
    :return:
    """

    cardlist = CardList.objects.get(id=cardlist_id)
    clgs = CardListGroup.objects.filter(groups__in=list(request.user.groups.all()),cardlist_id=cardlist_id)
    clus = CardListUser.objects.filter(users__exact=request.user.id,cardlist_id=cardlist_id)

    if request.user.is_staff or request.user.is_superuser:
        message = "Sorry, as a staff member you're damned to see everything. With great power comes great responsibility."
        messages.add_message(request, messages.WARNING, message)
        logger.debug(message)

    if cardlist.owner.pk == request.user.id:
        # The owner cannot remove his stacks from his list
        message = 'You cannot remove a stack of cards from your stacks if you are its owner.'
        messages.add_message(request, messages.WARNING, message)
        logger.debug(message)

    if clgs:
        # We have group access and can' do anything about it
        # Let' delete user access just in case, so the group access could be removed manually
        clus.delete()
        message = "You have access to this list through your membership to the group(s) "+\
                  ', '.join([clg.groups.name for clg in clgs])\
                  +". As long as you maintain this membership we cannot remove this stack."
        messages.add_message(request, messages.WARNING, message)
        logger.debug(message)

    if clus:
        # Finally we can work with user access and remove the user
        # There should only be one entry but you can never be sure
        clus.delete()
        message = "You won't be troubled again by this stack. We have removed it from your stacks."
        messages.add_message(request, messages.WARNING, message)
        logger.debug(message)
        # redirect to the cardlist index
        return redirect('cards:cardlist_index')

    # Then redirect to the active cardlist
    return redirect('cards:cardlist', cardlist_id)


@login_required
def share_cardlist(request, cardlist_id):
    cardlist = CardList.objects.get(id=cardlist_id)
    scl = ShareCardList.objects.filter(cardlist_id=cardlist_id)
    if scl:
        secret = scl[0].secret
    else:
        scl = ShareCardList(cardlist=cardlist)
        scl.save()
        secret = scl.secret
    context = {
        'base_url': settings.BASE_URL,
        'secret': secret,
        'cardlist_id': cardlist_id,
    }
    return render(request, 'cards/cardlist_share.html', context)

@login_required
def import_cardlist(request, secret):
    # Find out which cardlist is to be imported, there should be only one as per model
    # We need the name anyway
    scl = ShareCardList.objects.get(secret=secret)
    context = {
        "secret": secret,
        "cardlist_name": scl.cardlist.cardlist_name,
    }
    return render(request, 'cards/cardlist_share_confirm.html', context)

@login_required
def import_cardlist_confirmed(request, secret):
    """
    We have to drag the secret along
    :param request:
    :param cardlist_id:
    :param secret:
    :return:
    """

    scl = ShareCardList.objects.get(secret=secret)

    # Is there already a user access set?
    access = get_user_and_group_access_level(request, scl.cardlist.id)
    # existing_clu = CardListUser.objects.filter(users=request.user, cardlist=scl.cardlist)

    if access:
        # Set a message to confirm
        message = 'You already have access to "'+scl.cardlist.cardlist_name+'".'
        messages.add_message(request, messages.SUCCESS, message)
        logger.debug(message)
    else:
        # Now add user level access to this cardlist, in read only mode
        clu = CardListUser(users=request.user,cardlist=scl.cardlist,mode='r')
        clu.save()

        # Set a message to confirm
        message = 'The stack  "'+scl.cardlist.cardlist_name+'" has been added to your stacks.'
        messages.add_message(request, messages.SUCCESS, message)
        logger.debug(message)

    # Then redirect to the active cardlist
    return redirect('cards:cardlist', scl.cardlist.id)


@login_required
def get_list_of_allowed_cardlists(request, at_least_mode):
    """
    This function returns the cardlists for wich the user has a specified access
    :param request: the django request object, containing user
    :param at_least_mode: the lowest mode from CardListUser or CardListGroup, either 'r', 'cr' or 'crud'
    :return: a list of cardlist
    """

    if request.user.is_superuser:
        cardlist_list = CardList.objects.all()
        return cardlist_list
    else:
        # find all cardlists which groups match current_user_group_ids OR which users match current_user_id
        # OR which owner match current_user_id
        # http://stackoverflow.com/questions/7740356/logical-or-of-django-many-to-many-queries-returns-duplicate
        # -results
        cardlist_list = CardList.objects.filter(
            Q(groups__in=list(request.user.groups.all())) | Q(users__exact=request.user.id) |
            Q(owner__exact=request.user.id)).distinct().order_by('-created_date')
        # This returns all cardlists, because 'r' is the lowest access level.
        if at_least_mode == 'r':
            return cardlist_list
        else:
            # Let' retrieve the highest mode for cardlists the user has access to:
            cardlist_list_filtered_by_mode = []
            for cl in cardlist_list:
                # first check if user is owner:
                if cl.owner == request.user:
                    cardlist_list_filtered_by_mode.append(cl)
                    # only add a cl to the stack once.
                    continue
                # this gets us the highest access level for that cardlist
                trumping_mode = get_user_and_group_access_level(request, cl.id)
                # it needs to be equal or higher than 'cr' OR equal than 'crud'
                if (at_least_mode == 'cr' and (trumping_mode == 'cr' or trumping_mode == 'crud')) or \
                        (at_least_mode == 'crud' and trumping_mode == 'crud'):
                    cardlist_list_filtered_by_mode.append(cl)
                    # only add a cl to the stack once. This is to prevent future bugs.
                    continue

            return cardlist_list_filtered_by_mode

@login_required
def update_card(request, card_id):
    # this is a async endpoint
    # meaning it does not return any rendered HTML
    if request.method =='POST':
        try:
            question = request.POST['question']
            answer = request.POST['answer']
        except KeyError:
            return HttpResponseServerError()

        card = Card.objects.get(pk=card_id)
        card.card_question = question
        card.card_answer = answer
        card.save()

        # all ok
        return HttpResponse()


    else:
        return HttpResponseServerError()


@login_required
def card(request):
    pass