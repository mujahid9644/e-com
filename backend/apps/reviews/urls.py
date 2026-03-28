# ============================================
# REVIEWS APP URLS
# ============================================

from django.urls import path, include
from rest_framework.routers import SimpleRouter
from apps.reviews.views import ProductReviewViewSet

router = SimpleRouter()
router.register('', ProductReviewViewSet, basename='review')

urlpatterns = [
    path('', include(router.urls)),
]
