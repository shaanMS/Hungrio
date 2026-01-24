from rest_framework import serializers
from .models import Wishlist , WishlistItem

from rest_framework import serializers
from .models import Wishlist , WishlistItem

class WishlistProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    price = serializers.DecimalField(
        source="final_price",
        max_digits=10,
        decimal_places=2
    )


class WishlistItemSerializer(serializers.ModelSerializer):
    product = WishlistProductSerializer(read_only=True)

    class Meta:
        model = WishlistItem
        fields = [
            "id",
            "product",
            "added_at",
        ]


class WishlistActionSerializer(serializers.Serializer):
    product = serializers.IntegerField()
