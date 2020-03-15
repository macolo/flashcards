from django.db import models
from django.contrib.auth.models import User, Group
import uuid
from binascii import hexlify

# Create your models here.

# I don' like this, would rather have this in the model class but heck...
# http://stackoverflow.com/questions/3573834/django-fields-default-value-from-self-models-instances
def generate_random_hash():
    return uuid.uuid1().hex

# This stores the hashes for email validation
class UserValidationCode(models.Model):
    created_date = models.DateTimeField('date published', auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    # The hash is unique and auto-generated for an existing user
    hash = models.CharField(max_length=200, blank=True, default=generate_random_hash, editable=False, unique=True)

    def get_user_name(self):
        return self.user.username

    def get_user_email(self):
        return self.user.email

    def __str__(self):
        return self.user.username

