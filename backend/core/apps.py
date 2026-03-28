from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        """
        Initialize the core app.
        This method is called when Django starts.
        """
        # Import signals or perform initialization here if needed
        pass
