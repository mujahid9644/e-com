#!/usr/bin/env python
import os
import django
from django.conf import settings

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')

# Check if DATABASE_URL is set (required for PostgreSQL)
if 'DATABASE_URL' not in os.environ:
    print('ERROR: DATABASE_URL environment variable is not set!')
    print('Please set DATABASE_URL in your .env file to your PostgreSQL connection string.')
    exit(1)

django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Admin credentials
email = 'admin@ecommerce.com'
password = 'AdminPass123!@#'
username = 'admin'

try:
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
        print('\n✓ Superuser created successfully!\n')
    else:
        print('\n✓ Superuser already exists.\n')
    
    print('='*50)
    print('ADMIN CREDENTIALS')
    print('='*50)
    print(f'Email:    {email}')
    print(f'Password: {password}')
    print(f'Admin URL: http://localhost:8000/admin/')
    print('='*50)
    
except Exception as e:
    print(f'Error creating superuser: {e}')
