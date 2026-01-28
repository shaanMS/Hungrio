# accounts/urls.py

from django.urls import path
from .views import MeAPI




#api group
urlpatterns = [
    path("api/auth/me/", MeAPI.as_view(), name="me"),
    path("")
]

# page url group

urlpatterns += [
    
    path("/myProfile"),
    path(""),
    path(""),
    
    
    
    ]

x