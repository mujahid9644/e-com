# ============================================
# PAYMENT SERIALIZERS
# ============================================

from rest_framework import serializers
from apps.payments.models import Payment, Coupon, CouponUsage

# ============================================
# PAYMENT SERIALIZER
# ============================================
class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for payment records."""
    
    class Meta:
        model = Payment
        fields = [
            'id', 'order', 'payment_method', 'amount', 'currency',
            'status', 'transaction_id', 'reference_id', 'created_at', 'completed_at'
        ]
        read_only_fields = [
            'id', 'status', 'transaction_id', 'reference_id', 'created_at', 'completed_at'
        ]


# ============================================
# COUPON SERIALIZER
# ============================================
class CouponSerializer(serializers.ModelSerializer):
    """Serializer for displaying coupon information."""
    
    is_valid_coupon = serializers.SerializerMethodField()
    
    class Meta:
        model = Coupon
        fields = [
            'id', 'code', 'description', 'discount_type', 'discount_value',
            'minimum_order_amount', 'maximum_discount_amount',
            'is_active', 'start_date', 'end_date', 'is_valid_coupon'
        ]
        read_only_fields = fields
    
    def get_is_valid_coupon(self, obj):
        """Check if coupon is valid"""
        return obj.is_valid


# ============================================
# COUPON VALIDATION SERIALIZER
# ============================================
class CouponValidationSerializer(serializers.Serializer):
    """Serializer for validating and applying coupons."""
    
    code = serializers.CharField(max_length=50)
    order_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    
    def validate_code(self, value):
        """Validate coupon code exists"""
        try:
            Coupon.objects.get(code=value.upper())
        except Coupon.DoesNotExist:
            raise serializers.ValidationError('Coupon code not found.')
        return value.upper()
    
    def validate(self, attrs):
        """Validate coupon is applicable"""
        try:
            coupon = Coupon.objects.get(code=attrs['code'])
            
            if not coupon.is_valid:
                raise serializers.ValidationError('Coupon is not valid.')
            
            if attrs['order_amount'] < coupon.minimum_order_amount:
                raise serializers.ValidationError(
                    f'Minimum order amount {coupon.minimum_order_amount} required for this coupon.'
                )
            
            attrs['coupon'] = coupon
        except Coupon.DoesNotExist:
            raise serializers.ValidationError('Coupon not found.')
        
        return attrs
