"""
Health check views for monitoring the application status.
"""
from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
import psutil
import os


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Basic health check endpoint.
    Returns the status of the application and its dependencies.
    """
    health_status = {
        'status': 'healthy',
        'timestamp': __import__('datetime').datetime.now().isoformat(),
        'version': '1.0.0',
        'services': {}
    }

    # Check database
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        health_status['services']['database'] = 'healthy'
    except Exception as e:
        health_status['services']['database'] = 'unhealthy'
        health_status['status'] = 'unhealthy'
        health_status['database_error'] = str(e)

    # Check cache
    try:
        cache.set('health_check', 'ok', 10)
        cache_value = cache.get('health_check')
        if cache_value == 'ok':
            health_status['services']['cache'] = 'healthy'
        else:
            health_status['services']['cache'] = 'unhealthy'
    except Exception as e:
        health_status['services']['cache'] = 'unhealthy'
        health_status['cache_error'] = str(e)

    # System metrics
    try:
        health_status['system'] = {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('/').percent,
        }
    except Exception:
        health_status['system'] = 'metrics_unavailable'

    # Set HTTP status code
    status_code = 200 if health_status['status'] == 'healthy' else 503

    return JsonResponse(health_status, status=status_code)


@api_view(['GET'])
@permission_classes([AllowAny])
def ping(request):
    """
    Simple ping endpoint for load balancer health checks.
    """
    return JsonResponse({'status': 'pong', 'timestamp': __import__('datetime').datetime.now().isoformat()})


@api_view(['GET'])
@permission_classes([AllowAny])
def readiness(request):
    """
    Readiness probe for Kubernetes/Docker.
    Checks if the application is ready to serve traffic.
    """
    try:
        # Check database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")

        # Check if required tables exist
        from django.apps import apps
        required_apps = ['users', 'products', 'cart', 'orders']
        for app_name in required_apps:
            try:
                apps.get_app_config(f'apps.{app_name}')
            except Exception:
                return JsonResponse({
                    'status': 'not_ready',
                    'message': f'App {app_name} not ready'
                }, status=503)

        return JsonResponse({
            'status': 'ready',
            'message': 'Application is ready to serve traffic'
        })

    except Exception as e:
        return JsonResponse({
            'status': 'not_ready',
            'message': f'Application not ready: {str(e)}'
        }, status=503)
