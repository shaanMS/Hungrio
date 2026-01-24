from django.urls import path
from .views import PlaceOrder, stripe_webhook

urlpatterns = [
    path("place-order/", PlaceOrder.as_view()),
    path("stripe/webhook/", stripe_webhook),
]
