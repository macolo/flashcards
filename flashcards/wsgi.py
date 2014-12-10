"""
WSGI config for flashcards project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flashcards.settings")

from django.core.wsgi import get_wsgi_application

def application(environ, start_response):
    # pass the WSGI environment variables on through to os.environ
    for key in environ:
        if key.startswith('ME_FLASHCARDS_'):
            os.environ[key] = environ[key]
    _application = get_wsgi_application()
    return _application(environ, start_response)