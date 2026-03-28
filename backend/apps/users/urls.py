# ============================================
# USER APP URLS
# ============================================
# URL routing for user authentication and profile management.

from django.urls import path, include
from rest_framework.routers import SimpleRouter
from apps.users.views import (
    UserAuthViewSet,
    UserProfileViewSet,
    AddressViewSet,
    UserPreferencesViewSet
)

# Create a single router to avoid duplicate format suffix registration
router = SimpleRouter()
router.register('auth', UserAuthViewSet, basename='auth')
router.register('profile', UserProfileViewSet, basename='profile')
router.register('addresses', AddressViewSet, basename='addresses')
router.register('preferences', UserPreferencesViewSet, basename='preferences')

urlpatterns = router.urls
