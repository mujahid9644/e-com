# ============================================
# PRODUCT APP URLS
# ============================================

from django.urls import path, include
from rest_framework.routers import SimpleRouter
from apps.products.views import (
    CategoryViewSet, BrandViewSet, ProductViewSet,
    ProductImageViewSet, ProductAttributeViewSet
)

# Create router for viewsets
router = SimpleRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('brands', BrandViewSet, basename='brand')
router.register('', ProductViewSet, basename='product')
router.register('images', ProductImageViewSet, basename='product-image')
router.register('attributes', ProductAttributeViewSet, basename='product-attribute')

urlpatterns = [
    path('', include(router.urls)),
]
