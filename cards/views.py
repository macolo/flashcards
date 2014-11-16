from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from cards.models import CardList

def index(request):
    cardlists = CardList.objects.order_by('-')


    return HttpResponse("Hello, world. You're at the polls index.")