
from rest_framework import generics, permissions , viewsets
from .models import Product
from .serializers import ProductSerializer
from rest_framework.response import Response
from django.utils.timezone import now
import uuid
from cart.models import Cart , CartItem
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny

class DefaultPagination(PageNumberPagination):
    page_size = 10



class ProductListAPI(generics.ListAPIView):
    """
    GET /api/products/
    """
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
   # permission_classes = [permissions.IsAuthenticated]
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'subcategory', 'is_veg']
    permission_classes = [AllowAny]


    
class ProductDetailAPI(generics.RetrieveAPIView):
    """
    GET /api/products/<id>/
    """
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]






