"""
Orders Admin Configuration
Customizes Django admin for order management
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import Order, OrderItem, OrderShipment, OrderReturn


# ============================================
# ORDER ITEM INLINE
# ============================================
class OrderItemInline(admin.TabularInline):
    """Inline admin for order items"""
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'product_name', 'product_sku', 'quantity', 'unit_price', 'total_price']
    can_delete = False
    fields = ['product', 'product_name', 'quantity', 'unit_price', 'total_price']


# ============================================
# ORDER SHIPMENT INLINE
# ============================================
class OrderShipmentInline(admin.TabularInline):
    """Inline admin for order shipments"""
    model = OrderShipment
    extra = 0
    readonly_fields = ['created_at']


# ============================================
# ORDER ADMIN
# ============================================
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin configuration for orders"""
    
    list_display = [
        'order_number', 'customer_info', 'total_price', 'order_status_colored',
        'created_at'
    ]
    list_filter = ['order_status', 'created_at']
    search_fields = ['order_number', 'user__username', 'user__email', 'customer_name', 'phone_number']
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Order Info', {
            'fields': ('order_number', 'user', 'customer_name', 'phone_number', 'whatsapp_number')
        }),
        ('Status', {
            'fields': ('order_status', 'payment_status')
        }),
        ('Pricing', {
            'fields': ('total_price',)
        }),
        ('Address & Notes', {
            'fields': ('guest_address', 'customer_notes', 'admin_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [OrderItemInline]
    actions = ['mark_confirmed', 'mark_processing', 'mark_cancelled']
    
    def customer_info(self, obj):
        """Display customer info"""
        if obj.user:
            return obj.user.get_full_name() or obj.user.username
        return obj.customer_name or 'Guest'
    customer_info.short_description = 'Customer'
    
    def order_status_colored(self, obj):
        """Display order status with color"""
        colors = {
            'pending': '#FFC107',
            'processing': '#2196F3',
            'shipped': '#673AB7',
            'delivered': '#4CAF50',
            'cancelled': '#F44336',
        }
        color = colors.get(obj.order_status, '#999')
        return format_html(
            '<span style="background-color:{}; color:white; padding:3px 8px; border-radius:3px; font-size:12px;">{}</span>',
            color,
            obj.get_order_status_display()
        )
    order_status_colored.short_description = 'Status'
    
    def payment_status_display(self, obj):
        """Display payment status with color coding"""
        colors = {
            'pending': '#FFC107',
            'completed': '#4CAF50',
            'failed': '#F44336',
            'refunded': '#2196F3',
        }
        color = colors.get(obj.payment_status, '#999')
        return format_html(
            '<span style="background-color:{}; color:white; padding:5px 10px; border-radius:3px;">{}</span>',
            color,
            obj.get_payment_status_display()
        )
    payment_status_display.short_description = 'Payment'
    
    def mark_confirmed(self, request, queryset):
        """Mark selected orders as confirmed"""
        count = queryset.filter(order_status='pending').update(order_status='confirmed')
        self.message_user(request, f'{count} order(s) marked as confirmed.')
    mark_confirmed.short_description = 'Mark as confirmed'
    
    def mark_processing(self, request, queryset):
        """Mark selected orders as processing"""
        count = queryset.update(order_status='processing')
        self.message_user(request, f'{count} order(s) marked as processing.')
    mark_processing.short_description = 'Mark as processing'
    
    def mark_cancelled(self, request, queryset):
        """Mark selected orders as cancelled"""
        count = queryset.update(order_status='cancelled')
        self.message_user(request, f'{count} order(s) marked as cancelled.')
    mark_cancelled.short_description = 'Mark as cancelled'


# ============================================
# ORDER ITEM ADMIN
# ============================================
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Admin configuration for order items"""
    
    list_display = ['order', 'product', 'quantity', 'price_display', 'subtotal_display']
    list_filter = ['order__order_status']
    search_fields = ['order__order_number', 'product__name']
    readonly_fields = ['product_name', 'product_sku', 'unit_price', 'total_price']
    
    def price_display(self, obj):
        """Display item price"""
        return f'${obj.unit_price}'
    price_display.short_description = 'Price'
    
    def subtotal_display(self, obj):
        """Display item subtotal"""
        return f'${obj.total_price}'
    subtotal_display.short_description = 'Subtotal'


# ============================================
# ORDER SHIPMENT ADMIN
# ============================================
@admin.register(OrderShipment)
class OrderShipmentAdmin(admin.ModelAdmin):
    """Admin configuration for order shipments"""
    
    list_display = ['order', 'tracking_number', 'courier', 'status_display', 'delivered_at']
    list_filter = ['status', 'created_at']
    search_fields = ['order__order_number', 'tracking_number']
    readonly_fields = ['created_at', 'updated_at']
    
    def status_display(self, obj):
        """Display shipment status with color"""
        colors = {'processing': '#FFC107', 'dispatched': '#2196F3', 'delivered': '#4CAF50'}
        color = colors.get(obj.status, '#999')
        return format_html(
            '<span style="background-color:{}; color:white; padding:3px 8px; border-radius:3px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_display.short_description = 'Status'


# ============================================
# ORDER RETURN ADMIN
# ============================================
@admin.register(OrderReturn)
class OrderReturnAdmin(admin.ModelAdmin):
    """Admin configuration for order returns"""
    
    list_display = ['order', 'reason_display', 'status_display', 'requested_at']
    list_filter = ['status', 'reason']
    search_fields = ['order__order_number']
    readonly_fields = ['requested_at', 'updated_at']
    
    def reason_display(self, obj):
        """Display return reason"""
        return obj.get_reason_display()
    reason_display.short_description = 'Return Reason'
    
    def status_display(self, obj):
        """Display return status with color"""
        colors = {
            'requested': '#FFC107',
            'approved': '#2196F3',
            'received': '#673AB7',
            'refunded': '#4CAF50',
        }
        color = colors.get(obj.status, '#999')
        return format_html(
            '<span style="background-color:{}; color:white; padding:3px 8px; border-radius:3px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_display.short_description = 'Status'
