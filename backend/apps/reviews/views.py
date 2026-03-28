# ============================================
# REVIEW VIEWS
# ============================================

from rest_framework import status, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.reviews.models import ProductReview, ReviewVote
from apps.reviews.serializers import (
    ProductReviewDetailSerializer,
    ProductReviewCreateSerializer
)
from apps.products.models import Product

# ============================================
# PRODUCT REVIEW VIEWSET
# ============================================
class ProductReviewViewSet(viewsets.ModelViewSet):
    """
    API endpoints for product reviews.
    
    Endpoints:
    - POST /api/reviews/ - Create a review
    - GET /api/reviews/{id}/ - Get review details
    - PUT /api/reviews/{id}/ - Update review (own only)
    - DELETE /api/reviews/{id}/ - Delete review (own only)
    - POST /api/reviews/{id}/mark_helpful/ - Mark review as helpful
    - POST /api/reviews/{id}/mark_unhelpful/ - Mark review as unhelpful
    """
    
    def get_queryset(self):
        """Get only approved reviews by default"""
        return ProductReview.objects.filter(is_approved=True).order_by('-created_at')
    
    def get_serializer_class(self):
        """Use different serializer for creation"""
        if self.action == 'create':
            return ProductReviewCreateSerializer
        return ProductReviewDetailSerializer
    
    def get_permissions(self):
        """Adjust permissions based on action"""
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]
    
    def perform_create(self, serializer):
        """Create review for current user"""
        serializer.save(user=self.request.user)
    
    def perform_update(self, serializer):
        """Update review - only user's own reviews"""
        review = self.get_object()
        if review.user != self.request.user:
            raise permissions.PermissionDenied("You can only edit your own reviews.")
        serializer.save()
    
    def perform_destroy(self, instance):
        """Delete review - only user's own reviews"""
        if instance.user != self.request.user:
            raise permissions.PermissionDenied("You can only delete your own reviews.")
        instance.delete()
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def mark_helpful(self, request, pk=None):
        """Mark review as helpful"""
        review = self.get_object()
        
        # Check if user already voted
        existing_vote = ReviewVote.objects.filter(
            review=review,
            user=request.user
        ).first()
        
        if existing_vote:
            if existing_vote.vote_type == 'helpful':
                existing_vote.delete()
                review.helpful_count -= 1
            else:
                existing_vote.vote_type = 'helpful'
                existing_vote.save()
                review.helpful_count += 1
                review.unhelpful_count -= 1
        else:
            ReviewVote.objects.create(
                review=review,
                user=request.user,
                vote_type='helpful'
            )
            review.helpful_count += 1
        
        review.save()
        return Response({'helpful_count': review.helpful_count})
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def mark_unhelpful(self, request, pk=None):
        """Mark review as unhelpful"""
        review = self.get_object()
        
        existing_vote = ReviewVote.objects.filter(
            review=review,
            user=request.user
        ).first()
        
        if existing_vote:
            if existing_vote.vote_type == 'unhelpful':
                existing_vote.delete()
                review.unhelpful_count -= 1
            else:
                existing_vote.vote_type = 'unhelpful'
                existing_vote.save()
                review.unhelpful_count += 1
                review.helpful_count -= 1
        else:
            ReviewVote.objects.create(
                review=review,
                user=request.user,
                vote_type='unhelpful'
            )
            review.unhelpful_count += 1
        
        review.save()
        return Response({'unhelpful_count': review.unhelpful_count})
