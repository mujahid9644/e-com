# ============================================
# ORDER SERIALIZERS
# ============================================

from rest_framework import serializers
from apps.orders.models import Order, OrderItem, OrderShipment, OrderReturn
from apps.cart.serializers import CartItemSerializer
from apps.users.serializers import AddressSerializer

# ============================================
# ORDER ITEM SERIALIZER
# ============================================
class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for items in an order."""
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product_name', 'product_sku', 'quantity', 
                  'unit_price', 'total_price']
        read_only_fields = fields


# ============================================
# ORDER SHIPMENT SERIALIZER
# ============================================
class OrderShipmentSerializer(serializers.ModelSerializer):
    """Serializer for order shipment tracking."""
    
    class Meta:
        model = OrderShipment
        fields = ['id', 'tracking_number', 'courier', 'status', 
                  'status_updates', 'shipped_at', 'delivered_at']
        read_only_fields = fields


# ============================================
# ORDER RETURN SERIALIZER
# ============================================
class OrderReturnSerializer(serializers.ModelSerializer):
    """Serializer for order returns and refunds."""
    
    class Meta:
        model = OrderReturn
        fields = ['id', 'reason', 'status', 'refund_amount', 
                  'customer_comment', 'admin_comment', 'requested_at']
        read_only_fields = ['id', 'admin_comment', 'requested_at']


# ============================================
# ORDER LIST SERIALIZER
# ============================================
class OrderListSerializer(serializers.ModelSerializer):
    """Serializer for listing orders (minimal data)."""
    
    class Meta:
        model = Order
        fields = ['id', 'order_number', 'total_price', 'order_status', 
                  'payment_status', 'created_at']
        read_only_fields = fields


# ============================================
# ORDER DETAIL SERIALIZER
# ============================================
class OrderDetailSerializer(serializers.ModelSerializer):
    """Detailed order serializer with all information."""
    
    items = OrderItemSerializer(read_only=True, many=True)
    shipping_address = AddressSerializer(read_only=True)
    shipment = OrderShipmentSerializer(read_only=True)
    returns = OrderReturnSerializer(read_only=True, many=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'user', 'items', 'subtotal',
            'shipping_cost', 'tax_amount', 'discount_amount', 'total_price',
            'coupon_code', 'order_status', 'payment_method', 'payment_status',
            'transaction_id', 'shipping_address', 'customer_notes',
            'shipment', 'returns', 'estimated_delivery_date',
            'delivered_at', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'user', 'items', 'subtotal', 'shipping_cost',
            'tax_amount', 'discount_amount', 'total_price', 'coupon_code',
            'order_status', 'payment_status', 'transaction_id', 'shipment',
            'returns', 'estimated_delivery_date', 'delivered_at',
            'created_at', 'updated_at'
        ]


# ============================================
# CREATE ORDER SERIALIZER
# ============================================
class CreateOrderSerializer(serializers.Serializer):
    """Serializer for creating a new order from cart."""
    
    shipping_address_id = serializers.IntegerField()
    payment_method = serializers.ChoiceField(
        choices=['stripe', 'bkash', 'nagad', 'wallet', 'cod']
    )
    coupon_code = serializers.CharField(required=False, allow_blank=True)
    customer_notes = serializers.CharField(required=False, allow_blank=True)
    
    def create(self, validated_data):
        """Create order from user's cart"""
        # This will be implemented in the view
        pass
