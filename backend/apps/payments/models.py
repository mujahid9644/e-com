# ============================================
# PAYMENT MODELS
# ============================================
# Manages payment processing and payment history.

from django.db import models
from apps.orders.models import Order
from apps.users.models import CustomUser
from decimal import Decimal

# ============================================
# PAYMENT MODEL
# ============================================
class Payment(models.Model):
    """
    Record of payments made for orders.
    """
    
    PAYMENT_METHOD_CHOICES = [
        ('stripe', 'Stripe'),
        ('bkash', 'bKash'),
        ('nagad', 'Nagad'),
        ('wallet', 'E-Wallet'),
        ('cod', 'Cash on Delivery'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('initiated', 'Payment Initiated'),
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    
    # Link to order
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='payment',
        help_text='Order this payment is for'
    )
    
    # Payment details
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        help_text='Payment method used'
    )
    
    # Amount
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='Amount paid'
    )
    
    # Currency
    currency = models.CharField(
        max_length=3,
        default='USD',
        help_text='Currency code'
    )
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='initiated',
        help_text='Current payment status'
    )
    
    # Transaction ID from gateway
    transaction_id = models.CharField(
        max_length=200,
        unique=True,
        help_text='Unique transaction ID from payment gateway'
    )
    
    # Reference ID
    reference_id = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text='Reference ID from payment gateway'
    )
    
    # Payment gateway response (stored as JSON)
    gateway_response = models.JSONField(
        default=dict,
        blank=True,
        help_text='Complete response from payment gateway'
    )
    
    # Error message (if payment failed)
    error_message = models.TextField(
        blank=True,
        null=True,
        help_text='Error message if payment failed'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        db_table = 'payments'
        indexes = [
            models.Index(fields=['order']),
            models.Index(fields=['transaction_id']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"Payment {self.transaction_id} for Order #{self.order.order_number}"


# ============================================
# COUPON/DISCOUNT MODEL
# ============================================
class Coupon(models.Model):
    """
    Promotional coupons and discount codes.
    """
    
    DISCOUNT_TYPE_CHOICES = [
        ('percentage', 'Percentage Discount'),
        ('fixed', 'Fixed Amount Discount'),
        ('free_shipping', 'Free Shipping'),
    ]
    
    # Coupon code
    code = models.CharField(
        max_length=50,
        unique=True,
        help_text='Unique coupon code'
    )
    
    # Description
    description = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text='Coupon description'
    )
    
    # Discount type
    discount_type = models.CharField(
        max_length=20,
        choices=DISCOUNT_TYPE_CHOICES,
        help_text='Type of discount'
    )
    
    # Discount value
    discount_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='Discount amount or percentage'
    )
    
    # Minimum order amount to use coupon
    minimum_order_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0'),
        help_text='Minimum order amount required'
    )
    
    # Maximum discount amount (for percentage discounts)
    maximum_discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text='Maximum discount amount (for percentage discounts)'
    )
    
    # Usage limit
    usage_limit = models.IntegerField(
        blank=True,
        null=True,
        help_text='Total number of times coupon can be used'
    )
    
    # Uses count
    usage_count = models.IntegerField(
        default=0,
        help_text='Number of times this coupon has been used'
    )
    
    # Per-user limit
    usage_limit_per_user = models.IntegerField(
        default=1,
        help_text='Number of times each user can use this coupon'
    )
    
    # Applicable categories
    applicable_categories = models.TextField(
        blank=True,
        null=True,
        help_text='Comma-separated list of category IDs (leave empty for all)'
    )
    
    # Is active
    is_active = models.BooleanField(
        default=True,
        help_text='Coupon is active and can be used'
    )
    
    # Validity dates
    start_date = models.DateTimeField(help_text='Coupon valid from')
    end_date = models.DateTimeField(help_text='Coupon valid until')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        db_table = 'coupons'
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return self.code
    
    @property
    def is_valid(self):
        """Check if coupon is currently valid"""
        from django.utils import timezone
        now = timezone.now()
        return (
            self.is_active and
            self.start_date <= now <= self.end_date and
            (self.usage_limit is None or self.usage_count < self.usage_limit)
        )


# ============================================
# COUPON USAGE MODEL
# ============================================
class CouponUsage(models.Model):
    """
    Track coupon usage by users.
    """
    
    # Link to coupon
    coupon = models.ForeignKey(
        Coupon,
        on_delete=models.CASCADE,
        related_name='usages',
        help_text='Coupon used'
    )
    
    # Link to user
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='coupon_usages',
        help_text='User who used the coupon'
    )
    
    # Link to order
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text='Order this coupon was used for'
    )
    
    # Discount amount applied
    discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='Discount amount applied'
    )
    
    # Timestamp
    used_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'coupon_usages'
    
    def __str__(self):
        return f"{self.user.username} used {self.coupon.code}"
