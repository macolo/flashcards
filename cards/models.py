from django.db import models
from django.contrib.auth.models import User, Group
import uuid

# Create your models here.

class Card(models.Model):
    created_date = models.DateTimeField('date published', auto_now_add=True)
    card_question = models.CharField(max_length=200, blank=False)
    card_answer = models.CharField(max_length=200, blank=False)

    def __unicode__(self):
        return self.card_question + " - " + self.card_answer

class CardList(models.Model):
    cardlist_name = models.CharField(max_length=200)
    # related_name is needed because otherwise this clashes with the m2m from users below
    users = models.ManyToManyField(User, through="CardListUser")
    groups = models.ManyToManyField(Group, through="CardListGroup")
    owner = models.ForeignKey(User, related_name="owner")
    created_date = models.DateTimeField('date published', auto_now_add=True)
    cards = models.ManyToManyField(Card, related_name="cards", blank=True)


    def __unicode__(self):
        return self.cardlist_name

class CardListUser(models.Model):
    MODES = (('r', 'Read'), ('cr', 'Read, Create'), ('crud', 'Full'))
    cardlist = models.ForeignKey(CardList)
    users = models.ForeignKey(User)
    mode = models.CharField(max_length=4, default='r', choices=MODES)

    def __unicode__(self):
        # This is to have a nice title for the record in the admin interface
        beautiful_mode = dict(self.MODES).get(self.mode)
        return 'User "' + self.users.__unicode__() + '" has '+ beautiful_mode + ' access on "'+ self.cardlist.__unicode__() + '"'

    def set_mode_to_read(self):
        self.mode = self.MODES[0][0]

    def set_mode_to_readcreate(self):
        self.mode = self.MODES[1][0]

    def set_mode_to_crud(self):
        self.mode = self.MODES[2][0]

class CardListGroup(models.Model):

    MODES = (('r', 'read'), ('cr', 'create and read'), ('crud', 'create, read, update and delete'))
    cardlist = models.ForeignKey(CardList)
    groups = models.ForeignKey(Group)
    mode = models.CharField(max_length=4, default='r', choices=MODES)

    def __unicode__(self):
        # This is to have a nice title for the record in the admin interface
        beautiful_mode = dict(self.MODES).get(self.mode)
        return 'Group "' + self.groups.__unicode__() + '" has '+ beautiful_mode + ' access on "'+ self.cardlist.__unicode__() + '"'

    def set_mode_to_read(self):
        self.mode = self.MODES[0][0]

    def set_mode_to_readcreate(self):
        self.mode = self.MODES[1][0]

    def set_mode_to_crud(self):
        self.mode = self.MODES[2][0]

def generate_random_hash():
    return uuid.uuid1().hex

class ShareCardList(models.Model):
    cardlist = models.ForeignKey(CardList)
    secret = models.CharField(max_length=200,default=generate_random_hash,unique=True)
    created_date = models.DateTimeField('date published', auto_now_add=True)

    def __unicode__(self):
        return self.cardlist.cardlist_name