from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def cart_ui(request):
    return render(request, "cart/cart.html")
