"""
WSGI config for flashcards project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

# https://github.com/jpadilla/django-dotenv
import os
import dotenv
dotenv.read_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

from django.core.wsgi import get_wsgi_application
import config.settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# only if not locally executed
if not config.settings.LOCAL:

    # Activate the virtual env
    activate_virtual_env_path = config.settings.require_env('ME_VIRTUALENV_ACTIVATE_THIS_PATH')
    with open(activate_virtual_env_path) as f:
        code = compile(f.read(), activate_virtual_env_path, 'exec')
        exec(code)

application = get_wsgi_application()
