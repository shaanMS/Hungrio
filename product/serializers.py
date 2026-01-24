from rest_framework import serializers
from .models import Product
from rest_framework.pagination import PageNumberPagination


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    subcategory_name = serializers.CharField(source='subcategory.name', read_only=True)
    w = serializers.CharField(read_only=True , default = 'wwww')
   
    class Meta:
        model = Product      
        fields = [
            'id',
            'name',  
            'slug',
            'category',
            'category_name',
            'subcategory',
            'subcategory_name',
            'description',
            'is_veg',
            'base_price',
            'discount_percentage',
            'final_price',
            'is_active',
            'created_at',
           'w',
            
           ]









