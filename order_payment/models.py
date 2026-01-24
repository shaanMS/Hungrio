import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class PaymentTransaction(models.Model):

    STATUS = (
        ("INITIATED", "Initiated"),
        ("SUCCESS", "Success"),
        ("FAILED", "Failed"),
        ("REFUNDED", "Refunded"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # order = models.ForeignKey(
    #     "order.Order",
    #     on_delete=models.CASCADE,
    #     related_name="payments"
    # )
    order = models.ForeignKey(
        "order.Order",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payments"
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    payment_gateway = models.CharField(max_length=30)  # stripe
    gateway_payment_id = models.CharField(max_length=255, null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS, default="INITIATED")

    created_at = models.DateTimeField(auto_now_add=True)




# payments/models.py
class StripeWebhookEvent(models.Model):
    event_id = models.CharField(max_length=255, unique=True)
    processed_at = models.DateTimeField(auto_now_add=True)
