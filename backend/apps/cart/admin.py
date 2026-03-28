"""
Cart Admin Configuration
Customizes Django admin for cart and wishlist management
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import Cart, CartItem, Wishlist, WishlistItem


# ============================================
# CART ITEM INLINE
# ============================================
class CartItemInline(admin.TabularInline):
    """Inline admin for cart items"""
    model = CartItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'price_at_addition', 'added_at']
    can_delete = False
    fields = ['product', 'quantity', 'price_at_addition', 'added_at']
    
    def has_add_permission(self, request, obj=None):
        return False


# ============================================
# CART ADMIN
# ============================================
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Admin configuration for shopping carts"""
    
    list_display = ['user', 'item_count_display', 'total_items', 'created_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at', 'total_items']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Cart Information', {
            'fields': ('total_items',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [CartItemInline]
    
    def item_count_display(self, obj):
        """Display number of items in cart"""
        count = obj.cartitems.count()
        return format_html('<strong>{}</strong> items', count)
    item_count_display.short_description = 'Items'


# ============================================
# CART ITEM ADMIN
# ============================================
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """Admin configuration for cart items"""
    
    list_display = ['cart', 'product', 'quantity', 'price_at_addition', 'total_display', 'added_at']
    list_filter = ['added_at', 'cart__user']
    search_fields = ['cart__user__username', 'product__name']
    readonly_fields = ['cart', 'product', 'quantity', 'price_at_addition', 'added_at']
    date_hierarchy = 'added_at'
    
    def total_display(self, obj):
        """Display total price for item"""
        total = obj.quantity * obj.price_at_addition
        return format_html('<strong>${}</strong>', total)
    total_display.short_description = 'Total'
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False


# ============================================
# WISHLIST ITEM INLINE
# ============================================
class WishlistItemInline(admin.TabularInline):
    """Inline admin for wishlist items"""
    model = WishlistItem
    extra = 0
    readonly_fields = ['product', 'added_at']
    fields = ['product', 'added_at']


# ============================================
# WISHLIST ADMIN
# ============================================
@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    """Admin configuration for wishlists"""
    
    list_display = ['user', 'item_count_display', 'created_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [WishlistItemInline]
    
    def item_count_display(self, obj):
        """Display number of items in wishlist"""
        count = obj.wishlistitems.count()
        return format_html('<strong>{}</strong> items', count)
    item_count_display.short_description = 'Items'


# ============================================
# WISHLIST ITEM ADMIN
# ============================================
@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    """Admin configuration for wishlist items"""
    
    list_display = ['wishlist', 'product', 'added_at']
    list_filter = ['added_at', 'wishlist__user']
    search_fields = ['wishlist__user__username', 'product__name']
    readonly_fields = ['wishlist', 'product', 'added_at']
    date_hierarchy = 'added_at'
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
