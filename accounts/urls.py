   # accounts/urls.py

from django.urls import path
from .views import MeAPI




#api group
urlpatterns = [
    path("api/auth/me/", MeAPI.as_view(), name="me"),
<<<<<<< HEAD
]

=======
    
]

# page url group


>>>>>>> f6ace98ee09aea45157ae2f31b5c08266e9b4b46
