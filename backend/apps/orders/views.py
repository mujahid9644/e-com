# ============================================
# ORDER VIEWS
# ============================================

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from decimal import Decimal
import uuid
from apps.orders.models import Order, OrderItem, OrderShipment, OrderReturn
from apps.cart.models import Cart
from apps.payments.models import Coupon, Payment
from apps.orders.serializers import (
    OrderListSerializer, OrderDetailSerializer, CreateOrderSerializer,
    OrderReturnSerializer
)

# ============================================
# ORDER VIEWSET
# ============================================
class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoints for orders.
    
    Endpoints:
    - GET /api/orders/ - List user's orders
    - GET /api/orders/{id}/ - Get order details
    - POST /api/orders/create/ - Create new order from cart
    - POST /api/orders/{id}/cancel/ - Cancel order
    - POST /api/orders/{id}/request_return/ - Request return
    - GET /api/orders/{id}/tracking/ - Get shipment tracking
    """
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Get only current user's orders"""
        return Order.objects.filter(user=self.request.user).order_by('-created_at')
    
    def get_serializer_class(self):
        """Use different serializers for different actions"""
        if self.action == 'retrieve':
            return OrderDetailSerializer
        return OrderListSerializer
    
    @action(detail=False, methods=['post'])
    def create_from_cart(self, request):
        """
        Create a new order from user's cart.
        
        POST /api/orders/create_from_cart/
        Body: {
            shipping_address_id,
            payment_method,
            coupon_code (optional),
            customer_notes (optional)
        }
        """
        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            from apps.users.models import Address
            
            # Get cart
            try:
                cart = request.user.cart
            except:
                return Response(
                    {'error': 'Cart not found'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if not cart.items.exists():
                return Response(
                    {'error': 'Cart is empty'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Get shipping address
            address = Address.objects.get(
                id=serializer.validated_data['shipping_address_id'],
                user=request.user
            )
            
            # Calculate total
            subtotal = cart.total_price
            shipping_cost = Decimal('0')  # Can be dynamic based on location
            tax_amount = subtotal * Decimal('0.10')  # 10% tax
            discount_amount = Decimal('0')
            
            # Apply coupon if provided
            coupon_code = serializer.validated_data.get('coupon_code', '')
            if coupon_code:
                try:
                    coupon = Coupon.objects.get(code=coupon_code, is_active=True)
                    if coupon.is_valid:
                        if coupon.discount_type == 'fixed':
                            discount_amount = coupon.discount_value
                        elif coupon.discount_type == 'percentage':
                            discount_amount = subtotal * coupon.discount_value / 100
                            if coupon.maximum_discount_amount:
                                discount_amount = min(discount_amount, coupon.maximum_discount_amount)
                    else:
                        return Response(
                            {'error': 'Coupon is not valid'},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                except Coupon.DoesNotExist:
                    return Response(
                        {'error': 'Coupon not found'},
                        status=status.HTTP_404_NOT_FOUND
                    )
            
            total_price = subtotal + shipping_cost + tax_amount - discount_amount
            
            # Create order
            order = Order.objects.create(
                user=request.user,
                order_number=f"ORD-{uuid.uuid4().hex[:10].upper()}",
                shipping_address=address,
                subtotal=subtotal,
                shipping_cost=shipping_cost,
                tax_amount=tax_amount,
                discount_amount=discount_amount,
                total_price=total_price,
                coupon_code=coupon_code,
                payment_method=serializer.validated_data['payment_method'],
                customer_notes=serializer.validated_data.get('customer_notes', ''),
            )
            
            # Create order items from cart
            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    product_name=cart_item.product.name,
                    product_sku=cart_item.product.sku,
                    quantity=cart_item.quantity,
                    unit_price=cart_item.price_at_addition,
                    total_price=cart_item.total_price
                )
            
            # Clear cart
            cart.items.all().delete()
            
            return Response(
                OrderDetailSerializer(order).data,
                status=status.HTTP_201_CREATED
            )
        
        except Address.DoesNotExist:
            return Response(
                {'error': 'Address not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def create_guest_order(self, request):
        """
        Create a new order (for guests or logged users).
        
        POST /api/orders/create/
        Body: {
            product_id,
            customer_name (optional),
            phone_number,
            whatsapp_number (optional),
            address (optional),
            quantity,
            note (optional)
        }
        """
        data = request.data
        
        # Validate required fields
        if not data.get('product_id'):
            return Response({'error': 'Product ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not data.get('phone_number') and not data.get('whatsapp_number'):
            return Response({'error': 'Either phone number or WhatsApp number is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not data.get('quantity') or int(data.get('quantity', 0)) < 1:
            return Response({'error': 'Quantity must be at least 1'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            from apps.products.models import Product
            product = Product.objects.get(id=data['product_id'])
            
            if not product.is_in_stock or product.stock_quantity < int(data['quantity']):
                return Response({'error': 'Product out of stock'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Generate order number
            order_number = f"ORD-{uuid.uuid4().hex[:10].upper()}"
            
            # Calculate pricing
            quantity = int(data['quantity'])
            unit_price = product.discounted_price or product.price
            subtotal = unit_price * quantity
            tax_amount = subtotal * Decimal('0.10')  # 10% tax
            total_price = subtotal + tax_amount
            
            # Create order
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                order_number=order_number,
                customer_name=data.get('customer_name', ''),
                phone_number=data.get('phone_number', ''),
                whatsapp_number=data.get('whatsapp_number', ''),
                guest_address=data.get('address', ''),
                subtotal=subtotal,
                tax_amount=tax_amount,
                total_price=total_price,
                payment_method='cod',  # Default to COD for guest orders
                customer_notes=data.get('note', ''),
            )
            
            # Create order item
            OrderItem.objects.create(
                order=order,
                product=product,
                product_name=product.name,
                product_sku=product.sku,
                unit_price=unit_price,
                quantity=quantity,
                total_price=subtotal,
            )
            
            # Update product stock
            product.stock_quantity -= quantity
            product.save()
            
            return Response({
                'order_id': order.order_number,
                'message': 'Order placed successfully',
                'total': str(total_price)
            }, status=status.HTTP_201_CREATED)
            
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel an order (if still pending)"""
        order = self.get_object()
        
        if order.order_status != 'pending':
            return Response(
                {'error': 'Only pending orders can be cancelled'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        order.order_status = 'cancelled'
        order.save()
        
        return Response({'message': 'Order cancelled'})
    
    @action(detail=True, methods=['get'])
    def tracking(self, request, pk=None):
        """Get shipment tracking information"""
        order = self.get_object()
        
        try:
            shipment = order.shipment
            from apps.orders.serializers import OrderShipmentSerializer
            serializer = OrderShipmentSerializer(shipment)
            return Response(serializer.data)
        except OrderShipment.DoesNotExist:
            return Response(
                {'error': 'Shipment not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def request_return(self, request, pk=None):
        """Request a return for the order"""
        order = self.get_object()
        
        if order.order_status not in ['delivered', 'partially_returned']:
            return Response(
                {'error': 'Only delivered orders can be returned'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = OrderReturnSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Calculate refund
        refund_amount = order.total_price  # Full refund for now
        
        OrderReturn.objects.create(
            order=order,
            reason=serializer.validated_data['reason'],
            customer_comment=serializer.validated_data.get('customer_comment', ''),
            refund_amount=refund_amount
        )
        
        return Response(
            {'message': 'Return request submitted'},
            status=status.HTTP_201_CREATED
        )
