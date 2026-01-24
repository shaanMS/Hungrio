from rest_framework.routers import DefaultRouter
from .views import CartViewSet
from django.urls import path, include
from .cart_view import cart_ui 



router = DefaultRouter()
router.register(r'cart', CartViewSet, basename='cart')

urlpatterns = [
    path('', include(router.urls)),
    path("cart-ui/", cart_ui, name="cart-ui"),
]