from django.urls import path, re_path

from .views import (
    UserAPI
)

urlpatterns = [
    path("<int:pk>/", UserAPI.as_view())
]