"""
ASGI config for elements project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os


from channels.routing import get_default_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'port.settings')

application = get_default_application()
