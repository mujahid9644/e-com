# ============================================
# PRODUCT SERIALIZERS
# ============================================
# Serialize product data for API responses.

from rest_framework import serializers
from apps.products.models import (
    Category, Brand, Product, ProductImage, ProductAttribute
)
from apps.reviews.models import ProductReview

# ============================================
# CATEGORY SERIALIZER
# ============================================
class CategorySerializer(serializers.ModelSerializer):
    """Serializer for product categories."""
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'image']
        read_only_fields = ['id', 'slug']


# ============================================
# BRAND SERIALIZER
# ============================================
class BrandSerializer(serializers.ModelSerializer):
    """Serializer for product brands."""
    
    class Meta:
        model = Brand
        fields = ['id', 'name', 'slug', 'logo', 'description']
        read_only_fields = ['id', 'slug']


# ============================================
# PRODUCT ATTRIBUTE SERIALIZER
# ============================================
class ProductAttributeSerializer(serializers.ModelSerializer):
    """Serializer for product attributes (size, color, etc.)."""
    
    class Meta:
        model = ProductAttribute
        fields = ['id', 'name', 'value']
        read_only_fields = ['id']


# ============================================
# PRODUCT IMAGE SERIALIZER
# ============================================
class ProductImageSerializer(serializers.ModelSerializer):
    """Serializer for product gallery images."""
    
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductImage
        fields = ['id', 'image_url', 'alt_text', 'order']
        read_only_fields = ['id']
    
    def get_image_url(self, obj):
        """Get gallery image URL from Cloudinary."""
        if obj.image:
            return obj.image.url
        return None


# ============================================
# PRODUCT REVIEW BASIC SERIALIZER
# ============================================
class ProductReviewBasicSerializer(serializers.ModelSerializer):
    """Basic serializer for product reviews (for product listings)."""
    
    author = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = ProductReview
        fields = ['id', 'rating', 'title', 'author', 'is_verified_purchase']
        read_only_fields = fields


# ============================================
# PRODUCT LIST SERIALIZER
# ============================================
class ProductListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing products (minimal data for performance).
    Used in product listings and search results.
    """
    
    category_name = serializers.CharField(source='category.name', read_only=True)
    brand_name = serializers.CharField(source='brand.name', read_only=True, allow_null=True)
    image_url = serializers.SerializerMethodField()
    discount_percentage = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'price', 'discounted_price',
            'discount_percentage', 'image_url', 'category_name',
            'brand_name', 'is_featured', 'average_rating', 'reviews_count',
            'stock_status', 'is_in_stock', 'is_deleted', 'deleted_at'
        ]
        read_only_fields = fields
    
    def get_image_url(self, obj):
        """Get featured image URL from Cloudinary."""
        if obj.featured_image:
            return obj.featured_image.url
        return f"https://res.cloudinary.com/dw8r48tmq/image/upload/c_fill,h_200,w_200/v1/placeholder"


# ============================================
# PRODUCT DETAIL SERIALIZER
# ============================================
class ProductDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed product information.
    Used in product detail page.
    """
    
    category = CategorySerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    images = ProductImageSerializer(read_only=True, many=True)
    attributes = ProductAttributeSerializer(read_only=True, many=True)
    featured_image_url = serializers.SerializerMethodField()
    recent_reviews = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'short_description',
            'price', 'discounted_price', 'discount_percentage',
            'category', 'brand', 'featured_image_url', 'images', 'attributes',
            'stock_quantity', 'stock_status', 'is_in_stock', 'sku',
            'average_rating', 'reviews_count', 'recent_reviews',
            'is_featured', 'seo_title', 'seo_description', 'is_deleted', 'deleted_at'
        ]
        read_only_fields = fields
    
    def get_featured_image_url(self, obj):
        """Get featured image URL from Cloudinary."""
        if obj.featured_image:
            return obj.featured_image.url
        # Return placeholder if no image
        return f"https://res.cloudinary.com/dw8r48tmq/image/upload/c_fill,h_400,w_400/v1/placeholder"
    
    def get_recent_reviews(self, obj):
        """Get the 5 most recent reviews"""
        reviews = obj.reviews.filter(is_approved=True).order_by('-created_at')[:5]
        return ProductReviewBasicSerializer(reviews, many=True).data


# ============================================
# PRODUCT CREATE/UPDATE SERIALIZER (for admin)
# ============================================
class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating products (admin only).
    """
    
    class Meta:
        model = Product
        fields = [
            'name', 'description', 'short_description', 'category', 'brand',
            'price', 'discount_percentage', 'stock_quantity', 'sku',
            'featured_image', 'is_featured', 'is_active',
            'seo_title', 'seo_description'
        ]
    
    def create(self, validated_data):
        """Create product and auto-generate slug"""
        return Product.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """Update product fields"""
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance
