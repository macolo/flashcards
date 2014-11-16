import logging

from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.

from cards.models import CardList

@login_required
def index(request):
    cardlist_list = CardList.objects.order_by('-created_date')
    context = {'cardlist_list': cardlist_list,}
    return render(request, 'cards/index.html', context)


def cardlist(request):
    pass

def card(request):
    pass