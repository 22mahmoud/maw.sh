"""
WSGI config for core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from config.env import BASE_DIR, env

env.read_env(os.path.join(BASE_DIR, ".env"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.django.base")

application = get_wsgi_application()
