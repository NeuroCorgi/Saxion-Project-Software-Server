from django.db import models
from django.contrib.auth import get_user_model

from vault_server.redis_server import redis
# from users.models import User


class Vault(models.Model):

    name = models.CharField(max_length=100, default="New Vault")
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    token = models.CharField(max_length=40, unique=True)

    requires_2fa = models.BooleanField(default=True)

    @property
    def awaits_approve(self):
        if redis.get(self.token):
            return True
        return False

    @property
    def auth_token(self):
        return redis.get(self.token)

    def history(self):
        return self.openinglog_set.all()


class OpeningLog(models.Model):

    vault = models.ForeignKey(Vault, on_delete=models.CASCADE)
    time = models.DateTimeField()
    success = models.BooleanField(null=True, blank=True, default=False)
