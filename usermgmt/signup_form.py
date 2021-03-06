# -*- coding: UTF-8 -*-

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


# This code is from https://gist.github.com/fohlin/771052

class UniqueUserEmailField(forms.EmailField):
    """
    An EmailField which only is valid if no User has that email.
    """
    def validate(self, value):
        super(forms.EmailField, self).validate(value)
        try:
            User.objects.get(email = value)
            raise forms.ValidationError("Email already exists")
        except User.MultipleObjectsReturned:
            raise forms.ValidationError("Email already exists")
        except User.DoesNotExist:
            pass
 
 
class ExtendedUserCreationForm(UserCreationForm):
    """
    Extends the built in UserCreationForm in several ways:
    
    * Adds an email field, which uses the custom UniqueUserEmailField,
      that is, the form does not validate if the email address already exists
      in the User table.
    * The username field is generated based on the email, and isn't visible.
    * Data not saved by the default behavior of UserCreationForm is saved.
    """

    email = UniqueUserEmailField(required=True, label='Email address')
    username = forms.CharField(required=False, max_length=30)

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        """
        Changes the order of fields, and removes the username field.
        """
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields.pop('username')

    def clean(self, *args, **kwargs):
        """
        Normal cleanup + username generation.
        """
        cleaned_data = super(UserCreationForm, self).clean(*args, **kwargs)
        if 'email' in cleaned_data:
            cleaned_data['username'] = cleaned_data['email']
        return cleaned_data
        
    def save(self):
        """
        Saves the email, first_name and last_name properties, after the normal
        save behavior is complete.
        """
        user = super(UserCreationForm, self).save(commit=False)
        if user:
            user.username = self.cleaned_data['email']
            user.email = self.cleaned_data['email']
            user.set_password(self.cleaned_data['password1'])
            user.is_active = False
            user.save()
        return user
