# ============================================
# MAIN URL ROUTING
# ============================================
# This file routes all incoming requests to the appropriate apps.
# Think of it as the "map" of your entire API.

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework_simplejwt.views import TokenRefreshView

# ============================================
# URL PATTERNS
# ============================================
urlpatterns = [
    # -------- ADMIN PANEL --------
    path('admin/', admin.site.urls),
    
    # -------- API DOCUMENTATION (Swagger) --------
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # -------- API ENDPOINTS --------
    # Include URLs from each app
    path('api/auth/', include('apps.users.urls')),  # User authentication routes
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # JWT refresh
    path('api/products/', include('apps.products.urls')),  # Product management routes
    path('api/cart/', include('apps.cart.urls')),  # Shopping cart routes
    path('api/orders/', include('apps.orders.urls')),  # Order management routes
    path('api/payments/', include('apps.payments.urls')),  # Payment processing routes
    path('api/reviews/', include('apps.reviews.urls')),  # Product reviews routes
    path('api/', include('core.urls')),  # Core utilities and health checks
    path('auth/', include('social_django.urls', namespace='social')),  # Social auth routes
]

# ============================================
# SERVE STATIC & MEDIA FILES IN DEVELOPMENT
# ============================================
# In production, these should be served by a web server like Nginx
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# ============================================
# Custom error handlers
# ============================================
from django.http import JsonResponse

def custom_404_handler(request, exception):
    return JsonResponse({
        'error': 'Not Found',
        'message': 'The requested resource was not found.',
        'status_code': 404
    }, status=404)


def custom_500_handler(request):
    return JsonResponse({
        'error': 'Internal Server Error',
        'message': 'An unexpected error occurred. Please try again later.',
        'status_code': 500
    }, status=500)


handler404 = 'ecommerce.urls.custom_404_handler'
handler500 = 'ecommerce.urls.custom_500_handler'
