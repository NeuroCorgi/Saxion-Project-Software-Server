from uuid import uuid4
from datetime import timedelta

from asgiref.sync import async_to_sync

from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from rest_framework.generics import RetrieveUpdateDestroyAPIView

from django.http import JsonResponse
from django.http.response import Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404

from vault_server.redis_server import redis

from vault.models import Vault
from vault.serializers import VaultSerializer


def init_registration(request):
    if isinstance(request.user, AnonymousUser):
        auth_token = request.META.get("HTTP_AUTHORIZATION")
        if auth_token:
            auth_token = auth_token.split()[1]
            user = get_user_model().get_user_by_token(auth_token)
    else:
        user = request.user
    
    if user is None or isinstance(user, AnonymousUser):
        raise HttpResponseForbidden()

    token = str(uuid4())
    redis.set(token, user.id, timedelta(minutes=10))
    return JsonResponse({"token": token})


def confirm_2fa(request, token):
    vault_token = redis.get(token)
    if not vault_token:
        raise HttpResponseForbidden
    vault = get_object_or_404(Vault, token=str(vault_token)[2:-1])

    user = None
    if isinstance(request.user, AnonymousUser):
        auth_token = request.META.get("HTTP_AUTHORIZATION")
        if auth_token:
            auth_token = auth_token.split()[1]
            user = get_user_model().get_user_by_token(auth_token)
    else:
        user = request.user
    
    if user is None or isinstance(user, AnonymousUser):
        raise HttpResponseForbidden()

    if vault.owner.id != user.id:
        raise Http404

    async_to_sync(get_channel_layer().group_send)(
        vault.token,
        {
            "type": "confirm_2fa",
        }
    )

    redis.delete(token)
    redis.delete(vault_token)

    return JsonResponse({"result": "Ok"})


def OwnerMixin(owner_field: str):

    class OwnerMixin:
        
        def get_object(self):
            queryset = self.get_queryset()

            obj = get_object_or_404(queryset, **{self.lookup_field: self.kwargs[self.lookup_field]})
            
            if getattr(obj, owner_field).id != self.request.user.id:
                raise Http404
            
            return obj

    return OwnerMixin


class VaultAPI(RetrieveUpdateDestroyAPIView, OwnerMixin("owner")):
    serializer_class = VaultSerializer

    def get_queryset(self):
        return Vault.objects.all()
