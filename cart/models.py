# cart/models.py
from django.db import models
import uuid
from django.contrib.auth.models import User


class Cart(models.Model):
    """
    Shopping Cart Model
    Supports both authenticated and anonymous users
    Enforces: only one ACTIVE cart per user or session
    """
    STATUS_ACTIVE = 'ACTIVE'
    STATUS_CONVERTED = 'CONVERTED'
    STATUS_ABANDONED = 'ABANDONED'
    STATUS_EXPIRED = 'EXPIRED'

    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Active'),
        (STATUS_CONVERTED, 'Converted to Order'),
        (STATUS_ABANDONED, 'Abandoned'),
        (STATUS_EXPIRED, 'Expired'),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='carts',
        verbose_name="User"
    )

    session_key = models.CharField(
        max_length=40,
        null=True,
        blank=True,
        db_index=True,
        verbose_name="Session Key"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_ACTIVE,
        db_index=True,
        verbose_name="Status"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Meta:
    verbose_name = "Cart"
    verbose_name_plural = "Carts"

    constraints = [
        models.UniqueConstraint(
            fields=['user', 'status'],
            condition=models.Q(status='ACTIVE'),          # ← 'ACTIVE' स्ट्रिंग यूज़ करो
            name='unique_active_cart_per_user'
        ),
        models.UniqueConstraint(
            fields=['session_key', 'status'],
            condition=models.Q(status='ACTIVE'),          # ← यहाँ भी 'ACTIVE'
            name='unique_active_cart_per_session'
        ),
    ]

    indexes = [
        models.Index(fields=['user', 'status']),
        models.Index(fields=['session_key', 'status']),
        models.Index(fields=['status', 'updated_at']),
    ]

    ordering = ['-updated_at']



class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    cart = models.ForeignKey(
        'cart.Cart',
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey(
        'product.Product',
        on_delete=models.SET_NULL,
        null=True,                # product delete हो तो cart item रह जाए
        blank=True,
        related_name='cart_items',
        db_column='product_id'
    )

    quantity = models.PositiveIntegerField(default=1)

    price_snapshot = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Product की price उस समय की"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "cart_items"
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"
        ordering = ['created_at']

    def __str__(self):
        product_name = self.product.name if self.product else "Deleted Product"
        return f"{quantity}x {product_name} in Cart {self.cart.id[:8]}"

    @property
    def subtotal(self):
        """इस item का कुल मूल्य"""
        return self.quantity * self.price_snapshot