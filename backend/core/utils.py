"""
Utility functions for the e-commerce platform.
"""
import uuid
from django.utils.text import slugify
from django.core.exceptions import ValidationError


def generate_unique_slug(model_class, title, max_length=100):
    """
    Generate a unique slug for a model instance.

    Args:
        model_class: The Django model class
        title: The title to generate slug from
        max_length: Maximum length of the slug

    Returns:
        str: A unique slug
    """
    base_slug = slugify(title)[:max_length]
    slug = base_slug
    counter = 1

    while model_class.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
        if len(slug) > max_length:
            slug = f"{base_slug[:max_length-len(str(counter))-1]}-{counter}"

    return slug


def generate_order_number():
    """
    Generate a unique order number.

    Returns:
        str: A unique order number in format ORD-YYYYMMDD-XXXX
    """
    from datetime import datetime
    timestamp = datetime.now().strftime('%Y%m%d')
    unique_id = str(uuid.uuid4().hex)[:8].upper()
    return f"ORD-{timestamp}-{unique_id}"


def validate_image_size(image_file, max_size_mb=5):
    """
    Validate image file size.

    Args:
        image_file: The uploaded image file
        max_size_mb: Maximum allowed size in MB

    Raises:
        ValidationError: If image is too large
    """
    max_size_bytes = max_size_mb * 1024 * 1024
    if image_file.size > max_size_bytes:
        raise ValidationError(f"Image file too large. Maximum size is {max_size_mb}MB.")


def validate_image_format(image_file, allowed_formats=None):
    """
    Validate image file format.

    Args:
        image_file: The uploaded image file
        allowed_formats: List of allowed formats (default: ['JPEG', 'PNG', 'WEBP'])

    Raises:
        ValidationError: If format is not allowed
    """
    if allowed_formats is None:
        allowed_formats = ['JPEG', 'PNG', 'WEBP']

    try:
        from PIL import Image
        img = Image.open(image_file)
        if img.format.upper() not in allowed_formats:
            raise ValidationError(f"Unsupported image format. Allowed formats: {', '.join(allowed_formats)}")
    except Exception:
        raise ValidationError("Invalid image file")


def calculate_discount_percentage(original_price, discounted_price):
    """
    Calculate discount percentage.

    Args:
        original_price: Original price
        discounted_price: Discounted price

    Returns:
        float: Discount percentage (0-100)
    """
    if original_price <= 0:
        return 0

    discount = original_price - discounted_price
    percentage = (discount / original_price) * 100
    return round(percentage, 2)


def format_currency(amount, currency='USD'):
    """
    Format amount as currency.

    Args:
        amount: Numeric amount
        currency: Currency code

    Returns:
        str: Formatted currency string
    """
    try:
        # For now, simple formatting. In production, use proper currency formatting
        return f"${amount:.2f}"
    except (ValueError, TypeError):
        return f"${0:.2f}"


def get_client_ip(request):
    """
    Get the client IP address from the request.

    Args:
        request: Django request object

    Returns:
        str: Client IP address
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def safe_get(obj, key, default=None):
    """
    Safely get a value from a dictionary or object.

    Args:
        obj: Dictionary or object
        key: Key to access
        default: Default value if key doesn't exist

    Returns:
        Value or default
    """
    try:
        if isinstance(obj, dict):
            return obj.get(key, default)
        else:
            return getattr(obj, key, default)
    except (AttributeError, KeyError, TypeError):
        return default