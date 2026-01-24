# accounts/urls.py

from django.urls import path
from .views import MeAPI

urlpatterns = [
    path("api/auth/me/", MeAPI.as_view(), name="me"),
]
