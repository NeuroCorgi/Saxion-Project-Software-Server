from rest_framework.generics import RetrieveUpdateAPIView

from django.http import Http404
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from users.serializers import UserSerializer


class SelfOrAdminMixin:

    def get_object(self):
        queryset = self.get_queryset()

        obj = get_object_or_404(queryset, **{self.lookup_field: self.kwargs[self.lookup_field]})
        
        if obj.id != self.request.user.id and not self.request.user.is_superuser:
            raise Http404
        
        return obj


class UserAPI(RetrieveUpdateAPIView, SelfOrAdminMixin):
    serializer_class = UserSerializer

    def get_queryset(self):
        return get_user_model().objects.all()

    def get_object(self):
        token = self.request.META.get("HTTP_AUTHORIZATION")
        if self.kwargs[self.lookup_field] == 0 and token:
            token = token.split()[1]
            user = get_user_model().get_user_by_token(token)
            # user = get_user_model().objects.get(pk=Token.objects.get(key=token.split()[1]).user_id)
            return user
        return super().get_object()
