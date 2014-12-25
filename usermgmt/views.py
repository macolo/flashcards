# -*- coding: UTF-8 -*-

import logging
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from social.backends.utils import load_backends

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
from django.contrib.auth.models import User, Group
from usermgmt.models import UserValidationCode
from usermgmt import signup_form
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

# Get an instance of a logger
logger = logging.getLogger(__name__)

@login_required
def profile(request):
    context = {
        'available_backends': load_backends(settings.AUTHENTICATION_BACKENDS),
        'button_action': 'Connect ',
        'password_set_or_reset': request.user.has_usable_password(),
    }
    return render(request, 'registration/profile.html', context)



def signup(request):

    if request.user.is_authenticated():
        # we wanna log the person out first
        logout(request)

    # This shows the signup form and displays errors
    if request.method =='POST':
        # This form has been filled in by the user
        form = signup_form.ExtendedUserCreationForm(request.POST)
        if form.is_valid():
            newuser = form.save()
            logger.debug('Created user '+newuser.email+"& sent email validation")
            # the user needs to undergo email validation first, so we want to create him inactive

            send_validation_mail(newuser)
            # Set a message and redirect to login
            message = "We have sent an activation mail to "+newuser.email+" . Please go have a look at your inbox"
            messages.add_message(request, messages.SUCCESS, message)
            logger.debug(message)
            return redirect('accounts:login')

    else:
        # initial, empty form
        form = signup_form.ExtendedUserCreationForm()

    context = {
        'available_backends': load_backends(settings.AUTHENTICATION_BACKENDS),
        'button_action': 'Sign up with ',
        'form': form,
    }
    return render(request, 'registration/signup.html', context)


from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from flashcards import settings

def send_validation_mail(user):
    # http://sheeshmohsin.wordpress.com/2014/02/18/send-html-template-email-using-django/
    code = UserValidationCode(user=user)
    code.save()

    plaintext = get_template('registration/email_validation_body.txt')
    htmly     = get_template('registration/email_validation_body.html')

    d = Context({ 'email': user.email,
                  'code': code.hash,
                  'base_url': settings.BASE_URL,
                  })

    subject = settings.APP_NAME+" - validate your email address"
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
        message = "Welcome to "+settings.APP_NAME+"!"
        messages.add_message(request, messages.SUCCESS, message)
        logger.debug('Validation succeeded - logged in '+user.email+" - is_authenticated: "+str(request.user.is_authenticated()))
        return redirect('cards:cardlist_index')

    except UserValidationCode.DoesNotExist:
        message = "This activation code is not valid anymore"
        messages.add_message(request, messages.SUCCESS, message)
        logger.debug(message)
        # Send the user to signup
        return redirect('accounts:signup')



# copied from https://github.com/django/django/blob/master/django/contrib/auth/views.py
# so we can patch around and add python social auth context
@sensitive_post_parameters()
@csrf_protect
@never_cache
def login(request, template_name='registration/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm,
          current_app=None, extra_context=None):
    """
    Displays the login form and handles the login action.
    """

    if request.user.is_authenticated():
        # we wanna go to somewhere else, like profile
        return redirect('accounts:profile')

    redirect_to = request.POST.get(redirect_field_name,
                                   request.GET.get(redirect_field_name, ''))

    if request.method == "POST":
        form = authentication_form(request, data=request.POST)
        if form.is_valid():

            # Ensure the user-originating redirection url is safe.
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

            # Okay, security check complete. Log the user in.
            auth_login(request, form.get_user())

            return HttpResponseRedirect(redirect_to)
    else:
        form = authentication_form(request)

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
        'available_backends': load_backends(settings.AUTHENTICATION_BACKENDS),
        'button_action': 'Log in with '
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)

