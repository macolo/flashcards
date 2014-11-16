import logging

from django.shortcuts import get_object_or_404, render
from django.http import Http404

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.

from cards.models import CardList

def index(request):
    cardlist_list = CardList.objects.order_by('-created_date')
    context = {'cardlist_list': cardlist_list,}
    return render(request, 'cards/index.html', context)

