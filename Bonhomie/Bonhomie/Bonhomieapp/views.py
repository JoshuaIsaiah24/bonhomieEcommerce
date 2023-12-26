from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import render
from rest_framework import generics, viewsets, status
from .models import User, Category, Products, Order, Orderitem, Cart, Promotions, Shipping, DiscountCode
from .models import Ratings
from .serializers import UserSerializer, CategorySerializer, ProductSerializer, OrderSerializer, OrderItemSerializer, CartSerializer
from .serializers import RatingSerializer, PromotionSerializer, ShippingSerializer, DiscountSerializer
from decimal import Decimal
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
import stripe

# Create your views here.

class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class Productview(generics.ListCreateAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer

class OrderView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        cart_items = Cart.objects.filter(user=self.request.user)
        total = self.calculate_total(cart_items)
        
        express_delivery = self.request.data.get('express_delivery', False)
        
        try:
            order = serializer.save(user=self.request.user, total=total, express_delivery=express_delivery)
            
            for cart_item in cart_items:
                Orderitem.objects.create(
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    unit_price=cart_item.unit_price,
                    total_price= cart_item.total_price,
                    order=order)
                cart_item.delete()
                
            return Response (
                data={'message':'Product/s successfully ordered'},
                status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self, request, *args, **kwargs):
        serializer = DiscountSerializer(data=request.data)
        if serializer.is_valid():
            code = serializer.validated_data['code']
            try:
                discount = DiscountCode.objects.get(code=code, expiration_date__gte=timezone.now().date())
                return Response({'message':'discount applied successfully'}, status=status.HTTP_200_OK)
            except DiscountCode.DoesNotExist:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    def calculate_total(self, cart_items):
        total = Decimal(0)
        for item in cart_items:
            total += item.price
        return total
    
class CartView(generics.ListCreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Cart.objects.filter(user=user)
    
    def perform_create(self, serializer):
        product_name = self.request.data.get('product_name')
        quantity = int(self.request.data.get('quantity', 0))
        product_instance = get_object_or_404(Products, product_name=product_name)
        unit_price = product_instance.price
        total_price = quantity * unit_price
        serializer.save(user=self.request.user, product=product_instance, total_price=total_price)
    
    def delete(self,request):
        Cart.objects.filter(user=self.request.user).delete()
        return Response({'Message' : 'Successfully deleted item/s'}, status=status.HTTP_204_NO_CONTENT)
    
class RatingView(viewsets.ModelViewSet):
    queryset = Ratings.objects.all()
    serializer_class = RatingSerializer
    
class CheckoutSessionViewSet(viewsets.ViewSet):
    def create(self, request):
        user_cart_items = Cart.objects.filter(user=request.user)

        line_items = []
        for cart_item in user_cart_items:
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': cart_item.product.product_name,
                        'description': cart_item.product.description,
                    },
                    'unit_amount': int(cart_item.product.price * 100),
                },
                'quantity': cart_item.quantity,
            })

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=request.build_absolute_uri('success/'),
            cancel_url=request.build_absolute_uri('cancel/'),
        )

        return Response({'url': checkout_session.url})
    
class PromotionView(generics.ListCreateAPIView):
    queryset = Promotions.objects.all()
    serializer_class = PromotionSerializer
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        active_promotions = queryset.filter(start_date__lte=timezone.now(), end_date__gte=timezone.now())
        products_in_promotion = Products.objects.filter(productpromotion__promotion__in=active_promotions)
        
        discounted_prices = {}
        for product in products_in_promotion:
            for promotion in active_promotions:
                discounted_prices[{product.id, promotion.id}] = promotion.calculate_discount_price(product.price)
        
        data = {
            
            'promotions': serializer.data,
            'discounted_prices': discounted_prices,
            
        }
    
        return Response(data)
    
class PromotionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Promotions.objects.all()
    serializer_class = PromotionSerializer

class ShippingView(generics.ListCreateAPIView):
    queryset = Shipping.objects.all()
    serializer_class = ShippingSerializer
    
class DiscountView(generics.ListCreateAPIView):
    queryset = DiscountCode.objects.all()
    serializer_class = DiscountSerializer


def index (request):
    return render(request, 'index.html')
    

    
    
    
        