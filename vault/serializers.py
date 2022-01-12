from rest_framework import serializers

from vault.models import Vault, OpeningLog


class LogSerializer(serializers.ModelSerializer):

    time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = OpeningLog
        fields = ('time', 'success')


class UserVaultSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vault
        fields = ('id', 'name', 'awaits_approve')


class VaultSerializer(serializers.ModelSerializer):

    history = LogSerializer(many=True)

    class Meta:
        model = Vault
        fields = ('id', 'name', 'token', 'history', 'requires_2fa', 'awaits_approve', 'auth_token')
