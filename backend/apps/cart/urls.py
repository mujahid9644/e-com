# ============================================
# CART APP URLS
# ============================================

from django.urls import path, include
from rest_framework.routers import SimpleRouter
from apps.cart.views import CartViewSet, WishlistViewSet

router = SimpleRouter()
router.register('', CartViewSet, basename='cart')
router.register('wishlist', WishlistViewSet, basename='wishlist')

urlpatterns = [
    path('', include(router.urls)),
]
