"""
ASGI config for spiderweb_technologies project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
# Asynchronous programming
from django.core.asgi import get_asgi_application

# AI Chatbot app page routing
import chat.routing

# Channels routing
from channels.routing import ProtocolTypeRouter, URLRouter

# Authentication
from channels.auth import AuthMiddlewareStack


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spiderweb_technologies.settings')

# Asynchronous application
# application = get_asgi_application()

# Channels asynchronous application
application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': URLRouter(
            chat.routing.websocket_urlpatterns
            ),
            })