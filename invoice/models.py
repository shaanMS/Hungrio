




from django.db import models
from order.models import Order

class Invoice(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='invoice')

    invoice_number = models.CharField(max_length=50, blank=True, null=True)
    invoice_type = models.CharField(max_length=20, default="STRIPE", editable=False)

    stripe_invoice_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_invoice_pdf = models.URLField(blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=(("PENDING", "Pending"), ("GENERATED", "Generated"), ("FAILED", "Failed")),
        default="PENDING"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Invoice {self.invoice_number or '—'} for Order {self.order_id}"