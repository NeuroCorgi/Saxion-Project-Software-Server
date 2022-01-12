from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    UserManager
)

from rest_framework.authtoken.models import Token


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)

    is_active = models.BooleanField(verbose_name="active", default=True)
    is_staff = models.BooleanField(verbose_name="staff", default=False)

    date_joined = models.DateTimeField(null=True, blank=True)
    last_login = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('email',)

    def vaults(self):
        return self.vault_set.all()

    @classmethod
    def get_user_by_token(cls, token):
        try:
            user = cls.objects.get(pk=Token.objects.get(key=token).user_id)
        except cls.DoesNotExist:
            return None
        return user

    def __str__(self):
        return f"<User: {self.username}; {self.id}>"
