# ============================================
# APP CONFIGURATION
# ============================================
# This file configures the users app for Django.

from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Configuration class for the users app."""
    
    # Default auto field type
    default_auto_field = 'django.db.models.BigAutoField'
    
    # App name
    name = 'apps.users'
    
    # Verbose name shown in Django admin
    verbose_name = 'User Management'
