"""
Product Admin Configuration
Customizes Django admin for product management with advanced features
"""

from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django import forms
from django.conf import settings
from .models import Category, Brand, Product, ProductImage, ProductAttribute
from cloudinary.models import CloudinaryField
import random
from decouple import config


# ============================================
# CATEGORY ADMIN
# ============================================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin configuration for product categories"""
    
    list_display = ['name', 'slug', 'parent_category', 'product_count', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at', 'parent_category']
    search_fields = ['name', 'description']
    readonly_fields = ['slug', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'parent_category')
        }),
        ('Details', {
            'fields': ('description', 'image')
        }),
        ('Settings', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def product_count(self, obj):
        """Display count of products in this category"""
        count = obj.products.count()
        return format_html('<strong>{}</strong> products', count)
    product_count.short_description = 'Products'

    def change_view(self, request, object_id=None, form_url='', extra_context=None):
        """Override change_view to add Cloudinary credentials to template context"""
        extra_context = extra_context or {}
        extra_context['cloudinary_cloud_name'] = config('CLOUDINARY_CLOUD_NAME', default='')
        extra_context['cloudinary_api_key'] = config('CLOUDINARY_API_KEY', default='')
        return super().change_view(request, object_id, form_url, extra_context)


# ============================================
# BRAND ADMIN
# ============================================
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    """Admin configuration for brands"""
    
    list_display = ['name', 'slug', 'product_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['slug', 'created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug')
        }),
        ('Details', {
            'fields': ('description', 'logo')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def product_count(self, obj):
        """Display count of products for this brand"""
        count = obj.products.count()
        return format_html('<strong>{}</strong> products', count)
    product_count.short_description = 'Products'

    def change_view(self, request, object_id=None, form_url='', extra_context=None):
        """Override change_view to add Cloudinary credentials to template context"""
        extra_context = extra_context or {}
        extra_context['cloudinary_cloud_name'] = config('CLOUDINARY_CLOUD_NAME', default='')
        extra_context['cloudinary_api_key'] = config('CLOUDINARY_API_KEY', default='')
        return super().change_view(request, object_id, form_url, extra_context)


# ============================================
# PRODUCT IMAGE INLINE
# ============================================
class ProductImageInline(admin.StackedInline):
    """Inline admin for product images with visual preview"""
    model = ProductImage
    extra = 2
    fields = ['image', 'alt_text', 'order', 'created_at']
    readonly_fields = ['created_at', 'image_preview']
    
    # Use simple file input for image upload
    formfield_overrides = {
        CloudinaryField: {'widget': forms.FileInput(attrs={'accept': 'image/*'})},
    }
    
    def image_preview(self, obj):
        """Display thumbnail preview of the image"""
        if obj and obj.image:
            return format_html(
                '<img src="{}" width="300" height="200" style="object-fit:cover; border-radius:5px;" />',
                obj.image.url
            )
        return mark_safe('<em style="color:gray;">No image uploaded yet</em>')
    image_preview.short_description = 'Preview'


# ============================================
# PRODUCT FORM FOR CLOUDINARY
# ============================================
class ProductAdminForm(forms.ModelForm):
    """Custom form for Product admin with Cloudinary context"""
    
    class Meta:
        model = Product
        fields = [
            'name', 'slug', 'category', 'brand', 'sku', 
            'short_description', 'description',
            'featured_image',
            'price', 'discount_percentage',
            'stock_quantity',
            'is_featured', 'is_active',
            'seo_title', 'seo_description',
        ]
        widgets = {
            'featured_image': forms.FileInput(attrs={
                'accept': 'image/*',
                'class': 'vLargeImageField',
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Configure featured_image field to use simple file input
        # Django's file storage backend (Cloudinary) will handle the upload
        if 'featured_image' in self.fields:
            self.fields['featured_image'].widget = forms.FileInput(attrs={
                'accept': 'image/*',
                'class': 'vLargeImageField',
            })


# ============================================
# PRODUCT ATTRIBUTE INLINE
# ============================================
class ProductAttributeInline(admin.TabularInline):
    """Inline admin for product attributes"""
    model = ProductAttribute
    extra = 1
    fields = ['name', 'value']


# ============================================
# PRODUCT ADMIN
# ============================================
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin configuration for products with advanced features"""
    
    list_display = [
        'thumbnail_preview', 'product_name_display', 'category', 'price_display',
        'discount_percentage', 'discounted_price', 'stock_display', 'sku',
        'average_rating', 'reviews_count', 'is_featured', 'is_active', 'is_deleted', 'created_at'
    ]
    list_filter = [
        'category', 'brand', 'is_featured', 'is_active', 'is_deleted',
        'created_at', 'price', 'stock_quantity', 'discount_percentage'
    ]
    search_fields = ['name', 'description', 'sku', 'slug', 'short_description']
    readonly_fields = [
        'slug', 'average_rating', 'reviews_count', 'discounted_price',
        'created_at', 'updated_at', 'image_preview', 'deleted_at'
    ]

    
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'category', 'brand', 'sku')
        }),
        ('Description', {
            'fields': ('short_description', 'description')
        }),
        ('Featured Image', {
            'fields': ('featured_image', 'image_preview')
        }),
        ('Pricing', {
            'fields': ('price', 'discount_percentage', 'discounted_price')
        }),
        ('Inventory', {
            'fields': ('stock_quantity',)
        }),
        ('Settings', {
            'fields': ('is_featured', 'is_active')
        }),
        ('SEO', {
            'fields': ('seo_title', 'seo_description'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [ProductImageInline, ProductAttributeInline]
    form = ProductAdminForm
    
    actions = [
        'soft_delete_products', 'restore_products', 'hard_delete_products',
        'mark_featured', 'unmark_featured', 'activate_products', 'deactivate_products',
        'apply_discount', 'clear_discount', 'randomize_reviews',
    ]
    
    def product_name_display(self, obj):
        """Display product name with featured indicator"""
        name = obj.name[:50] + '...' if len(obj.name) > 50 else obj.name
        if obj.is_featured:
            return format_html('⭐ <strong>{}</strong>', name)
        return name
    product_name_display.short_description = 'Product Name'

    def thumbnail_preview(self, obj):
        """Display thumbnail preview of featured image"""
        if obj.featured_image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit:cover; border-radius:3px;" />', obj.featured_image.url)
        return 'No image'
    thumbnail_preview.short_description = 'Thumbnail'

    def soft_delete_products(self, request, queryset):
        count = 0
        for product in queryset:
            if not product.is_deleted:
                product.delete()
                count += 1
        self.message_user(request, f'{count} product(s) moved to trash.')
    soft_delete_products.short_description = 'Soft delete selected products'

    def restore_products(self, request, queryset):
        count = 0
        for product in queryset:
            if product.is_deleted:
                product.is_deleted = False
                product.deleted_at = None
                product.save(update_fields=['is_deleted', 'deleted_at'])
                count += 1
        self.message_user(request, f'{count} product(s) restored from trash.')
    restore_products.short_description = 'Restore selected products'

    def hard_delete_products(self, request, queryset):
        count = 0
        for product in queryset:
            if product.is_deleted:
                product.hard_delete()
                count += 1
        self.message_user(request, f'{count} product(s) permanently deleted.')
    hard_delete_products.short_description = 'Permanently delete selected products'

    
    def price_display(self, obj):
        """Display original and discounted price"""
        if obj.discounted_price and obj.discounted_price < obj.price:
            return format_html(
                '<del>${}</del> <strong style="color:green;">${}</strong>',
                obj.price,
                obj.discounted_price,
            )
        return format_html('${}', obj.price)
    price_display.short_description = 'Price'
    
    def stock_display(self, obj):
        """Display stock quantity with color coding"""
        if obj.stock_quantity > 10:
            color = 'green'
        elif obj.stock_quantity > 0:
            color = 'orange'
        else:
            color = 'red'
        return format_html(
            '<span style="color:{}; font-weight:bold;">{}</span>',
            color,
            obj.stock_quantity,
        )
    stock_display.short_description = 'Stock'
    
    def image_preview(self, obj):
        """Display preview of featured image"""
        if obj.featured_image:
            return format_html(
                '<img src="{}" width="200" height="200" style="object-fit:cover; border-radius:5px;" />', 
                obj.featured_image.url
            )
        return "No image"
    image_preview.short_description = 'Image Preview'
    
    def mark_featured(self, request, queryset):
        """Bulk action to mark products as featured"""
        count = queryset.update(is_featured=True)
        self.message_user(request, f'{count} product(s) marked as featured.')
    mark_featured.short_description = 'Mark selected as featured'
    
    def unmark_featured(self, request, queryset):
        """Bulk action to unmark products as featured"""
        count = queryset.update(is_featured=False)
        self.message_user(request, f'{count} product(s) unmarked as featured.')
    unmark_featured.short_description = 'Unmark selected as featured'
    
    def activate_products(self, request, queryset):
        """Bulk action to activate products"""
        count = queryset.update(is_active=True)
        self.message_user(request, f'{count} product(s) activated.')
    activate_products.short_description = 'Activate selected products'
    
    def deactivate_products(self, request, queryset):
        """Bulk action to deactivate products"""
        count = queryset.update(is_active=False)
        self.message_user(request, f'{count} product(s) deactivated.')
    deactivate_products.short_description = 'Deactivate selected products'

    def apply_discount(self, request, queryset):
        """Bulk mark a standard promotional discount (10%%)"""
        for product in queryset:
            product.discount_percentage = 10
            product.save(update_fields=['discount_percentage', 'discounted_price'])
        self.message_user(request, f'{queryset.count()} product(s) set to 10%% discount.')
    apply_discount.short_description = 'Apply 10 percent discount to selected products'

    def clear_discount(self, request, queryset):
        """Bulk clear any discount"""
        for product in queryset:
            product.discount_percentage = 0
            product.discounted_price = product.price
            product.save(update_fields=['discount_percentage', 'discounted_price'])
        self.message_user(request, f'{queryset.count()} product(s) discount cleared.')
    clear_discount.short_description = 'Clear discount for selected products'

    def change_view(self, request, object_id=None, form_url='', extra_context=None):
        """Override change_view to add Cloudinary credentials to template context"""
        extra_context = extra_context or {}
        extra_context['cloudinary_cloud_name'] = config('CLOUDINARY_CLOUD_NAME', default='')
        extra_context['cloudinary_api_key'] = config('CLOUDINARY_API_KEY', default='')
        return super().change_view(request, object_id, form_url, extra_context)

    def randomize_reviews(self, request, queryset):
        """Bulk randomize reviews count for realism"""
        for product in queryset:
            product.reviews_count = random.randint(20, 1000)
            product.save(update_fields=['reviews_count'])
        self.message_user(request, f'{queryset.count()} product(s) review count randomized.')
    randomize_reviews.short_description = 'Randomize reviews for selected products'


# ============================================
# PRODUCT IMAGE ADMIN
# ============================================
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """Admin configuration for product images with visual previews"""
    
    list_display = ['product', 'image_thumbnail', 'alt_text', 'order', 'created_at']
    list_filter = ['created_at', 'product', 'order']
    search_fields = ['product__name', 'alt_text']
    readonly_fields = ['created_at', 'image_preview']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Image Information', {
            'fields': ('product', 'image')
        }),
        ('Preview', {
            'fields': ('image_preview',)
        }),
        ('Settings', {
            'fields': ('alt_text', 'order')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def image_thumbnail(self, obj):
        """Display thumbnail of image in list view"""
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit:cover; border-radius:3px; cursor:pointer;" title="Click to view" loading="lazy" />',
                obj.image.url
            )
        return format_html('<em style="color:gray;">No image</em>')
    image_thumbnail.short_description = 'Thumbnail'
    
    def change_view(self, request, object_id=None, form_url='', extra_context=None):
        """Override change_view to add Cloudinary credentials to template context"""
        extra_context = extra_context or {}
        extra_context['cloudinary_cloud_name'] = config('CLOUDINARY_CLOUD_NAME', default='')
        extra_context['cloudinary_api_key'] = config('CLOUDINARY_API_KEY', default='')
        return super().change_view(request, object_id, form_url, extra_context)
    
    def image_preview(self, obj):
        """Display full preview of image in detail view"""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width:400px; max-height:400px; object-fit:contain; border-radius:8px; border:1px solid #ddd; padding:5px;" />',
                obj.image.url
            )
        return format_html('<em style="color:gray;">No image uploaded</em>')
    image_preview.short_description = 'Image Preview'


# ============================================
# PRODUCT ATTRIBUTE ADMIN
# ============================================
@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    """Admin configuration for product attributes"""
    
    list_display = ['product', 'name', 'value']
    list_filter = ['name']
    search_fields = ['product__name', 'name', 'value']
    
    fieldsets = (
        ('Attribute Information', {
            'fields': ('product', 'name', 'value')
        }),
    )
