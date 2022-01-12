from django.urls import path, re_path

from .views import (
    init_registration,
    confirm_2fa,
    VaultAPI
)

urlpatterns = [
    path('register/',  init_registration),
    re_path(r'confirm/(?P<token>[a-f0-9]{8}\-[a-f0-9]{4}\-4[a-f0-9]{3}\-[89ab][a-f0-9]{3}\-[a-f0-9]{12})/$', confirm_2fa),
    path("<int:pk>/", VaultAPI.as_view())
]