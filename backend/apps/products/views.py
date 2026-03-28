# ============================================
# PRODUCT VIEWS
# ============================================
# API views for product management, listing, search, and filtering.

from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from apps.products.models import Category, Brand, Product, ProductImage, ProductAttribute
from apps.products.serializers import (
    CategorySerializer, BrandSerializer, ProductListSerializer,
    ProductDetailSerializer, ProductCreateUpdateSerializer,
    ProductImageSerializer, ProductAttributeSerializer
)

# ============================================
# CATEGORY VIEWSET
# ============================================
class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoints for product categories.
    GET: List all categories or get category details
    POST/PUT/DELETE: Admin only
    """
    
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    
    def get_permissions(self):
        """Only admin can create/update/delete categories"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


# ============================================
# BRAND VIEWSET
# ============================================
class BrandViewSet(viewsets.ModelViewSet):
    """
    API endpoints for product brands.
    """
    
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    lookup_field = 'slug'
    
    def get_permissions(self):
        """Only admin can modify brands"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


# ============================================
# PRODUCT VIEWSET
# ============================================
class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoints for products.
    
    Endpoints:
    - GET /api/products/ - List products with filters
    - GET /api/products/{slug}/ - Get product details
    - POST /api/products/ - Create product (admin)
    - PUT /api/products/{slug}/ - Update product (admin)
    - DELETE /api/products/{slug}/ - Soft delete product (admin)
    - POST /api/products/{slug}/hard_delete/ - Permanent delete (admin)
    - POST /api/products/{slug}/restore/ - Restore soft deleted product (admin)
    - GET /api/products/{slug}/reviews/ - Get product reviews
    - GET /api/products/{slug}/related/ - Get related products
    """
    
    queryset = Product.objects.all()
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Filter options
    filterset_fields = {
        'category__id': ['exact'],
        'brand__id': ['exact'],
        'price': ['gte', 'lte'],
        'is_featured': ['exact'],
        'average_rating': ['gte'],
    }
    
    # Search fields
    search_fields = ['name', 'description', 'sku', 'brand__name']
    
    # Ordering fields
    ordering_fields = ['created_at', 'price', 'average_rating', 'reviews_count']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Use different serializers for different actions"""
        if self.action == 'retrieve':
            return ProductDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ProductCreateUpdateSerializer
        return ProductListSerializer
    
    def get_permissions(self):
        """Only admin can create/update/delete"""
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'hard_delete', 'restore']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        """Return products - active by default, deleted for staff with flag."""
        qs = Product.objects.all()
        
        # Show deleted products only for staff with deleted flag
        if not (self.request.user.is_staff and self.request.query_params.get('deleted') == 'true'):
            qs = qs.filter(is_deleted=False)
        
        return qs

    def perform_destroy(self, instance):
        """Permanent delete and cleanup media in Cloudinary."""
        instance.hard_delete()

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def restore(self, request, slug=None):
        """Restore a soft-deleted product."""
        product = Product.all_objects.filter(slug=slug, is_deleted=True).first()
        if not product:
            return Response({'detail': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        product.is_deleted = False
        product.deleted_at = None
        product.save(update_fields=['is_deleted', 'deleted_at'])
        serializer = ProductDetailSerializer(product, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def hard_delete(self, request, slug=None):
        """Permanently delete a product."""
        product = Product.all_objects.filter(slug=slug).first()
        if not product:
            return Response({'detail': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        product.hard_delete()
        return Response({'detail': 'Product permanently deleted.'}, status=status.HTTP_204_NO_CONTENT)

    
    @action(detail=True, methods=['get'])
    def reviews(self, request, slug=None):
        """
        Get product reviews.
        
        GET /api/products/{slug}/reviews/
        """
        product = self.get_object()
        reviews = product.reviews.filter(is_approved=True).order_by('-created_at')
        
        # Pagination
        page = self.paginate_queryset(reviews)
        if page is not None:
            from apps.reviews.serializers import ProductReviewDetailSerializer
            serializer = ProductReviewDetailSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        return Response([])
    
    @action(detail=True, methods=['get'])
    def related(self, request, slug=None):
        """
        Get related products (same category, exclude deleted).
        
        GET /api/products/{slug}/related/
        """
        product = self.get_object()
        related = product.category.products.exclude(
            id=product.id, is_deleted=True
        )[:6]
        
        serializer = ProductListSerializer(
            related, 
            many=True, 
            context={'request': request}
        )
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """
        Get featured products (not deleted).
        
        GET /api/products/featured/
        """
        featured = Product.objects.filter(is_featured=True, is_deleted=False)[:8]
        serializer = ProductListSerializer(
            featured, 
            many=True, 
            context={'request': request}
        )
        return Response(serializer.data)


# ============================================
# PRODUCT IMAGE VIEWSET
# ============================================
class ProductImageViewSet(viewsets.ModelViewSet):
    """
    API endpoints for managing product images (admin only).
    """
    
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [permissions.IsAdminUser]


# ============================================
# PRODUCT ATTRIBUTE VIEWSET
# ============================================
class ProductAttributeViewSet(viewsets.ModelViewSet):
    """
    API endpoints for managing product attributes like size, color, etc.
    """
    
    queryset = ProductAttribute.objects.all()
    serializer_class = ProductAttributeSerializer
    permission_classes = [permissions.IsAdminUser]
