"""
Custom exception handler for Django REST Framework.
Provides consistent error responses across the API.
"""
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from django.db import IntegrityError
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler that provides consistent error responses.

    Returns a standardized error response format for all API errors.
    """
    # Get the standard error response
    response = exception_handler(exc, context)

    if response is not None:
        # Log the error for debugging
        logger.error(f"API Error: {exc.__class__.__name__}: {str(exc)}", exc_info=True)

        # Customize the error response format
        custom_response_data = {
            'error': get_error_type(exc),
            'message': get_error_message(exc, response.data),
            'status_code': response.status_code,
            'details': get_error_details(exc, response.data)
        }

        # Remove sensitive information in production
        if hasattr(exc, 'detail') and 'password' in str(exc.detail).lower():
            custom_response_data['message'] = 'Authentication failed'

        response.data = custom_response_data

    else:
        # Handle unhandled exceptions
        logger.critical(f"Unhandled exception: {exc.__class__.__name__}: {str(exc)}", exc_info=True)

        custom_response_data = {
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred. Please try again later.',
            'status_code': 500,
            'details': {}
        }

        response = Response(custom_response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response


def get_error_type(exc):
    """
    Get a user-friendly error type based on the exception.
    """
    error_types = {
        ValidationError: 'Validation Error',
        IntegrityError: 'Data Integrity Error',
        PermissionError: 'Permission Denied',
        ValueError: 'Invalid Value',
        KeyError: 'Missing Required Field',
        TypeError: 'Invalid Data Type',
    }

    return error_types.get(type(exc), 'API Error')


def get_error_message(exc, response_data):
    """
    Extract a user-friendly error message from the exception and response data.
    """
    # Handle DRF validation errors
    if hasattr(exc, 'detail') and isinstance(exc.detail, dict):
        # Get the first error message from validation errors
        for field, errors in exc.detail.items():
            if isinstance(errors, list) and errors:
                return str(errors[0])
            return str(errors)

    # Handle standard DRF error responses
    if isinstance(response_data, dict):
        if 'detail' in response_data:
            return str(response_data['detail'])
        elif 'non_field_errors' in response_data and response_data['non_field_errors']:
            return str(response_data['non_field_errors'][0])

    # Handle IntegrityError
    if isinstance(exc, IntegrityError):
        if 'unique constraint' in str(exc).lower():
            return 'This record already exists'
        elif 'foreign key' in str(exc).lower():
            return 'Related record not found'
        return 'Database constraint violation'

    # Default to exception message
    return str(exc) if str(exc) else 'An error occurred'


def get_error_details(exc, response_data):
    """
    Get additional error details for debugging (only in DEBUG mode).
    """
    from django.conf import settings

    if not settings.DEBUG:
        return {}

    details = {}

    # Add field-specific validation errors
    if hasattr(exc, 'detail') and isinstance(exc.detail, dict):
        details['field_errors'] = exc.detail

    # Add response data for debugging
    if isinstance(response_data, dict):
        details['response_data'] = response_data

    # Add exception type
    details['exception_type'] = exc.__class__.__name__

    return details