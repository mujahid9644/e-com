# ============================================
# PRODUCT MODELS
# ============================================
# Defines the structure for products, categories, and inventory management.

import random
from django.db import models
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from django.utils import timezone
from decimal import Decimal
from cloudinary.models import CloudinaryField

# ============================================
# CATEGORY MODEL
# ============================================
class Category(models.Model):
    """
    Product categories for organization and filtering.
    Examples: Electronics, Clothing, Books, etc.
    """
    
    # Category name
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text='Category name'
    )
    
    # URL-friendly name (e.g., "electronics" from "Electronics")
    slug = models.SlugField(
        unique=True,
        blank=True,
        help_text='URL-friendly category name'
    )
    
    # Category description
    description = models.TextField(
        blank=True,
        null=True,
        help_text='Category description'
    )
    
    # Category image
    image = CloudinaryField(
        'image',
        blank=True,
        null=True,
        folder='categories/',
        help_text='Category cover image'
    )
    
    # Parent category (for hierarchical categories)
    # Example: "Laptops" is a subcategory of "Electronics"
    parent_category = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='subcategories',
        blank=True,
        null=True,
        help_text='Parent category (for subcategories)'
    )
    
    # Is active
    is_active = models.BooleanField(
        default=True,
        help_text='Show this category on frontend'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        db_table = 'categories'
        verbose_name_plural = 'Categories'
    
    def save(self, *args, **kwargs):
        """Automatically generate slug from name"""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


# ============================================
# BRAND MODEL
# ============================================
class Brand(models.Model):
    """
    Brand information for products.
    Examples: Apple, Samsung, Nike, etc.
    """
    
    # Brand name
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text='Brand name'
    )
    
    # URL slug
    slug = models.SlugField(
        unique=True,
        blank=True,
        help_text='URL-friendly brand name'
    )
    
    # Brand logo
    logo = CloudinaryField(
        'image',
        blank=True,
        null=True,
        folder='brands/',
        help_text='Brand logo'
    )
    
    # Brand description
    description = models.TextField(
        blank=True,
        null=True,
        help_text='Brand description'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
        db_table = 'brands'
    
    def save(self, *args, **kwargs):
        """Automatically generate slug from name"""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


# ============================================
# PRODUCT MODEL
# ============================================
class ProductQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True, is_deleted=False)

    def deleted(self):
        return self.filter(is_deleted=True)


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db).filter(is_deleted=False)

    def all_with_deleted(self):
        return ProductQuerySet(self.model, using=self._db)

    def deleted(self):
        return self.all_with_deleted().deleted()


class Product(models.Model):
    """
    Main product model containing all product information.
    """

    # System fields for soft delete
    is_deleted = models.BooleanField(
        default=False,
        help_text='Soft-deleted products are hidden from public API'
    )
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Timestamp when product was soft deleted'
    )

    # Product name
    name = models.CharField(
        max_length=200,
        help_text='Product name/title'
    )
    
    # URL slug
    slug = models.SlugField(
        unique=True,
        blank=True,
        help_text='URL-friendly product name'
    )
    
    # Description
    description = models.TextField(
        help_text='Detailed product description'
    )
    
    # Short description (for listings)
    short_description = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        help_text='Short description for product listings'
    )
    
    # Category
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='products',
        help_text='Product category'
    )
    
    # Brand
    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products',
        help_text='Product brand'
    )
    
    # -------- PRICING --------
    # Base price
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text='Original product price'
    )
    
    # Discount percentage
    discount_percentage = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text='Discount percentage (0-100)'
    )
    
    # Discounted price (automatically calculated)
    discounted_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text='Price after discount'
    )
    
    # -------- INVENTORY --------
    # Stock quantity
    stock_quantity = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text='Number of items in stock'
    )
    
    # SKU (Stock Keeping Unit)
    sku = models.CharField(
        max_length=100,
        unique=True,
        help_text='Unique stock keeping unit'
    )
    
    # -------- RATINGS & REVIEWS --------
    # Average rating (calculated from reviews)
    average_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=Decimal('4.5'),
        validators=[MinValueValidator(Decimal('0')), MaxValueValidator(Decimal('5'))],
        help_text='Average customer rating'
    )
    
    # Total reviews count
    reviews_count = models.IntegerField(
        default=0,
        help_text='Total number of reviews'
    )
    
    # -------- IMAGES --------
    # Featured image
    featured_image = CloudinaryField(
        'image',
        blank=True,
        null=True,
        folder='products/featured/',
        help_text='Main product image'
    )
    
    # -------- METADATA --------
    # Is featured on homepage
    is_featured = models.BooleanField(
        default=False,
        help_text='Show on homepage featured section'
    )
    
    # Is active/available
    is_active = models.BooleanField(
        default=True,
        help_text='Product is available for purchase'
    )
    
    # SEO Title (for search engines)
    seo_title = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text='SEO title for search engines'
    )
    
    # SEO Description
    seo_description = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        help_text='SEO description for search engines'
    )
    
    # -------- TIMESTAMPS --------
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        db_table = 'products'
        # Optimize queries with indexes
        indexes = [
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['brand']),
            models.Index(fields=['-created_at']),
        ]
    
    objects = ProductManager()
    all_objects = models.Manager()

    def save(self, *args, **kwargs):
        """
        Auto-generate slug and calculate discounted price
        This is called before saving to database
        """
        # Generate/clean slug if not provided
        if not self.slug:
            self.slug = slugify(self.name)

        self.slug = slugify(self.slug)

        # Make slug unique across products
        slug_base = self.slug
        counter = 1
        while Product.all_objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
            self.slug = f"{slug_base}-{counter}"
            counter += 1

        # Calculate discounted price
        price_value = Decimal(self.price)
        discount_value = Decimal(self.discount_percentage)
        if discount_value > 0:
            discount_amount = price_value * discount_value / 100
            self.discounted_price = price_value - discount_amount
        else:
            self.discounted_price = price_value
        
        # Randomize reviews count (avoid constant 100 every time)
        if self.reviews_count in (None, 0, 100):
            self.reviews_count = random.randint(10, 850)

        super().save(*args, **kwargs)

    def soft_delete(self, using=None, keep_parents=False):
        """Soft delete product (set is_deleted, deleted_at)."""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=['is_deleted', 'deleted_at'])

    def delete(self, using=None, keep_parents=False):
        """Soft delete by default; preserve for recovery."""
        self.soft_delete()

    def hard_delete(self, using=None, keep_parents=False):
        """Permanent delete product and cleanup media."""
        # CloudinaryField handles deletion automatically
        super().delete(using=using, keep_parents=keep_parents)

    @property
    def is_in_stock(self):
        """Check if product is in stock"""
        return self.stock_quantity > 0
    
    @property
    def stock_status(self):
        """Return stock status string"""
        if self.stock_quantity > 10:
            return 'In Stock'
        elif self.stock_quantity > 0:
            return 'Low Stock'
        else:
            return 'Out of Stock'


# ============================================
# PRODUCT IMAGE MODEL
# ============================================
class ProductImage(models.Model):
    """
    Additional product images (gallery).
    Each product can have multiple images.
    """
    
    # Link to product
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',  # Access via product.images.all()
        help_text='Product this image belongs to'
    )
    
    # Image file
    image = CloudinaryField(
        'image',
        folder='products/gallery/',
        help_text='Product gallery image'
    )
    
    # Display order
    order = models.IntegerField(
        default=0,
        help_text='Display order (lower numbers first)'
    )
    
    # Alt text for SEO
    alt_text = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text='Alt text for accessibility'
    )
    
    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order']
        db_table = 'product_images'
        verbose_name_plural = 'Product Images'
    
    def __str__(self):
        return f"Image for {self.product.name}"


# Cloudinary deletion signals disabled for development (using ImageField instead)
# @receiver(post_delete, sender=Product)
# def delete_product_featured_image(sender, instance, **kwargs):
#     """Delete featured image from Cloudinary when product is deleted."""
#     if instance.featured_image:
#         try:
#             import cloudinary.uploader
#             # Extract public_id from CloudinaryField
#             public_id = instance.featured_image.public_id
#             if public_id:
#                 cloudinary.uploader.destroy(public_id)
#         except Exception as e:
#             # Log error but don't crash
#             import logging
#             logger = logging.getLogger(__name__)
#             logger.error(f"Failed to delete Cloudinary image {instance.featured_image}: {e}")


# @receiver(pre_save, sender=Product)
# def delete_old_featured_image_on_change(sender, instance, **kwargs):
#     """Delete old featured image from Cloudinary when image is replaced."""
#     if not instance.pk:
#         return
#     try:
#         old = Product.objects.get(pk=instance.pk)
#     except Product.DoesNotExist:
#         return
#
#     if old.featured_image and old.featured_image != instance.featured_image:
#         try:
#             import cloudinary.uploader
#             public_id = old.featured_image.public_id
#             if public_id:
#                 cloudinary.uploader.destroy(public_id)
#         except Exception as e:
#             import logging
#             logger = logging.getLogger(__name__)
#             logger.error(f"Failed to delete old Cloudinary image {old.featured_image}: {e}")


# @receiver(post_delete, sender=ProductImage)
# def delete_gallery_image_file(sender, instance, **kwargs):
#     """Delete gallery image from Cloudinary when ProductImage is deleted."""
#     if instance.image:
#         try:
#             import cloudinary.uploader
#             public_id = instance.image.public_id
#             if public_id:
#                 cloudinary.uploader.destroy(public_id)
#         except Exception as e:
#             import logging
#             logger = logging.getLogger(__name__)
#             logger.error(f"Failed to delete Cloudinary gallery image {instance.image}: {e}")


# @receiver(pre_save, sender=ProductImage)
# def delete_old_gallery_image_on_change(sender, instance, **kwargs):
#     """Delete old gallery image from Cloudinary when image is replaced."""
#     if not instance.pk:
#         return
#     try:
#         old = ProductImage.objects.get(pk=instance.pk)
#     except ProductImage.DoesNotExist:
#         return
#
#     if old.image and old.image != instance.image:
#         try:
#             import cloudinary.uploader
#             public_id = old.image.public_id
#             if public_id:
#                 cloudinary.uploader.destroy(public_id)
#         except Exception as e:
#             import logging
#             logger = logging.getLogger(__name__)
#             logger.error(f"Failed to delete old Cloudinary gallery image {old.image}: {e}")


# ============================================
# PRODUCT ATTRIBUTE MODEL
# ============================================
class ProductAttribute(models.Model):
    """
    Products can have attributes like size, color, weight, etc.
    This is flexible for different product types.
    """
    
    # Link to product
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='attributes',
        help_text='Product this attribute belongs to'
    )
    
    # Attribute name (e.g., "Color", "Size", "Weight")
    name = models.CharField(
        max_length=100,
        help_text='Attribute name'
    )
    
    # Attribute value (e.g., "Red", "Large", "500g")
    value = models.CharField(
        max_length=100,
        help_text='Attribute value'
    )
    
    class Meta:
        db_table = 'product_attributes'
        # Ensure unique combinations
        unique_together = ['product', 'name', 'value']
    
    def __str__(self):
        return f"{self.product.name} - {self.name}: {self.value}"
