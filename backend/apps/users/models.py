# ============================================
# USER MODELS
# ============================================
# Defines the database structure for user accounts and profiles.

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.utils import timezone

# ============================================
# CUSTOM USER MODEL
# ============================================
class CustomUser(AbstractUser):
    """
    Extended user model with additional fields for e-commerce.
    
    Extends Django's built-in AbstractUser to add:
    - Phone number
    - Profile picture
    - Two-factor authentication setting
    """
    
    # Core fields (inherited from AbstractUser)
    # username, email, first_name, last_name, password, is_staff, is_active etc.
    
    # Additional fields for e-commerce
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text='User phone number for contact'
    )
    
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True,
        help_text='User profile picture'
    )
    
    date_of_birth = models.DateField(
        blank=True,
        null=True,
        help_text='User date of birth'
    )
    
    is_verified_email = models.BooleanField(
        default=False,
        help_text='Whether user has verified their email'
    )
    
    is_verified_phone = models.BooleanField(
        default=False,
        help_text='Whether user has verified their phone number'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        # Ordering - newest first
        ordering = ['-created_at']
        # Table name in database
        db_table = 'custom_users'
        # Verbose names for admin panel
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        """Return user's full name or username"""
        return self.get_full_name() or self.username
    
    @property
    def is_complete_profile(self):
        """Check if user has completed their profile"""
        return all([self.phone_number, self.date_of_birth])


# ============================================
# USER ADDRESS MODEL
# ============================================
class Address(models.Model):
    """
    Stores user addresses (shipping and billing addresses).
    Users can have multiple addresses.
    """
    
    ADDRESS_TYPE_CHOICES = [
        ('shipping', 'Shipping Address'),
        ('billing', 'Billing Address'),
        ('both', 'Both Shipping and Billing'),
    ]
    
    # Link to user
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='addresses',  # Access via user.addresses.all()
        help_text='User who owns this address'
    )
    
    # Address details
    address_type = models.CharField(
        max_length=20,
        choices=ADDRESS_TYPE_CHOICES,
        default='shipping',
        help_text='Type of address (shipping/billing)'
    )
    
    full_name = models.CharField(
        max_length=100,
        help_text='Full name for delivery'
    )
    
    phone = models.CharField(
        max_length=20,
        help_text='Contact phone number'
    )
    
    street_address = models.CharField(
        max_length=255,
        help_text='Street name and house number'
    )
    
    city = models.CharField(
        max_length=100,
        help_text='City name'
    )
    
    state_or_province = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='State or province name'
    )
    
    postal_code = models.CharField(
        max_length=20,
        help_text='Postal/zip code'
    )
    
    country = models.CharField(
        max_length=100,
        help_text='Country name'
    )
    
    # Special instructions for delivery
    delivery_instructions = models.TextField(
        blank=True,
        null=True,
        help_text='Special instructions for delivery (e.g., leave package at door)'
    )
    
    # Mark as default
    is_default = models.BooleanField(
        default=False,
        help_text='Use as default address'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_default', '-created_at']
        db_table = 'addresses'
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'
        # Ensure user has only one default address of each type
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'address_type'],
                condition=models.Q(is_default=True),
                name='unique_default_address_per_type'
            )
        ]
    
    def __str__(self):
        """Return formatted address"""
        return f"{self.full_name} - {self.street_address}, {self.city}, {self.country}"


# ============================================
# USER PREFERENCES MODEL
# ============================================
class UserPreferences(models.Model):
    """
    Store user preferences and settings.
    """
    
    # Link to user
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='preferences',  # Access via user.preferences
        help_text='User who owns these preferences'
    )
    
    # Notification preferences
    email_notifications_enabled = models.BooleanField(
        default=True,
        help_text='Receive email notifications'
    )
    
    sms_notifications_enabled = models.BooleanField(
        default=False,
        help_text='Receive SMS notifications'
    )
    
    marketing_emails_enabled = models.BooleanField(
        default=True,
        help_text='Receive marketing emails and offers'
    )
    
    # Theme preferences
    dark_mode_enabled = models.BooleanField(
        default=True,
        help_text='Use dark mode in frontend'
    )
    
    # Language
    language = models.CharField(
        max_length=10,
        default='en',
        choices=[('en', 'English'), ('bn', 'Bengali')],
        help_text='Preferred language'
    )
    
    # Currency for display
    currency = models.CharField(
        max_length=3,
        default='USD',
        help_text='Preferred currency for display'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_preferences'
        verbose_name = 'User Preferences'
        verbose_name_plural = 'User Preferences'
    
    def __str__(self):
        return f"Preferences for {self.user.username}"


# ============================================
# USER ACTIVITY LOG (for audit trail)
# ============================================
class UserActivity(models.Model):
    """
    Track user activities for security and analytics.
    Examples: login, logout, purchase, review, etc.
    """
    
    ACTIVITY_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('register', 'Register'),
        ('purchase', 'Purchase'),
        ('review', 'Review Product'),
        ('wishlist_add', 'Add to Wishlist'),
        ('cart_add', 'Add to Cart'),
        ('password_change', 'Change Password'),
        ('profile_update', 'Update Profile'),
    ]
    
    # User who performed the activity
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='activities',  # Access via user.activities.all()
        help_text='User who performed the activity'
    )
    
    # Activity type
    activity_type = models.CharField(
        max_length=50,
        choices=ACTIVITY_CHOICES,
        help_text='Type of activity'
    )
    
    # Details about the activity
    description = models.TextField(
        blank=True,
        null=True,
        help_text='Additional details about the activity'
    )
    
    # IP address
    ip_address = models.GenericIPAddressField(
        blank=True,
        null=True,
        help_text='IP address of the user'
    )
    
    # User agent (device info)
    user_agent = models.TextField(
        blank=True,
        null=True,
        help_text='Browser or device information'
    )
    
    # Timestamp
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        db_table = 'user_activities'
        verbose_name = 'User Activity'
        verbose_name_plural = 'User Activities'
        # Index for faster queries
        indexes = [
            models.Index(fields=['user', '-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.activity_type} - {self.timestamp}"
