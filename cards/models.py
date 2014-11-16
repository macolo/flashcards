from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.

class CardList(models.Model):
    cardlist_name = models.CharField(max_length=200)
    # related_name is needed because otherwise this clashes with the m2m from users below
    owner = models.ForeignKey(User, related_name="owner")
    users = models.ManyToManyField(User, blank=True)
    groups = models.ManyToManyField(Group, blank=True)
    created_date = models.DateTimeField('date published', auto_now_add=True)

    def __unicode__(self):
        return self.cardlist_name


class Card(models.Model):
    cardlist = models.ManyToManyField(CardList)
    created_date = models.DateTimeField('date published', auto_now_add=True)
    card_question = models.CharField(max_length=200)
    card_answer = models.CharField(max_length=200)


    def __unicode__(self):
        return self.card_question