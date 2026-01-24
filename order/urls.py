# order/urls.py
from django.urls import path
from .views import OrderStatusView

urlpatterns = [
    path(
        "status/<uuid:order_id>/",
        OrderStatusView.as_view(),
        name="order-status"
    ),
]
