from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from myapp.consumers import TimeConsumer

application = ProtocolTypeRouter({
    "websocket": URLRouter([
        path("ws/time/", TimeConsumer.as_asgi()),
    ]),
})
