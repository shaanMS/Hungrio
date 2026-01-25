from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,

)
from django.conf import settings
from django.views.generic import TemplateView
from checkout_and_billing.views import checkout_view
urlpatterns = [
    path('admin/', admin.site.urls),

    # ---------- UI PAGES ----------
    path('', TemplateView.as_view(template_name='index.html'), name='home'),   # HOME
    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    path("cart/", TemplateView.as_view(template_name="cart.html"), name="cart"),
    path("wishlist/", TemplateView.as_view(template_name="wishlist.html")),
    path("checkout/", checkout_view, name="checkout"),   # ✅ FIXED
    path(
    "order-status/<uuid:order_id>/",
    TemplateView.as_view(template_name="order_status.html"),
    name="order_status"
),

    # ---------- AUTH APIs ----------
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include('accounts.urls')),   # /api/auth/me/
    path("api/checkout/", include("checkout_and_billing.urls")),
    path("api/order-payment/", include("order_payment.urls")),
    
    # ---------- APP APIs ----------
    path('api/products/', include('product.urls')),
    path('api/cart/', include('cart.urls')),
    path("api/wishlist/", include("wishlist.urls")),
    path("api/orders/", include("order.urls")),
    path("api/invoices/", include("invoice.urls")),

]






if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns