# ============================================
# CART SERIALIZERS
# ============================================

from rest_framework import serializers
from apps.cart.models import Cart, CartItem, Wishlist, WishlistItem
from apps.products.models import Product
from apps.products.serializers import ProductListSerializer

# ============================================
# CART ITEM SERIALIZER
# ============================================
class CartItemSerializer(serializers.ModelSerializer):
    """Serializer for items in cart."""
    
    product_detail = ProductListSerializer(source='product', read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    quantity = serializers.IntegerField()
    total_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )
    
    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity', 'price_at_addition',
                  'product_detail', 'total_price']
        read_only_fields = ['id', 'price_at_addition', 'total_price']
    
    def create(self, validated_data):
        """Create or update cart item"""
        product_id = validated_data.pop('product_id')
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise serializers.ValidationError({'product': 'Product not found'})
        
        # Get or create cart item
        cart = self.context['cart']
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={
                'quantity': validated_data.get('quantity', 1),
                'price_at_addition': product.discounted_price or product.price
            }
        )
        
        # If exists, update quantity
        if not created:
            cart_item.quantity += validated_data.get('quantity', 1)
            cart_item.save()
        
        return cart_item


# ============================================
# CART SERIALIZER
# ============================================
class CartSerializer(serializers.ModelSerializer):
    """Serializer for shopping cart."""
    
    items = CartItemSerializer(read_only=True, many=True)
    total_items = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_items', 'total_price', 'updated_at']
        read_only_fields = fields
    
    def get_total_items(self, obj):
        """Get total number of items"""
        return obj.total_items
    
    def get_total_price(self, obj):
        """Get total cart price"""
        return obj.total_price


# ============================================
# WISHLIST ITEM SERIALIZER
# ============================================
class WishlistItemSerializer(serializers.ModelSerializer):
    """Serializer for items in wishlist."""
    
    product_detail = ProductListSerializer(source='product', read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = WishlistItem
        fields = ['id', 'product_id', 'product_detail', 'added_at']
        read_only_fields = ['id', 'added_at']


# ============================================
# WISHLIST SERIALIZER
# ============================================
class WishlistSerializer(serializers.ModelSerializer):
    """Serializer for user's wishlist."""
    
    items = WishlistItemSerializer(read_only=True, many=True)
    
    class Meta:
        model = Wishlist
        fields = ['id', 'items', 'updated_at']
        read_only_fields = fields
