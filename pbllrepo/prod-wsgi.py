"""
WSGI config for pbllrepo project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os, sys

sys.path.insert(0, '/pythonapps/nflrc-pbllrepo-dev/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pbllrepo.settings.prod-pbllrepo-hawaii-edu")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
