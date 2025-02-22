"""
ASGI config for mental project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""
import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from django.urls import path , re_path
from .middlewares import JWTmiddleware
from doctors.consumer import Aiserver   

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mental.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
        JWTmiddleware(
            URLRouter([
                re_path(r'ws/chat',Aiserver.as_asgi())
            ])
        )
    ),
})



