import os
from django.core.asgi import get_asgi_application
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from myapp.consumers import TimeConsumer
from myapp.clientchat import ChatSetup
from myapp.onlinemessage import MessageBot

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myapp.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter([
        path("ws/time/", TimeConsumer.as_asgi()),
        path("ws/chat/", ChatSetup.as_asgi()),
        path("ws/messagebot/", MessageBot.as_asgi()),
    ]),
})
