# ============================================
# PAYMENTS APP URLS
# ============================================

from django.urls import path, include
from rest_framework.routers import SimpleRouter
from apps.payments.views import PaymentViewSet, CouponViewSet

router = SimpleRouter()
router.register('payments', PaymentViewSet, basename='payment')
router.register('coupons', CouponViewSet, basename='coupon')

urlpatterns = [
    path('', include(router.urls)),
]
