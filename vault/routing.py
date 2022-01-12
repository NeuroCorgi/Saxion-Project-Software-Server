from django.urls import re_path, path

from vault.consumers import VaultConsumer


websocket_urlpatterns = [
    re_path(
        r'ws/vault/(?P<token>[a-f0-9]{8}\-[a-f0-9]{4}\-4[a-f0-9]{3}\-[89ab][a-f0-9]{3}\-[a-f0-9]{12})/$',
        VaultConsumer.as_asgi()
    )
]
