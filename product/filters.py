''' for implementing filters like product titile ok , its another app for just filtering ok!'''



import django_filters
from category.models import (Category , SubCategory)
from .models import Product






class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains' , label='Dish Name')






    class Meta:
        model = Product
        fields = [
            'name'
        ]