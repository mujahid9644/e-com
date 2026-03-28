"""
Custom middleware for the e-commerce platform.
Provides performance monitoring, error handling, and security features.
"""
import time
import logging
from django.conf import settings
from django.http import JsonResponse
from django.core.exceptions import SuspiciousOperation

logger = logging.getLogger(__name__)


class PerformanceMonitoringMiddleware:
    """
    Middleware to monitor request performance and log slow requests.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Start timing
        start_time = time.time()

        # Process the request
        response = self.get_response(request)

        # Calculate duration
        duration = time.time() - start_time

        # Log slow requests
        if duration > 1.0:  # Log requests taking more than 1 second
            logger.warning(
                f"Slow request: {request.method} {request.path} "
                f"took {duration:.2f}s from {self._get_client_ip(request)}"
            )

        # Add performance header in debug mode
        if settings.DEBUG:
            response['X-Response-Time'] = f"{duration:.3f}s"

        return response

    def _get_client_ip(self, request):
        """Get client IP address."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')


class SecurityMiddleware:
    """
    Additional security middleware for suspicious requests.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check for suspicious patterns
        if self._is_suspicious_request(request):
            logger.warning(
                f"Suspicious request blocked: {request.method} {request.path} "
                f"from {self._get_client_ip(request)}"
            )
            return JsonResponse({
                'error': 'Bad Request',
                'message': 'Request blocked for security reasons',
                'status_code': 400
            }, status=400)

        response = self.get_response(request)
        return response

    def _is_suspicious_request(self, request):
        """Check if request looks suspicious."""
        # Check for SQL injection patterns
        sql_patterns = ['union select', 'information_schema', 'script>', '<script']
        query_string = request.META.get('QUERY_STRING', '').lower()

        for pattern in sql_patterns:
            if pattern in query_string:
                return True

        # Check for directory traversal
        if '../' in request.path or '..\\' in request.path:
            return True

        return False

    def _get_client_ip(self, request):
        """Get client IP address."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')


class MaintenanceModeMiddleware:
    """
    Middleware to handle maintenance mode.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if maintenance mode is enabled
        if getattr(settings, 'MAINTENANCE_MODE', False):
            # Allow access to admin and API health check
            if not (request.path.startswith('/admin/') or
                    request.path == '/api/health/' or
                    request.path.startswith('/static/')):
                return JsonResponse({
                    'error': 'Service Unavailable',
                    'message': 'System is currently under maintenance. Please try again later.',
                    'status_code': 503
                }, status=503)

        return self.get_response(request)


class RequestLoggingMiddleware:
    """
    Middleware to log all requests for auditing.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log the request
        logger.info(
            f"Request: {request.method} {request.path} "
            f"from {self._get_client_ip(request)} "
            f"user_agent: {request.META.get('HTTP_USER_AGENT', 'Unknown')[:100]}"
        )

        response = self.get_response(request)

        # Log response status
        if response.status_code >= 400:
            logger.warning(
                f"Error response: {response.status_code} for {request.method} {request.path}"
            )

        return response

    def _get_client_ip(self, request):
        """Get client IP address."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')