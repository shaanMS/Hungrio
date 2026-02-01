   # accounts/urls.py

from django.urls import path
from .views import MeAPI
from .CaptchaView import CaptchaTokenView



#api group
urlpatterns = [
    path("api/auth/me/", MeAPI.as_view(), name="me"),
  #  path("login/", CaptchaTokenView.as_view()),
    # path("api/token/", CaptchaTokenView.as_view()),
    
]

