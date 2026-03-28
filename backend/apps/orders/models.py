# ============================================
# ORDER MODELS
# ============================================
# Manages orders, order items, and order tracking.

from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from apps.users.models import CustomUser, Address
from apps.products.models import Product

# ============================================
# ORDER MODEL
# ============================================
class Order(models.Model):
    """
    Main order model storing all order information.
    """
    
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('stripe', 'Credit/Debit Card (Stripe)'),
        ('bkash', 'bKash'),
        ('nagad', 'Nagad'),
        ('wallet', 'E-Wallet'),
        ('cod', 'Cash on Delivery'),
    ]
    
    # Link to user (nullable for guest orders)
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders',
        help_text='User who placed the order (null for guest orders)'
    )
    
    # Guest order fields
    customer_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='Customer name for guest orders'
    )
    
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text='Phone number for guest orders'
    )
    
    whatsapp_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text='WhatsApp number for guest orders'
    )
    
    guest_address = models.TextField(
        blank=True,
        null=True,
        help_text='Address for guest orders'
    )
    
    # Order number (unique identifier)
    order_number = models.CharField(
        max_length=100,
        unique=True,
        help_text='Unique order number'
    )
    
    # -------- SHIPPING ADDRESS --------
    shipping_address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        null=True,
        related_name='orders_shipped_to',
        help_text='Shipping address'
    )
    
    # Or store address as JSON if address is deleted
    shipping_address_data = models.JSONField(
        default=dict,
        blank=True,
        help_text='Backup shipping address data'
    )
    
    # -------- PRICING --------
    # Subtotal (sum of all items)
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='Subtotal before tax/shipping'
    )
    
    # Shipping cost
    shipping_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0'),
        help_text='Shipping charges'
    )
    
    # Tax amount
    tax_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0'),
        help_text='Tax amount'
    )
    
    # Discount amount
    discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0'),
        help_text='Discount/coupon amount'
    )
    
    # Total price
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='Final total price'
    )
    
    # -------- COUPON/PROMOTION --------
    coupon_code = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='Applied coupon/promotion code'
    )
    
    # -------- ORDER STATUS --------
    order_status = models.CharField(
        max_length=20,
        choices=ORDER_STATUS_CHOICES,
        default='pending',
        help_text='Current order status'
    )
    
    # -------- PAYMENT --------
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        help_text='Payment method used'
    )
    
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending',
        help_text='Payment status'
    )
    
    # Transaction ID from payment gateway
    transaction_id = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text='Payment gateway transaction ID'
    )
    
    # -------- NOTES --------
    customer_notes = models.TextField(
        blank=True,
        null=True,
        help_text='Special instructions from customer'
    )
    
    admin_notes = models.TextField(
        blank=True,
        null=True,
        help_text='Internal notes for admin'
    )
    
    # -------- TIMESTAMPS --------
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Delivery date
    estimated_delivery_date = models.DateField(
        blank=True,
        null=True,
        help_text='Estimated delivery date'
    )
    
    delivered_at = models.DateTimeField(
        blank=True,
        null=True,
        help_text='Actual delivery time'
    )
    
    class Meta:
        ordering = ['-created_at']
        db_table = 'orders'
        # Index for faster queries
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['order_number']),
            models.Index(fields=['order_status']),
        ]
    
    def __str__(self):
        return f"Order #{self.order_number}"


# ============================================
# ORDER ITEM MODEL
# ============================================
class OrderItem(models.Model):
    """
    Individual items in an order.
    """
    
    # Link to order
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        help_text='Order this item belongs to'
    )
    
    # Link to product
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        help_text='Product ordered'
    )
    
    # Product details (snapshot at time of order)
    product_name = models.CharField(
        max_length=200,
        help_text='Product name at time of order'
    )
    
    product_sku = models.CharField(
        max_length=100,
        help_text='Product SKU at time of order'
    )
    
    # Quantity ordered
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text='Quantity ordered'
    )
    
    # Price per unit at time of order
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0'))],
        help_text='Price per unit when ordered'
    )
    
    # Total price for this item
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='Total for this item'
    )
    
    class Meta:
        db_table = 'order_items'
    
    def __str__(self):
        return f"{self.product_name} x {self.quantity} in Order #{self.order.order_number}"
    
    def save(self, *args, **kwargs):
        """Automatically calculate total price"""
        self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)


# ============================================
# ORDER SHIPMENT TRACKING MODEL
# ============================================
class OrderShipment(models.Model):
    """
    Track shipment information and updates for orders.
    """
    
    SHIPMENT_STATUS_CHOICES = [
        ('processing', 'Processing'),
        ('picked', 'Picked'),
        ('packed', 'Packed'),
        ('dispatched', 'Dispatched'),
        ('in_transit', 'In Transit'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('failed', 'Delivery Failed'),
    ]
    
    # Link to order
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='shipment',
        help_text='Order being shipped'
    )
    
    # Tracking number
    tracking_number = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        null=True,
        help_text='Courier tracking number'
    )
    
    # Courier name
    courier = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='Courier service name'
    )
    
    # Current status
    status = models.CharField(
        max_length=20,
        choices=SHIPMENT_STATUS_CHOICES,
        default='processing',
        help_text='Current shipment status'
    )
    
    # Status updates/events
    status_updates = models.JSONField(
        default=list,
        blank=True,
        help_text='Array of status update events'
    )
    
    # Timestamps
    shipped_at = models.DateTimeField(
        blank=True,
        null=True,
        help_text='When package was shipped'
    )
    
    delivered_at = models.DateTimeField(
        blank=True,
        null=True,
        help_text='When package was delivered'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'order_shipments'
    
    def __str__(self):
        return f"Shipment for Order #{self.order.order_number}"


# ============================================
# ORDER RETURN/REFUND MODEL
# ============================================
class OrderReturn(models.Model):
    """
    Handle product returns and refunds.
    """
    
    RETURN_STATUS_CHOICES = [
        ('requested', 'Return Requested'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('received', 'Received'),
        ('refunded', 'Refunded'),
    ]
    
    RETURN_REASON_CHOICES = [
        ('defective', 'Defective/Damaged'),
        ('wrong_item', 'Wrong Item Received'),
        ('not_as_described', 'Not as Described'),
        ('changed_mind', 'Changed Mind'),
        ('other', 'Other'),
    ]
    
    # Link to order
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='returns',
        help_text='Order this return belongs to'
    )
    
    # Return reason
    reason = models.CharField(
        max_length=50,
        choices=RETURN_REASON_CHOICES,
        help_text='Reason for return'
    )
    
    # Return status
    status = models.CharField(
        max_length=20,
        choices=RETURN_STATUS_CHOICES,
        default='requested',
        help_text='Return status'
    )
    
    # Refund amount
    refund_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='Amount to be refunded'
    )
    
    # Customer comment
    customer_comment = models.TextField(
        blank=True,
        null=True,
        help_text='Customer explanation'
    )
    
    # Admin comment
    admin_comment = models.TextField(
        blank=True,
        null=True,
        help_text='Admin notes'
    )
    
    # Timestamps
    requested_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(blank=True, null=True)
    refunded_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'order_returns'
    
    def __str__(self):
        return f"Return for Order #{self.order.order_number}"
