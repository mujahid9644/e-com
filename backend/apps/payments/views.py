# ============================================
# PAYMENT VIEWS
# ============================================

from rest_framework import status, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.payments.models import Payment, Coupon, CouponUsage
from apps.payments.serializers import PaymentSerializer, CouponSerializer, CouponValidationSerializer
from apps.orders.models import Order
from django.utils import timezone

# ============================================
# PAYMENT VIEWSET
# ============================================
class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoints for payment management.
    
    Endpoints:
    - GET /api/payments/{id}/- Get payment details
    - POST /api/payments/validate_coupon/ - Validate coupon code
    - POST /api/payments/apply_coupon/ - Apply coupon to order
    """
    
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PaymentSerializer
    
    def get_queryset(self):
        """Get payments for current user's orders"""
        return Payment.objects.filter(order__user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def validate_coupon(self, request):
        """
        Validate if a coupon code is valid and applicable.
        
        POST /api/payments/validate_coupon/
        Body: {code, order_amount}
        """
        serializer = CouponValidationSerializer(data=request.data)
        if serializer.is_valid():
            coupon = serializer.validated_data['coupon']
            order_amount = serializer.validated_data['order_amount']
            
            # Calculate discount
            if coupon.discount_type == 'percentage':
                discount = order_amount * coupon.discount_value / 100
                if coupon.maximum_discount_amount:
                    discount = min(discount, coupon.maximum_discount_amount)
            elif coupon.discount_type == 'fixed':
                discount = coupon.discount_value
            else:  # free_shipping
                discount = 0
            
            return Response({
                'valid': True,
                'discount': float(discount),
                'discount_type': coupon.discount_type,
                'final_amount': float(order_amount - discount)
            })
        
        return Response(
            {'valid': False, 'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=False, methods=['post'])
    def apply_coupon(self, request):
        """
        Apply a coupon to an order.
        
        POST /api/payments/apply_coupon/
        Body: {order_id, code}
        """
        order_id = request.data.get('order_id')
        code = request.data.get('code', '').upper()
        
        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response(
                {'error': 'Order not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        try:
            coupon = Coupon.objects.get(code=code, is_active=True)
        except Coupon.DoesNotExist:
            return Response(
                {'error': 'Coupon not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if not coupon.is_valid:
            return Response(
                {'error': 'Coupon has expired'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check user usage limit
        user_usage_count = CouponUsage.objects.filter(
            coupon=coupon,
            user=request.user
        ).count()
        
        if user_usage_count >= coupon.usage_limit_per_user:
            return Response(
                {'error': 'You have reached the usage limit for this coupon'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Apply coupon to order
        order.coupon_code = code
        order.save()
        
        # Log coupon usage
        CouponUsage.objects.create(
            coupon=coupon,
            user=request.user,
            order=order,
            discount_amount=order.discount_amount
        )
        
        return Response({
            'message': 'Coupon applied successfully',
            'discount': float(order.discount_amount)
        })


# ============================================
# COUPON VIEWSET
# ============================================
class CouponViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoints for viewing coupons.
    Admin only can create/modify coupons.
    """
    
    queryset = Coupon.objects.filter(is_active=True)
    serializer_class = CouponSerializer
    permission_classes = [permissions.AllowAny]
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get currently active and valid coupons"""
        now = timezone.now()
        coupons = Coupon.objects.filter(
            is_active=True,
            start_date__lte=now,
            end_date__gte=now
        )
        serializer = self.get_serializer(coupons, many=True)
        return Response(serializer.data)
