# ============================================
# REVIEW SERIALIZERS
# ============================================

from rest_framework import serializers
from apps.reviews.models import ProductReview, ReviewImage, ReviewVote
from apps.users.models import CustomUser

# ============================================
# REVIEW IMAGE SERIALIZER
# ============================================
class ReviewImageSerializer(serializers.ModelSerializer):
    """Serializer for review images."""
    
    class Meta:
        model = ReviewImage
        fields = ['id', 'image']
        read_only_fields = ['id']


# ============================================
# REVIEW BASIC SERIALIZER
# ============================================
class ProductReviewBasicSerializer(serializers.ModelSerializer):
    """Basic review info for product listings."""
    
    author = serializers.StringRelatedField(source='user', read_only=True)
    
    class Meta:
        model = ProductReview
        fields = ['id', 'rating', 'title', 'author', 'is_verified_purchase']


# ============================================
# REVIEW DETAIL SERIALIZER
# ============================================
class ProductReviewDetailSerializer(serializers.ModelSerializer):
    """Detailed review serializer."""
    
    author = serializers.StringRelatedField(source='user', read_only=True)
    images = ReviewImageSerializer(read_only=True, many=True)
    
    class Meta:
        model = ProductReview
        fields = [
            'id', 'rating', 'title', 'content', 'author',
            'is_verified_purchase', 'helpful_count', 'unhelpful_count',
            'images', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'helpful_count', 'unhelpful_count', 'created_at', 'updated_at']


# ============================================
# REVIEW CREATE SERIALIZER
# ============================================
class ProductReviewCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new reviews."""
    
    class Meta:
        model = ProductReview
        fields = ['product', 'rating', 'title', 'content']
    
    def create(self, validated_data):
        """Create review for current user"""
        user = self.context['request'].user
        product = validated_data['product']
        
        # Check if user already reviewed this product
        existing_review = ProductReview.objects.filter(
            product=product,
            user=user
        ).exists()
        
        if existing_review:
            raise serializers.ValidationError('You have already reviewed this product.')
        
        # Check if user purchased this product
        from apps.orders.models import OrderItem
        is_verified = OrderItem.objects.filter(
            order__user=user,
            product=product
        ).exists()
        
        validated_data['user'] = user
        validated_data['is_verified_purchase'] = is_verified
        
        return ProductReview.objects.create(**validated_data)
