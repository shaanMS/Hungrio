from django.contrib.postgres.fields import JSONField  # Django 5+ me models.JSONField bhi use kar sakte ho
from django.db import models
import uuid
from category.models import Category, SubCategory   # ← ये लाइन जोड़ो
# product/models.py
class Product(models.Model):
    id = models.BigAutoField(primary_key=True)  # Matches your current integer PK
    
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,  # Don't allow category delete if products exist
        related_name="products"
    )
    
    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.SET_NULL,   # ← Very important: keep product even if subcategory deleted
        null=True,
        blank=True,
        related_name="products"
    )
    
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    
    description = models.TextField(blank=True)
    is_veg = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    
    # Price fields (add these — very important for ordering app!)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    
    # Optional: image later
    # image = models.ImageField(upload_to='products/%Y/%m/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['category', 'subcategory', 'is_active']),
        ]
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Auto-calculate final price
        if self.discount_percentage > 0:
            discount = self.base_price * (self.discount_percentage / 100)
            self.final_price = round(self.base_price - discount, 2)
        else:
            self.final_price = self.base_price
        super().save(*args, **kwargs)





class ProductImage(models.Model):
    product = models.OneToOneField(
        'Product',
        on_delete=models.CASCADE,
        related_name='images'
    )

    # JSONB column (PostgreSQL)
    images = models.JSONField(default=list)
    """
    Example:
    [
        "products/1/main.jpg",
        "products/1/side.jpg",
        "products/1/top.jpg"
    ]
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Images for {self.product.name}"