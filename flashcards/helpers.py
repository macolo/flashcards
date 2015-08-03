__author__ = 'mario'

from django.db.models import Q
from models import CardList, CardListUser, CardListGroup


def get_list_of_allowed_cardlists(request, at_least_mode):
    """
    This function returns the cardlists for which the user has a specified access
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