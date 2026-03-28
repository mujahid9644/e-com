#!/usr/bin/env python
"""
Django's command-line utility for administrative tasks.
This file is used to manage the Django project from the command line.
"""

import os
import sys


def main():
    """Run administrative tasks."""
    # Set the Django settings module to our project settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Execute the command passed to this script
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
