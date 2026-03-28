# ============================================
# CART MODELS
# ============================================
# Manages shopping cart items for users.

from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from apps.users.models import CustomUser
from apps.products.models import Product

# ============================================
# CART MODEL
# ============================================
class Cart(models.Model):
    """
    Shopping cart for each user.
    Each user has one active cart.
    """
    
    # Link to user
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='cart',
        help_text='User who owns this cart'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'carts'
    
    def __str__(self):
        return f"Cart for {self.user.username}"
    
    @property
    def total_items(self):
        """Get total number of items in cart"""
        return sum(item.quantity for item in self.items.all())
    
    @property
    def total_price(self):
        """Calculate total cart price"""
        return sum(item.total_price for item in self.items.all())


# ============================================
# CART ITEM MODEL
# ============================================
class CartItem(models.Model):
    """
    An item in the shopping cart.
    """
    
    # Link to cart
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        help_text='Cart this item belongs to'
    )
    
    # Link to product
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='cart_items',
        help_text='Product in cart'
    )
    
    # Quantity
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        help_text='Number of items'
    )
    
    # Price at time of adding (product price can change)
    price_at_addition = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='Product price when added to cart'
    )
    
    # Timestamps
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'cart_items'
        # Ensure no duplicate products in same cart
        unique_together = ['cart', 'product']
    
    def __str__(self):
        return f"{self.product.name} - Qty: {self.quantity}"
    
    @property
    def total_price(self):
        """Calculate total price for this cart item"""
        return self.quantity * self.price_at_addition


# ============================================
# WISHLIST MODEL
# ============================================
class Wishlist(models.Model):
    """
    User's wishlist of favorite products.
    """
    
    # Link to user
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='wishlist',
        help_text='User who owns this wishlist'
    )
    
    # Products in wishlist
    products = models.ManyToManyField(
        Product,
        related_name='wishlists',
        through='WishlistItem',
        help_text='Products in wishlist'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'wishlists'
        verbose_name_plural = 'Wishlists'
    
    def __str__(self):
        return f"Wishlist for {self.user.username}"


# ============================================
# WISHLIST ITEM MODEL
# ============================================
class WishlistItem(models.Model):
    """
    Individual items in a wishlist.
    """
    
    # Link to wishlist
    wishlist = models.ForeignKey(
        Wishlist,
        on_delete=models.CASCADE,
        related_name='items',
        help_text='Wishlist this item belongs to'
    )
    
    # Link to product
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        help_text='Product in wishlist'
    )
    
    # Timestamp
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'wishlist_items'
        # Ensure no duplicate products in same wishlist
        unique_together = ['wishlist', 'product']
    
    def __str__(self):
        return f"{self.product.name} in {self.wishlist.user.username}'s wishlist"
