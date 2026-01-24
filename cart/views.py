from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Cart, CartItem
from product.models import Product
from stock_and_capacity.models import ProductStockCapacity
from .serializers import CartSerializer, CartItemSerializer



class CartViewSet(viewsets.ViewSet):

    def get_cart(self, request):
     if request.user.is_authenticated:
        print('ok ok cart user is autherized')
        cart, _ = Cart.objects.get_or_create(
            user=request.user,
            status=Cart.STATUS_ACTIVE
        )
     else:
      '''  request.session.save()
        cart, _ = Cart.objects.get_or_create(
            session_key=request.session.session_key,
            status=Cart.STATUS_ACTIVE
        )'''
     
     return cart

    @action(detail=False, methods=['get'])
    def list_items(self, request):
       if request.user.is_authenticated:
        cart = self.get_cart(request)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def add_item(self, request):
        product_id = request.data.get('product')
        quantity = int(request.data.get('quantity', 1))
        
        try:
            product = Product.objects.get(id=product_id, is_active=True)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        cart = self.get_cart(request)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product,
        defaults={"price_snapshot": product.final_price})
       
       
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()
        
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def remove_item(self, request):
        product_id = request.data.get('product')
        cart = self.get_cart(request)

        try:
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
            cart_item.delete()
            return Response({"status": "removed"})
        except CartItem.DoesNotExist:
            return Response({"error": "Item not in cart"}, status=status.HTTP_404_NOT_FOUND)

