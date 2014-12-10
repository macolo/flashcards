"""
Django settings for flashcards project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

from django.conf import settings

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['ME_FLASHCARDS_SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['flashcards.typodrive.com', 'www.mercedes-espanol.ch']


# Application definition

INSTALLED_APPS = (
    'django_extensions',
    'usermgmt', # before django.contrib.admin because of
    # http://stackoverflow.com/questions/447512/how-do-i-override-djangos-administrative-change-password-page
    'django.contrib.admin',
    'django.contrib.auth',
    'social.apps.django_app.default',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'cards',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'flashcards.urls'

WSGI_APPLICATION = 'flashcards.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['ME_FLASHCARDS_DB_NAME'],
        'USER': os.environ['ME_FLASHCARDS_DB_USER'],
        'PASSWORD': os.environ['ME_FLASHCARDS_DB_PASSWORD'],
        'HOST': os.environ['ME_FLASHCARDS_DB_HOST'],
        'PORT': os.environ['ME_FLASHCARDS_DB_PORT'],
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

# where static files will be available over http
STATIC_URL = '/flashcards/static/'

# where static files will be copied to
STATIC_ROOT = '/var/www/flashcards/static/'

LOGGING = {
    'disable_existing_loggers': False,
    'version': 1,
    'handlers': {
        'console': {
            # logging handler that outputs log messages to terminal
            'class': 'logging.StreamHandler',
            'level': 'DEBUG', # message level to be written to console
        },
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'logfile': {
            'level':'WARNING',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR + "/logfile.log",
            'maxBytes': 50000,
            'backupCount': 2,
        },
    },
    'loggers': {
        '': {
            # this sets root level logger to log debug and higher level
            # logs to console. All other loggers inherit settings from
            # root level logger.
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
            'propagate': False, # this tells logger to send logging message
                                # to its parent (will send if set to True)
        },
        # http://stackoverflow.com/questions/7768027/turn-off-sql-logging-while-keeping-settings-debug
        'django.db.backends': {
            'handlers': ['null'],  # Quiet by default!
            'propagate': False,
            'level':'DEBUG',
            },
    },
}

LOGIN_REDIRECT_URL = "cards:cardlist_index"

# this is the name for the login page from flashcards/urls.py
LOGIN_URL = 'login'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TEMPLATE_CONTEXT': True,
}

# needed for python social auth
AUTHENTICATION_BACKENDS = settings.AUTHENTICATION_BACKENDS +  (
    'social.backends.google.GoogleOAuth2',
    'social.backends.facebook.FacebookOAuth2',
)

# needed for python social auth
# http://psa.matiasaguirre.net/docs/configuration/django.html
TEMPLATE_CONTEXT_PROCESSORS = settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
)

# needed for python social auth
SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['username', 'first_name', 'email']

# needed for python social auth
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ['ME_FLASHCARDS_SOCIAL_AUTH_GOOGLE_OAUTH2_KEY']
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ['ME_FLASHCARDS_SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET']
SOCIAL_AUTH_GOOGLE_OAUTH2_AUTH_EXTRA_ARGUMENTS = {'access_type': 'offline'}
SOCIAL_AUTH_GOOGLE_OAUTH2_REQUEST_TOKEN_EXTRA_ARGUMENTS = {'access_type': 'offline'}

SOCIAL_AUTH_FACEBOOK_KEY = os.environ['ME_FLASHCARDS_SOCIAL_AUTH_FB_OAUTH2_KEY']
SOCIAL_AUTH_FACEBOOK_SECRET = os.environ['ME_FLASHCARDS_SOCIAL_AUTH_FB_OAUTH2_SECRET']
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']

# unique e-mail addresses:
# http://stackoverflow.com/questions/19273904/how-to-have-unique-emails-with-python-social-auth
# http://django-social-auth.readthedocs.org/en/latest/pipeline.html
SOCIAL_AUTH_PIPELINE = (
    # Get the information we can about the user and return it in a simple
    # format to create the user instance later. On some cases the details are
    # already part of the auth response from the provider, but sometimes this
    # could hit a provider API.
    'social.pipeline.social_auth.social_details',

    # Get the social uid from whichever service we're authing thru. The uid is
    # the unique identifier of the given user in the provider.
    'social.pipeline.social_auth.social_uid',

    # Verifies that the current auth process is valid within the current
    # project, this is were emails and domains whitelists are applied (if
    # defined).
    'social.pipeline.social_auth.auth_allowed',

    # Checks if the current social-account is already associated in the site.
    'social.pipeline.social_auth.social_user',

    # Make up a username for this person, appends a random string at the end if
    # there's any collision.
    'social.pipeline.user.get_username',

    # Send a validation email to the user to verify its email address.
    # Disabled by default.
    # 'social.pipeline.mail.mail_validation',

    # Associates the current social details with another user account with
    # a similar email address. Disabled by default.
    'social.pipeline.social_auth.associate_by_email',

    # Create a user account if we haven't found one yet.
    'social.pipeline.user.create_user',

    # Create the record that associated the social account with this user.
    'social.pipeline.social_auth.associate_user',

    # Populate the extra_data field in the social record with the values
    # specified by settings (and the default ones like access_token, etc).
    'social.pipeline.social_auth.load_extra_data',

    # Update the user record with any changed info from the auth service.
    'social.pipeline.user.user_details'
)
