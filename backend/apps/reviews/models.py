# ============================================
# REVIEW MODELS
# ============================================
# Manages product reviews and ratings from customers.

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.products.models import Product
from apps.users.models import CustomUser
from decimal import Decimal

# ============================================
# PRODUCT REVIEW MODEL
# ============================================
class ProductReview(models.Model):
    """
    Customer reviews and ratings for products.
    """
    
    # Link to product
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews',
        help_text='Product being reviewed'
    )
    
    # Link to user
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='reviews',
        help_text='User who wrote the review'
    )
    
    # Rating (1-5 stars)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='Rating from 1 to 5 stars'
    )
    
    # Review title
    title = models.CharField(
        max_length=200,
        help_text='Short review title'
    )
    
    # Review content
    content = models.TextField(
        help_text='Detailed review content'
    )
    
    # Is this a verified purchase?
    is_verified_purchase = models.BooleanField(
        default=False,
        help_text='User actually purchased this product'
    )
    
    # Helpful votes
    helpful_count = models.IntegerField(
        default=0,
        help_text='Number of "helpful" votes'
    )
    
    unhelpful_count = models.IntegerField(
        default=0,
        help_text='Number of "unhelpful" votes'
    )
    
    # Is visible/approved
    is_approved = models.BooleanField(
        default=True,
        help_text='Admin approval for review visibility'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-helpful_count', '-created_at']
        db_table = 'product_reviews'
        # Prevent duplicate reviews from same user for same product
        unique_together = ['product', 'user']
        # Optimize with indexes
        indexes = [
            models.Index(fields=['product', '-created_at']),
            models.Index(fields=['user']),
        ]
    
    def __str__(self):
        return f"Review of {self.product.name} by {self.user.username}"


# ============================================
# REVIEW IMAGE MODEL
# ============================================
class ReviewImage(models.Model):
    """
    Images uploaded with product reviews.
    Customers can attach photos of the product.
    """
    
    # Link to review
    review = models.ForeignKey(
        ProductReview,
        on_delete=models.CASCADE,
        related_name='images',
        help_text='Review this image belongs to'
    )
    
    # Image file
    image = models.ImageField(
        upload_to='review_images/',
        help_text='Review image'
    )
    
    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'review_images'
    
    def __str__(self):
        return f"Image for review by {self.review.user.username}"


# ============================================
# REVIEW HELPFUL/UNHELPFUL MODEL
# ============================================
class ReviewVote(models.Model):
    """
    Track helpful/unhelpful votes on reviews.
    """
    
    VOTE_TYPE_CHOICES = [
        ('helpful', 'Helpful'),
        ('unhelpful', 'Unhelpful'),
    ]
    
    # Link to review
    review = models.ForeignKey(
        ProductReview,
        on_delete=models.CASCADE,
        related_name='votes',
        help_text='Review being voted on'
    )
    
    # User voting
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        help_text='User who voted'
    )
    
    # Vote type
    vote_type = models.CharField(
        max_length=20,
        choices=VOTE_TYPE_CHOICES,
        help_text='Type of vote'
    )
    
    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'review_votes'
        # One vote per user per review
        unique_together = ['review', 'user']
    
    def __str__(self):
        return f"{self.user.username} marked review as {self.vote_type}"
