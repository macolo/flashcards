# -*- coding: UTF-8 -*-

import logging
from django.shortcuts import render
from social_core.backends.utils import load_backends

from django.conf import settings
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils.http import is_safe_url
from django.shortcuts import resolve_url
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import (REDIRECT_FIELD_NAME, login as auth_login)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from usermgmt.models import UserValidationCode
from usermgmt import signup_form
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.views import login as django_login

# Create your views here.

# Get an instance of a logger
logger = logging.getLogger(__name__)


def login(request):

    if request.user.is_authenticated():
        if request.GET.get('next'):
            return redirect(request.GET.get('next'))
        else:
            return redirect('accounts:profile')

    if request.GET.get('deeplink'):
        message = "Welcome! You must sign in at this point and will then be redirected to the requested page."
        messages.add_message(request, messages.SUCCESS, message)
        logger.debug(message)
    return django_login(request)


@login_required
def profile(request):
    context = {
        'button_action': 'Connect ',
        'password_set': request.user.has_usable_password(),
    }
    return render(request, 'registration/profile.html', context)


def signup(request):

    if request.GET.get('deeplink'):
        message = "You will be redirected to the requested page after signup."
        messages.add_message(request, messages.SUCCESS, message)
        logger.debug(message)

    if request.user.is_authenticated():
        # we wanna log the person out first
        logout(request)

    # This shows the signup form and displays errors
    if request.method == 'POST':
        # This form has been filled in by the user
        form = signup_form.ExtendedUserCreationForm(request.POST)
        if form.is_valid():
            newuser = form.save()
            logger.debug('Created user ' + newuser.email + "& sent email validation")
            # the user needs to undergo email validation first, so we want to create him inactive

            # if the user has been redirected to signup, try to route him back to the page he originally requested.
            send_validation_mail(newuser, request.POST.get('next'))
            # Set a message and redirect to login
            message = "We have sent an activation mail to " + newuser.email + " . Please go have a look at your inbox"
            messages.add_message(request, messages.SUCCESS, message)
            logger.debug(message)
            return redirect('accounts:login')

    else:
        # initial, empty form
        form = signup_form.ExtendedUserCreationForm()

    context = {
        'button_action': 'Sign up with ',
        'form': form,
    }
    return render(request, 'registration/signup.html', context)


from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from config import settings


def send_validation_mail(user, next_url):
    # http://sheeshmohsin.wordpress.com/2014/02/18/send-html-template-email-using-django/
    code = UserValidationCode(user=user)
    code.save()

    plaintext = get_template('registration/email_validation_body.txt')
    htmly = get_template('registration/email_validation_body.html')

    d = {
        'email': user.email,
        'code': code.hash,
        'base_url': settings.BASE_URL,
        'next_url': next_url,
    }

    subject = settings.APP_NAME + " - validate your email address"
    from_email = settings.EMAIL_FROM
    to = user.email
    text_content = plaintext.render(d)
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def validate_email(request, code):
    if request.user.is_authenticated():
        # we wanna log the person out first
        logout(request)
        request.session.flush()

    # This view sets the user to active and logs the user in or renders an error page

    try:
        user_code_combination = UserValidationCode.objects.get(hash=code)
        user = user_code_combination.user
        user.is_active = True
        user.save()
        user_code_combination.delete()
        # Crazy hack: http://stackoverflow.com/questions/15192808/django-automatic-login-after-user-registration-1-4
        user.backend = "django.contrib.auth.backends.ModelBackend"
        auth_login(request, user)
        message = "Welcome to " + settings.APP_NAME + "!"
        messages.add_message(request, messages.SUCCESS, message)
        logger.debug('Validation succeeded - logged in ' + user.email + " - is_authenticated: " + str(
            request.user.is_authenticated()))
        # the user will get next urls in the e-mail link if they came through a deep url (like stack sharing).
        if(request.GET.get('next')):
            return redirect(request.GET.get('next'))
        else:
            return redirect('cards:cardlist_index')

    except UserValidationCode.DoesNotExist:
        message = "This activation code is not valid anymore"
        messages.add_message(request, messages.SUCCESS, message)
        logger.debug(message)
        # Send the user to signup
        return redirect('accounts:signup')


from django.contrib.auth.forms import SetPasswordForm


@login_required()
def set_password(request):
    # This shows the signup form and displays errors
    if request.method == 'POST':
        # This form has been filled in by the user
        form = SetPasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            logger.debug('Set password for ' + request.user.email)
            # Set a message and redirect

            # Django logs the user out after successful password set :( WTF
            # Crazy hack: http://stackoverflow.com/questions/15192808/django-automatic-login-after-user-registration-1-4
            request.user.backend = "django.contrib.auth.backends.ModelBackend"
            auth_login(request, request.user)
            message = "Your password has been set!"
            messages.add_message(request, messages.SUCCESS, message)
            logger.debug(message)
            return redirect('accounts:profile')

    else:
        # initial, empty form
        form = SetPasswordForm(user=request.user)

    context = {
        'form': form,
    }
    return render(request, 'registration/password_set_form.html', context)
