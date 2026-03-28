# ============================================
# WSGI APPLICATION
# ============================================
# WSGI (Web Server Gateway Interface) is the interface between
# Django and the web server. This file is used by production servers.

import os
from django.core.wsgi import get_wsgi_application

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')

# Get the WSGI application
application = get_wsgi_application()
