# ============================================
# ORDERS APP URLS
# ============================================

from django.urls import path, include
from rest_framework.routers import SimpleRouter
from apps.orders.views import OrderViewSet

router = SimpleRouter()
router.register('', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
]
