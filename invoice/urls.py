from django.urls import path
from .views import DownloadStripeInvoiceView

urlpatterns = [
    path("<uuid:order_id>/download/", DownloadStripeInvoiceView.as_view(), name="stripe-invoice-download"),
]