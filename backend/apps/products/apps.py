# ============================================
# APP CONFIGURATION
# ============================================
# This file configures the products app for Django.

from django.apps import AppConfig


class ProductsConfig(AppConfig):
    """Configuration class for the products app."""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.products'
    verbose_name = 'Product Management'
    
    def ready(self):
        """Import signals to ensure they are registered."""
        import apps.products.models  # noqa
