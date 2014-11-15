from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class CardList(models.Model):
    cardlist_name = models.CharField(max_length=200)
    user = models.ForeignKey(User)
    created_date = models.DateTimeField('date published')

    def __unicode__(self):
        return self.cardlist_name


class Card(models.Model):
    cardlist = models.ForeignKey(CardList)
    created_date = models.DateTimeField('date published')
    card_question = models.CharField(max_length=200)
    card_answer = models.CharField(max_length=200)


    def __unicode__(self):
        return self.card_question