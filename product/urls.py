from django.urls import path
from . import views
from . import product_home_view 
#from .views import ProductHierarchyAPI

urlpatterns = [
    path('', views.ProductListAPI.as_view(), name='product-list'),
    path('<int:pk>/', views.ProductDetailAPI.as_view(), name='product-detail'),
    path('ui/', product_home_view.menu_ui, name='menu-ui'),
]
