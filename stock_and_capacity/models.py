from django.db import models
import uuid

class ProductStockCapacity(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    product = models.ForeignKey(
        'product.Product',              # ← ये सबसे safe तरीका
        on_delete=models.CASCADE,
        related_name='daily_capacity'
    )
    
    effective_date = models.DateField()
    
    max_capacity = models.PositiveIntegerField(default=100)
    available_capacity = models.PositiveIntegerField(default=100)
    
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    is_available = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('product', 'effective_date')
        indexes = [
            models.Index(fields=['effective_date']),
            models.Index(fields=['product', 'effective_date']),
        ]

    def __str__(self):
        return f"{self.product.name} - {self.effective_date} (Capacity)"