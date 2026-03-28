"""
Reviews Admin Configuration
Customizes Django admin for product reviews management
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import ProductReview, ReviewImage, ReviewVote


# ============================================
# REVIEW IMAGE INLINE
# ============================================
class ReviewImageInline(admin.TabularInline):
    """Inline admin for review images"""
    model = ReviewImage
    extra = 1
    fields = ['image', 'image_thumbnail']
    readonly_fields = ['image_thumbnail']
    
    def image_thumbnail(self, obj):
        """Display thumbnail"""
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius:5px;" />', obj.image.url
            )
        return "No image"
    image_thumbnail.short_description = 'Preview'


# ============================================
# PRODUCT REVIEW ADMIN
# ============================================
@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    """Admin configuration for product reviews"""
    
    list_display = [
        'product', 'user', 'rating_display', 'title_display', 
        'is_verified_display', 'helpful_count_display', 'created_at'
    ]
    list_filter = ['rating', 'is_verified_purchase', 'created_at']
    search_fields = ['product__name', 'user__username', 'title', 'content']
    readonly_fields = ['helpful_count', 'unhelpful_count', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Review Information', {
            'fields': ('product', 'user', 'rating')
        }),
        ('Content', {
            'fields': ('title', 'content')
        }),
        ('Verification', {
            'fields': ('is_verified_purchase',)
        }),
        ('Engagement', {
            'fields': ('helpful_count', 'unhelpful_count')
        }),
        ('Approval', {
            'fields': ('is_approved',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [ReviewImageInline]
    actions = ['mark_verified', 'mark_unverified']
    
    def rating_display(self, obj):
        """Display rating with stars"""
        stars = '⭐' * int(obj.rating) + '☆' * (5 - int(obj.rating))
        return format_html('{} <strong>{}/5</strong>', stars, obj.rating)
    rating_display.short_description = 'Rating'
    
    def title_display(self, obj):
        """Display review title truncated"""
        title = obj.title[:50] + '...' if len(obj.title) > 50 else obj.title
        return title
    title_display.short_description = 'Title'
    
    def is_verified_display(self, obj):
        """Display verified purchase status"""
        if obj.is_verified_purchase:
            return format_html('<span style="color:green; font-weight:bold;">{}</span>', '✓ Verified')
        return format_html('<span style="color:gray;">{}</span>', 'Not Verified')
    is_verified_display.short_description = 'Verified Purchase'
    
    def helpful_count_display(self, obj):
        """Display helpful vote statistics"""
        total_votes = obj.helpful_count + obj.unhelpful_count
        if total_votes == 0:
            return "No votes"
        return format_html('👍 {} / 👎 {}', obj.helpful_count, obj.unhelpful_count)
    helpful_count_display.short_description = 'Helpful Votes'
    
    def mark_verified(self, request, queryset):
        """Mark reviews as verified purchases"""
        count = queryset.update(is_verified_purchase=True)
        self.message_user(request, f'{count} review(s) marked as verified.')
    mark_verified.short_description = 'Mark as verified purchase'
    
    def mark_unverified(self, request, queryset):
        """Mark reviews as unverified"""
        count = queryset.update(is_verified_purchase=False)
        self.message_user(request, f'{count} review(s) marked as unverified.')
    mark_unverified.short_description = 'Mark as unverified'


# ============================================
# REVIEW IMAGE ADMIN
# ============================================
@admin.register(ReviewImage)
class ReviewImageAdmin(admin.ModelAdmin):
    """Admin configuration for review images"""
    
    list_display = ['review', 'image_thumbnail', 'created_at']
    list_filter = ['created_at', 'review__product']
    search_fields = ['review__title', 'review__product__name']
    readonly_fields = ['created_at', 'image_preview']
    
    def image_thumbnail(self, obj):
        """Display thumbnail of image"""
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius:5px;" />', obj.image.url
            )
        return "No image"
    image_thumbnail.short_description = 'Thumbnail'
    
    def image_preview(self, obj):
        """Display full preview of image"""
        if obj.image:
            return format_html(
                '<img src="{}" width="300" />', obj.image.url
            )
        return "No image"
    image_preview.short_description = 'Preview'


# ============================================
# REVIEW VOTE ADMIN (Read-only for tracking)
# ============================================
@admin.register(ReviewVote)
class ReviewVoteAdmin(admin.ModelAdmin):
    """Admin configuration for review votes (tracking only)"""
    
    list_display = ['review', 'user', 'vote_type_display', 'created_at']
    list_filter = ['vote_type', 'created_at']
    search_fields = ['review__title', 'user__username']
    readonly_fields = ['review', 'user', 'vote_type', 'created_at']
    date_hierarchy = 'created_at'
    
    # Prevent adding/deleting votes from admin
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def vote_type_display(self, obj):
        """Display vote type with emoji"""
        if obj.vote_type == 'upvote':
            return format_html('<span style="color:green; font-weight:bold;">👍 Upvote</span>')
        return format_html('<span style="color:red; font-weight:bold;">👎 Downvote</span>')
    vote_type_display.short_description = 'Vote Type'
