from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator  # very important 
User = get_user_model()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    phone = models.CharField(max_length=15)

    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    age = models.PositiveIntegerField(
        null=False,
        blank=False,
        validators=[
            MinValueValidator(14),
            MaxValueValidator(100)
        ]
    )
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    country = models.CharField(max_length=50, default="India")

    created_at = models.DateTimeField(auto_now_add=True)
    profile_filled_count = models.PositiveSmallIntegerField(default=0)
    profile_completion_percent = models.PositiveSmallIntegerField(default=0)
    def __str__(self):
        return f"{self.user.email}"
    
    class meta:
        indexes =[]