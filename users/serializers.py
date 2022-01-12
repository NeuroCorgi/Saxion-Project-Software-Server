from django.contrib.auth import get_user_model
from rest_framework import serializers

from vault.serializers import UserVaultSerializer


class UserSerializer(serializers.ModelSerializer):

    vaults = UserVaultSerializer(many=True)

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'vaults')