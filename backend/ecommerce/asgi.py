# ============================================
# ASGI APPLICATION (for WebSocket support - optional)
# ============================================
# ASGI (Asynchronous Server Gateway Interface) extends WSGI
# to support WebSocket, HTTP/2, etc.

import os
from django.core.asgi import get_asgi_application

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')

# Get the ASGI application
application = get_asgi_application()
