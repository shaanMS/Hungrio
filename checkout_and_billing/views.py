from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from decimal import Decimal
from cart.models import Cart
# views.py
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

#@login_required
def checkout_view(request):
    #if request.user.is_authenticated:
    # print('auth................')
     return render(request, "checkout.html", {
        "STRIPE_PUBLISHABLE_KEY": settings.STRIPE_PUBLISHABLE_KEY })
   # print('no auth ..... ')
   # return render(request, "checkout.html")



class CheckoutSummary(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart = Cart.objects.get(user=request.user, status="ACTIVE")

        subtotal = 0
        items = []

        for item in cart.items.all():
            price = item.product.final_price
            subtotal += price * item.quantity

            items.append({
                "product": item.product.name,
                 "price": str(price),   
                "qty": item.quantity,
                "total": str(price * item.quantity)
            })

        tax = subtotal * Decimal(0.05)  # example 5%
        discount = 10           # manual for now
        total = subtotal + tax - discount

        return Response({
            "cart_id": cart.id,
            "items": items,
            "subtotal": str(subtotal),
            "tax": str(tax),
            "discount": str(discount),
            "total": str(total),
            "payment_modes": ["CARD", "UPI", "NETBANKING"]
        })
