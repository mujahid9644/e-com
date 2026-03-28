"""
Users Admin Configuration
Customizes Django admin for user management
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import CustomUser, Address, UserPreferences, UserActivity


# ============================================
# ADDRESS INLINE
# ============================================
class AddressInline(admin.TabularInline):
    """Inline admin for user addresses"""
    model = Address
    extra = 1
    fields = ['full_name', 'phone', 'street_address', 'city', 'postal_code', 'country', 'is_default']


# ============================================
# CUSTOM USER ADMIN
# ============================================
@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """Admin configuration for custom users"""
    
    list_display = [
        'username', 'email', 'full_name_display', 'phone_number', 'is_verified_display',
        'is_active_display', 'date_joined'
    ]
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'date_joined', 'is_verified_email')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone_number')
    readonly_fields = ('created_at', 'updated_at', 'date_joined', 'last_login', 'profile_picture_preview')
    date_hierarchy = 'date_joined'
    
    fieldsets = (
        ('Authentication', {
            'fields': ('username', 'password')
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone_number', 'date_of_birth')
        }),
        ('Profile', {
            'fields': ('profile_picture', 'profile_picture_preview')
        }),
        ('Verification Status', {
            'fields': ('is_verified_email', 'is_verified_phone')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Important Dates', {
            'fields': ('date_joined', 'last_login'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [AddressInline]
    actions = ['verify_email', 'activate_users', 'deactivate_users']
    
    def full_name_display(self, obj):
        """Display user's full name"""
        full_name = obj.get_full_name()
        return full_name if full_name else '—'
    full_name_display.short_description = 'Full Name'
    
    def is_verified_display(self, obj):
        """Display email verification status"""
        if obj.is_verified_email:
            return format_html('<span style="color:green; font-weight:bold;">{}</span>', '✓ Verified')
        return format_html('<span style="color:red; font-weight:bold;">{}</span>', '✗ Not Verified')
    is_verified_display.short_description = 'Email Verified'
    
    def is_active_display(self, obj):
        """Display active status"""
        if obj.is_active:
            return format_html('<span style="color:green; font-weight:bold;">{}</span>', '✓ Active')
        return format_html('<span style="color:red; font-weight:bold;">{}</span>', '✗ Inactive')
    is_active_display.short_description = 'Status'
    
    def profile_picture_preview(self, obj):
        """Display preview of profile picture"""
        if obj.profile_picture:
            return format_html(
                '<img src="{}" width="150" height="150" style="border-radius:10px;" />',
                obj.profile_picture.url
            )
        return "No profile picture"
    profile_picture_preview.short_description = 'Profile Picture'
    
    def verify_email(self, request, queryset):
        """Mark users as verified"""
        count = queryset.update(is_verified_email=True)
        self.message_user(request, f'{count} user(s) verified.')
    verify_email.short_description = 'Mark email as verified'
    
    def activate_users(self, request, queryset):
        """Activate selected users"""
        count = queryset.update(is_active=True)
        self.message_user(request, f'{count} user(s) activated.')
    activate_users.short_description = 'Activate selected users'
    
    def deactivate_users(self, request, queryset):
        """Deactivate selected users"""
        count = queryset.update(is_active=False)
        self.message_user(request, f'{count} user(s) deactivated.')
    deactivate_users.short_description = 'Deactivate selected users'


# ============================================
# ADDRESS ADMIN
# ============================================
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    """Admin configuration for user addresses"""
    
    list_display = ['user', 'full_name', 'address_type', 'city', 'country', 'is_default']
    list_filter = ['address_type', 'country', 'is_default', 'created_at']
    search_fields = ['user__username', 'full_name', 'city', 'street_address']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User & Type', {
            'fields': ('user', 'address_type', 'is_default')
        }),
        ('Contact Information', {
            'fields': ('full_name', 'phone')
        }),
        ('Address', {
            'fields': ('street_address', 'city', 'state_or_province', 'postal_code', 'country')
        }),
        ('Special Instructions', {
            'fields': ('delivery_instructions',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# ============================================
# USER PREFERENCES ADMIN
# ============================================
@admin.register(UserPreferences)
class UserPreferencesAdmin(admin.ModelAdmin):
    """Admin configuration for user preferences"""
    
    list_display = ['user', 'language', 'currency', 'dark_mode_enabled', 'email_notifications_enabled']
    list_filter = ['language', 'currency', 'dark_mode_enabled', 'email_notifications_enabled']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Site Preferences', {
            'fields': ('language', 'currency', 'dark_mode_enabled')
        }),
        ('Notifications', {
            'fields': ('email_notifications_enabled', 'sms_notifications_enabled', 'marketing_emails_enabled')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# ============================================
# USER ACTIVITY ADMIN
# ============================================
@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    """Admin configuration for user activity tracking"""
    
    list_display = ['user', 'activity_type', 'timestamp', 'ip_address']
    list_filter = ['activity_type', 'timestamp']
    search_fields = ['user__username', 'ip_address']
    readonly_fields = ['user', 'activity_type', 'ip_address', 'timestamp']
    date_hierarchy = 'timestamp'
    
    # Prevent modifications from admin
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
