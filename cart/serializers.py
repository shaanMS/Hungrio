from rest_framework import serializers
from .models import Cart, CartItem
from product.models import Product
from stock_and_capacity.models import ProductStockCapacity


class CartItemSerializer(serializers.ModelSerializer):
  product_name = serializers.CharField(source='product.name', read_only=True)
  final_price = serializers.IntegerField(source = 'productstockcapacity.selling_price' , read_only=True)
  
  class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_name', 'quantity', 'final_price']






class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True) # we can initial it with any serializer
    
    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'created_at', 'updated_at']