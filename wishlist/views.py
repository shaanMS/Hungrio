from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from product.models import Product
from .models import Wishlist, WishlistItem
from .serializers import (
    WishlistItemSerializer,
    WishlistActionSerializer
)






class WishlistView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)

        items = wishlist.items.select_related("product").all()
     
        serializer = WishlistItemSerializer(items, many=True)

        return Response({
            "status": True,
            "message": "Wishlist fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
   
    def post(self, request):
        serializer = WishlistActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_id = serializer.validated_data["product"]

        product = get_object_or_404(Product, id=product_id)

        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)

        item, created = WishlistItem.objects.get_or_create(
            wishlist=wishlist,
            product=product
        )

        if not created:
            return Response({
                "status": False,
                "message": "Product already in wishlist",
                "data": None
            }, status=status.HTTP_200_OK)

        return Response({
            "status": True,
            "message": "Product added to wishlist",
            "data": None
        }, status=status.HTTP_201_CREATED)
    
    
    def delete(self, request):
        serializer = WishlistActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_id = serializer.validated_data["product"]

        deleted, _ = WishlistItem.objects.filter(
            wishlist__user=request.user,
            product_id=product_id
        ).delete()

        if deleted == 0:
            return Response({
                "status": False,
                "message": "Product not found in wishlist",
                "data": None
            }, status=status.HTTP_404_NOT_FOUND)

        return Response({
            "status": True,
            "message": "Product removed from wishlist",
            "data": None
        }, status=status.HTTP_200_OK)
