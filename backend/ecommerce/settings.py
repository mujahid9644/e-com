# ============================================
# DJANGO PROJECT SETTINGS
# ============================================
# This is the main configuration file for the Django project.
# All Django settings and app configurations are defined here.

import os
from pathlib import Path
from datetime import timedelta
from django.core.exceptions import ImproperlyConfigured
from decouple import config

import cloudinary
import cloudinary.uploader
import cloudinary.api

# Configure Cloudinary immediately after import if credentials are available
# This ensures CloudinaryField models can use the credentials
CLOUDINARY_CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME') or config('CLOUDINARY_CLOUD_NAME', default='')
CLOUDINARY_API_KEY = os.environ.get('CLOUDINARY_API_KEY') or config('CLOUDINARY_API_KEY', default='')
CLOUDINARY_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET') or config('CLOUDINARY_API_SECRET', default='')

if all([CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET]):
    cloudinary.config(
        cloud_name=CLOUDINARY_CLOUD_NAME,
        api_key=CLOUDINARY_API_KEY,
        api_secret=CLOUDINARY_API_SECRET,
        secure=True
    )

# ============================================
# PROJECT DIRECTORIES
# ============================================
# Get the absolute path to the project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# ============================================
# SECRET KEY & DEBUG MODE
# ============================================
# SECURITY WARNING: keep the secret key used in production secret!
# Change this in production environment
SECRET_KEY = config('SECRET_KEY', default='django-insecure-your-secret-key-change-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

# ============================================
# ALLOWED HOSTS
# ============================================
# Add your domain and servers here
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=lambda v: [s.strip() for s in v.split(',')])

# ============================================
# INSTALLED APPS
# ============================================
# Django apps and third-party apps
INSTALLED_APPS = [
    'django_filters',
    # Django default apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'rest_framework',  # Django REST Framework
    'corsheaders',  # Handle CORS requests
    'drf_spectacular',  # API documentation
    'cloudinary',  # Cloudinary storage backend
    'cloudinary_storage',
    'social_django',  # Social authentication (Google OAuth, etc.)
    
    # Local apps
    'apps.users',  # User authentication and profiles
    'apps.products',  # Product management
    'apps.cart',  # Shopping cart
    'apps.orders',  # Order management
    'apps.payments',  # Payment processing
    'apps.reviews',  # Product reviews and ratings
    'core',  # Core utilities and error handling
]

# ============================================
# MIDDLEWARE
# ============================================
# Middleware is processed in order - top to bottom for request, bottom to top for response
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # WhiteNoise for static file serving
    'corsheaders.middleware.CorsMiddleware',  # CORS middleware - must be before Django middleware
    'core.middleware.SecurityMiddleware',  # Custom security middleware
    'core.middleware.PerformanceMonitoringMiddleware',  # Performance monitoring
    'core.middleware.RequestLoggingMiddleware',  # Request logging
    'core.middleware.MaintenanceModeMiddleware',  # Maintenance mode
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',  # Social auth middleware
]

# ============================================
# URL CONFIGURATION
# ============================================
ROOT_URLCONF = 'ecommerce.urls'

# ============================================
# TEMPLATES
# ============================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Global templates directory
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

# ============================================
# WSGI APPLICATION
# ============================================
# WSGI is used by the web server to serve the application
WSGI_APPLICATION = 'ecommerce.wsgi.application'

# ============================================
# DATABASE CONFIGURATION
# ============================================
# PostgreSQL (Neon) is the ONLY database used in this project
# No SQLite fallback - DATABASE_URL must be set to PostgreSQL

import dj_database_url

# Get DATABASE_URL from environment (required for PostgreSQL)
DATABASE_URL = config('DATABASE_URL')

# PostgreSQL configuration only
DATABASES = {
    'default': dj_database_url.config(
        default=DATABASE_URL,
        conn_max_age=600,
        conn_health_checks=True,
        ssl_require=True,
    )
}


# ============================================
# PASSWORD VALIDATION
# ============================================
# These validators ensure strong passwords are used
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ============================================
# INTERNATIONALIZATION
# ============================================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ============================================
# STATIC FILES (CSS, JavaScript, Images)
# ============================================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
# Only include static directory in development
STATICFILES_DIRS = [BASE_DIR / 'static'] if DEBUG else []

# WhiteNoise configuration for efficient static file serving
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ============================================
# MEDIA FILES (User uploads - products, profile pictures)
# ============================================
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ============================================
# CLOUDINARY STORAGE (DEVELOPMENT/PRODUCTION)
# ============================================
USE_CLOUDINARY = config('USE_CLOUDINARY', default=False, cast=bool)

if USE_CLOUDINARY:
    # Check that credentials are available
    if not all([CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET]):
        raise ImproperlyConfigured('Cloudinary is enabled but CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, or CLOUDINARY_API_SECRET is not set.')

    # Set CLOUDINARY_URL so third-party packages can detect credentials
    os.environ['CLOUDINARY_URL'] = f"cloudinary://{CLOUDINARY_API_KEY}:{CLOUDINARY_API_SECRET}@{CLOUDINARY_CLOUD_NAME}"
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
else:
    # Development: Use local file storage
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# ============================================
# DEFAULT PRIMARY KEY FIELD TYPE
# ============================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ============================================
# REST FRAMEWORK CONFIGURATION
# ============================================
REST_FRAMEWORK = {
    # Authentication classes used for the API
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # JWT token auth
        'rest_framework.authentication.SessionAuthentication',  # Session auth (fallback)
    ),
    
    # Permission classes - who can access what
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',  # Allow read access to all, write only for authenticated
    ),
    
    # Pagination for listing endpoints
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    
    # Filter and search backends
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
    
    # Schema/Documentation generation
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    
    # JSON date format
    'DATE_FORMAT': '%Y-%m-%d',
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',
    
    # Disable format suffixes to avoid router conflicts
    'URL_FORMAT_OVERRIDE': None,
}

# ============================================
# JWT (JSON Web Token) SETTINGS
# ============================================
# Configure JWT token expiration and refresh times
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=24),  # Access token valid for 24 hours
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),  # Refresh token valid for 7 days
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': config('JWT_SECRET', default=SECRET_KEY),
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JTI_CLAIM': 'jti',
    'TOKEN_TYPE_CLAIM': 'token_type',
    'JTI_ALGORITHM': 'HS256',
}

# ============================================
# CORS CONFIGURATION
# ============================================
# Allow requests from frontend URLs
CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default='http://localhost:3000,http://127.0.0.1:3000',
    cast=lambda v: [s.strip() for s in v.split(',')]
)

# Convenience for local development
CORS_ALLOW_ALL_ORIGINS = DEBUG

# Allow credentials (cookies) in CORS requests
CORS_ALLOW_CREDENTIALS = True

# ============================================
# STATIC CONFIGURATION
# ============================================
# In production (not DEBUG), enable HTTPS/SSL and secure cookies
SECURE_SSL_REDIRECT = not DEBUG  # Set to True in production with HTTPS
SESSION_COOKIE_SECURE = not DEBUG  # Set to True in production with HTTPS
CSRF_COOKIE_SECURE = not DEBUG  # Set to True in production with HTTPS
SECURE_HSTS_SECONDS = 31536000 if not DEBUG else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG
SECURE_HSTS_PRELOAD = not DEBUG

# ============================================
# DRF SPECTACULAR (API DOCUMENTATION)
# ============================================
SPECTACULAR_SETTINGS = {
    'TITLE': 'E-Commerce API',
    'DESCRIPTION': 'Modern E-Commerce Platform API',
    'VERSION': '1.0.0',
    'SERVE_PERMISSIONS': ['rest_framework.permissions.AllowAny'],
    'SERVE_INCLUDE_SCHEMA': False,
}

# ============================================
# LOGGING CONFIGURATION
# ============================================
# Configure logging for debugging and production monitoring
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console', 'file'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}

# Create logs directory if it doesn't exist
os.makedirs(BASE_DIR / 'logs', exist_ok=True)

# ============================================
# ERROR HANDLING & DEBUGGING
# ============================================
# Custom error handlers for better error responses
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

# ============================================
# PERFORMANCE OPTIMIZATIONS
# ============================================
# Database connection pooling and optimization for PostgreSQL
if not DEBUG:
    DATABASES['default']['CONN_MAX_AGE'] = 60  # Connection pooling
    # PostgreSQL doesn't use init_command like MySQL
    # Connection optimization is handled via dj_database_url

# Cache settings (Redis recommended for production)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# Session caching
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

# ============================================
# SECURITY ENHANCEMENTS
# ============================================
# Additional security settings
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# Rate limiting (requires django-ratelimit)
RATELIMIT_ENABLE = True
RATELIMIT_USE_CACHE = 'default'

# ============================================
# REST FRAMEWORK ENHANCEMENTS
# ============================================
# Enhanced REST Framework settings for better error handling
REST_FRAMEWORK.update({
    'EXCEPTION_HANDLER': 'apps.core.exceptions.custom_exception_handler',
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour'
    },
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
})

# ============================================
# EMAIL CONFIGURATION
# ============================================
# Email settings for notifications
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@yourdomain.com')

# ============================================
# CELERY CONFIGURATION (Optional)
# ============================================
# Background task processing
CELERY_BROKER_URL = config('REDIS_URL', default='redis://localhost:6379/0')
CELERY_RESULT_BACKEND = config('REDIS_URL', default='redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

# ============================================
# CUSTOM USER MODEL
# ============================================
# Use CustomUser as the default user model for authentication
AUTH_USER_MODEL = 'users.CustomUser'

# ============================================
# SOCIAL AUTHENTICATION (GOOGLE OAUTH)
# ============================================
AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = config('GOOGLE_OAUTH_CLIENT_ID', default='')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = config('GOOGLE_OAUTH_CLIENT_SECRET', default='')

SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'profile',
    'email',
]

SOCIAL_AUTH_GOOGLE_OAUTH2_PROFILE_EXTRA_DATA = {
    'first_name': 'first_name',
    'last_name': 'last_name',
    'picture': 'picture',
    'locale': 'locale',
}

# Pipeline for handling user data after authentication
SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.auth.auth_allowed',
    'social_core.pipeline.auth.get_username',
    'social_core.pipeline.user.get_user_id',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

# URL for redirecting after social login
SOCIAL_AUTH_LOGIN_REDIRECT_URL = config('FRONTEND_URL', default='http://localhost:3000')
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = config('FRONTEND_URL', default='http://localhost:3000')
