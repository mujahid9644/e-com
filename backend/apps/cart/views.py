# ============================================
# CART VIEWS
# ============================================

from rest_framework import status, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.cart.models import Cart, CartItem, Wishlist, WishlistItem
from apps.cart.serializers import CartItemSerializer, CartSerializer, WishlistSerializer
from apps.products.models import Product

# ============================================
# CART VIEWSET
# ============================================
class CartViewSet(viewsets.ViewSet):
    """
    API endpoints for shopping cart management.
    
    Endpoints:
    - GET /api/cart/view/ - Get cart
    - POST /api/cart/add/ - Add item to cart
    - POST /api/cart/remove/ - Remove item from cart
    - POST /api/cart/update/ - Update item quantity
    - POST /api/cart/clear/ - Clear entire cart
    """
    
    permission_classes = [permissions.IsAuthenticated]
    
    def _get_or_create_cart(self, user):
        """Get or create cart for user"""
        cart, created = Cart.objects.get_or_create(user=user)
        return cart
    
    @action(detail=False, methods=['get'])
    def view(self, request):
        """
        Get current user's cart.
        
        GET /api/cart/view/
        """
        cart = self._get_or_create_cart(request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def add(self, request):
        """
        Add item to cart or update quantity if exists.
        
        POST /api/cart/add/
        Body: {product_id, quantity}
        """
        cart = self._get_or_create_cart(request.user)
        
        try:
            product_id = request.data.get('product_id')
            quantity = int(request.data.get('quantity', 1))
            
            if quantity < 1:
                return Response(
                    {'error': 'Quantity must be at least 1'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            product = Product.objects.get(id=product_id, is_active=True)
            
            # Check stock
            if not product.is_in_stock:
                return Response(
                    {'error': 'Product is out of stock'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if quantity > product.stock_quantity:
                return Response(
                    {'error': f'Only {product.stock_quantity} items available'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Add or update cart item
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={
                    'quantity': quantity,
                    'price_at_addition': product.discounted_price or product.price
                }
            )
            
            if not created:
                # Item already in cart, increase quantity
                cart_item.quantity += quantity
                cart_item.save()
            
            return Response(
                {'message': 'Item added to cart'},
                status=status.HTTP_201_CREATED
            )
        
        except Product.DoesNotExist:
            return Response(
                {'error': 'Product not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['post'])
    def remove(self, request):
        """
        Remove item from cart.
        
        POST /api/cart/remove/
        Body: {product_id}
        """
        cart = self._get_or_create_cart(request.user)
        product_id = request.data.get('product_id')
        
        try:
            CartItem.objects.get(cart=cart, product_id=product_id).delete()
            return Response({'message': 'Item removed from cart'})
        except CartItem.DoesNotExist:
            return Response(
                {'error': 'Item not in cart'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['post'])
    def update_item_quantity(self, request):
        """
        Update item quantity in cart.
        
        POST /api/cart/update_item_quantity/
        Body: {product_id, quantity}
        """
        cart = self._get_or_create_cart(request.user)
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        
        if quantity < 0:
            return Response(
                {'error': 'Quantity must be 0 or positive'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
            
            if quantity == 0:
                # Remove item if quantity is 0
                cart_item.delete()
                return Response({'message': 'Item removed from cart'})
            
            cart_item.quantity = quantity
            cart_item.save()
            return Response({'message': 'Cart updated'})
        
        except CartItem.DoesNotExist:
            return Response(
                {'error': 'Item not in cart'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['post'])
    def clear(self, request):
        """
        Clear entire cart.
        
        POST /api/cart/clear/
        """
        cart = self._get_or_create_cart(request.user)
        cart.items.all().delete()
        return Response({'message': 'Cart cleared'})


# ============================================
# WISHLIST VIEWSET
# ============================================
class WishlistViewSet(viewsets.ViewSet):
    """
    API endpoints for wishlist management.
    """
    
    permission_classes = [permissions.IsAuthenticated]
    
    def _get_or_create_wishlist(self, user):
        """Get or create wishlist for user"""
        wishlist, created = Wishlist.objects.get_or_create(user=user)
        return wishlist
    
    @action(detail=False, methods=['get'])
    def view(self, request):
        """Get user's wishlist"""
        wishlist = self._get_or_create_wishlist(request.user)
        serializer = WishlistSerializer(wishlist)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def add(self, request):
        """Add product to wishlist"""
        wishlist = self._get_or_create_wishlist(request.user)
        product_id = request.data.get('product_id')
        
        try:
            product = Product.objects.get(id=product_id)
            WishlistItem.objects.get_or_create(wishlist=wishlist, product=product)
            return Response({'message': 'Added to wishlist'}, status=status.HTTP_201_CREATED)
        except Product.DoesNotExist:
            return Response(
                {'error': 'Product not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['post'])
    def remove(self, request):
        """Remove product from wishlist"""
        wishlist = self._get_or_create_wishlist(request.user)
        product_id = request.data.get('product_id')
        
        try:
            WishlistItem.objects.get(wishlist=wishlist, product_id=product_id).delete()
            return Response({'message': 'Removed from wishlist'})
        except WishlistItem.DoesNotExist:
            return Response(
                {'error': 'Item not in wishlist'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['post'])
    def is_in_wishlist(self, request):
        """Check if product is in wishlist"""
        wishlist = self._get_or_create_wishlist(request.user)
        product_id = request.data.get('product_id')
        
        exists = WishlistItem.objects.filter(
            wishlist=wishlist,
            product_id=product_id
        ).exists()
        
        return Response({'in_wishlist': exists})
