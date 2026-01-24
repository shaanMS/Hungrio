from django.urls import path
from .views import CheckoutSummary

urlpatterns = [
    path("summary/", CheckoutSummary.as_view()),
]
