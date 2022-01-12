import json
from uuid import uuid4
from datetime import datetime, timedelta

from asgiref.sync import async_to_sync

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from channels.generic.websocket import WebsocketConsumer

from vault_server.redis_server import redis

from .models import Vault, OpeningLog

class VaultConsumer(WebsocketConsumer):

    def connect(self):
        self.room_name = token = self.scope['url_route']['kwargs']['token']
        try:
            self.vault = Vault.objects.get(token=token)
        except ObjectDoesNotExist:
            owner = get_user_model().objects.get(pk=int(redis.get(token)))
            self.vault = Vault(token=token, owner=owner)
            self.vault.save()

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_name,
            self.channel_name
        )

        redis.delete(token)

        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name,
            self.channel_name
        )

    def receive(self, text_data=None, **kwargs):
        data = json.loads(text_data)
        if data["type"] == "log":
            OpeningLog(
                vault=self.vault,
                time=datetime.now(),
                success=data["success"]
            ).save()

        elif data["type"] == "2fa_req":
            token = str(uuid4())
            redis.set(token, self.vault.token, timedelta(minutes=5))
            redis.set(self.vault.token, token, timedelta(minutes=5))

        elif data["type"] == "2fa_canc":
            auth_token = redis.get(self.vault.token)
            if auth_token:
                redis.delete(self.vault.token)
                redis.delete(auth_token)

    def confirm_2fa(self, event):
        self.send(text_data="confirm_2fa")
