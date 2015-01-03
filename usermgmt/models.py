from django.db import models
from django.contrib.auth.models import User, Group
import uuid
from binascii import hexlify

# Create your models here.

# This stores the hashes for email validation
class UserValidationCode(models.Model):
    created_date = models.DateTimeField('date published', auto_now_add=True)
    user = models.ForeignKey(User)
    # The hash is unique and auto-generated for an existing user
    hash = models.CharField(max_length=200, blank=True, default=uuid.uuid1().hex, editable=False)

    def get_user_name(self):
        return self.user.username

    def get_user_email(self):
        return self.user.email

    def __unicode__(self):
        return self.user.username