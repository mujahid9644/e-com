"""
Payments Admin Configuration
Customizes Django admin for payment tracking and coupon management
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import Payment, Coupon, CouponUsage


# ============================================
# PAYMENT ADMIN
# ============================================
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """Admin configuration for payments"""
    
    list_display = [
        'transaction_id', 'order', 'amount_display', 'payment_method_display',
        'status_display', 'created_at'
    ]
    list_filter = ['payment_method', 'status', 'created_at']
    search_fields = ['transaction_id', 'order__order_number', 'user__username']
    readonly_fields = ['transaction_id', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Payment Information', {
            'fields': ('transaction_id', 'order', 'user', 'payment_method')
        }),
        ('Amount', {
            'fields': ('amount', 'currency', 'processing_fee')
        }),
        ('Status', {
            'fields': ('status', 'status_message')
        }),
        ('Details', {
            'fields': ('gateway_response', 'card_last_four', 'notes'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def amount_display(self, obj):
        """Display payment amount with currency"""
        return format_html('<strong>{} {}</strong>', obj.currency, obj.amount)
    amount_display.short_description = 'Amount'
    
    def payment_method_display(self, obj):
        """Display payment method with icon"""
        icons = {
            'credit_card': '💳',
            'debit_card': '💳',
            'paypal': '🅿️',
            'bkash': '₲',
            'nagad': 'ₙ',
            'cod': '🚚',
            'bank_transfer': '🏦',
        }
        icon = icons.get(obj.payment_method, '💰')
        return format_html('{} {}', icon, obj.get_payment_method_display())
    payment_method_display.short_description = 'Method'
    
    def status_display(self, obj):
        """Display payment status with color coding"""
        colors = {
            'pending': '#FFC107',
            'completed': '#4CAF50',
            'failed': '#F44336',
            'refunded': '#2196F3',
        }
        color = colors.get(obj.status, '#999')
        return format_html(
            '<span style="background-color:{}; color:white; padding:5px 10px; border-radius:3px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_display.short_description = 'Status'


# ============================================
# COUPON USAGE INLINE
# ============================================
class CouponUsageInline(admin.TabularInline):
    """Inline admin for coupon usage tracking"""
    model = CouponUsage
    extra = 0
    readonly_fields = ['user', 'discount_amount', 'used_at']
    can_delete = False


# ============================================
# COUPON ADMIN
# ============================================
@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    """Admin configuration for coupons"""
    
    list_display = [
        'code', 'discount_display', 'usage_count_display', 'is_active_display',
        'end_date', 'created_at'
    ]
    list_filter = ['is_active', 'discount_type', 'created_at']
    search_fields = ['code', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Coupon Information', {
            'fields': ('code', 'description')
        }),
        ('Discount', {
            'fields': ('discount_type', 'discount_value', 'maximum_discount_amount')
        }),
        ('Validity', {
            'fields': ('start_date', 'end_date', 'is_active')
        }),
        ('Usage Limits', {
            'fields': ('usage_limit', 'minimum_order_amount', 'usage_limit_per_user')
        }),
        ('Restrictions', {
            'fields': ('applicable_categories',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [CouponUsageInline]
    actions = ['activate_coupons', 'deactivate_coupons']
    
    def discount_display(self, obj):
        """Display discount information"""
        symbol = '%' if obj.discount_type == 'percentage' else '$'
        return format_html('<strong>{}{}</strong>', obj.discount_value, symbol)
    discount_display.short_description = 'Discount'
    
    def usage_count_display(self, obj):
        """Display coupon usage statistics"""
        used = obj.usage_count
        limit = obj.usage_limit if obj.usage_limit else 'Unlimited'
        return format_html('{} / {}', used, limit)
    usage_count_display.short_description = 'Usage'
    
    def is_active_display(self, obj):
        """Display active status with visual indicator"""
        if obj.is_active:
            return format_html(
                '<span style="color:green; font-weight:bold;">✓ Active</span>'
            )
        return format_html(
            '<span style="color:red; font-weight:bold;">✗ Inactive</span>'
        )
    is_active_display.short_description = 'Status'
    
    def activate_coupons(self, request, queryset):
        """Activate selected coupons"""
        count = queryset.update(is_active=True)
        self.message_user(request, f'{count} coupon(s) activated.')
    activate_coupons.short_description = 'Activate selected coupons'
    
    def deactivate_coupons(self, request, queryset):
        """Deactivate selected coupons"""
        count = queryset.update(is_active=False)
        self.message_user(request, f'{count} coupon(s) deactivated.')
    deactivate_coupons.short_description = 'Deactivate selected coupons'


# ============================================
# COUPON USAGE ADMIN
# ============================================
@admin.register(CouponUsage)
class CouponUsageAdmin(admin.ModelAdmin):
    """Admin configuration for coupon usage tracking"""
    
    list_display = ['coupon', 'user', 'discount_applied_display', 'used_at']
    list_filter = ['coupon', 'used_at']
    search_fields = ['coupon__code', 'user__username', 'user__email']
    readonly_fields = ['coupon', 'user', 'discount_amount', 'used_at']
    date_hierarchy = 'used_at'
    
    def discount_applied_display(self, obj):
        """Display discount amount applied"""
        return format_html('<strong>${}</strong>', obj.discount_amount)
    discount_applied_display.short_description = 'Discount'
