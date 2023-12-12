from django.shortcuts import render
from rest_framework import generics, viewsets
from .models import User, Category, Products, Order, Orderitem, Cart
from .models import Ratings
from .serializers import UserSerializer, CategorySerializer, ProductSeriliazer, OrderSerializer, OrderItemSerializer, CartSerializer
from .serializers import RatingSerializer
from decimal import Decimal
from rest_framework.response import Response
from rest_framework import status
import stripe

# Create your views here.

class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class Productview(generics.ListCreateAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSeriliazer

class OrderView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user)
    
    def perform_create(self, request, *args, **kwargs):
        cart_items = Cart.objects.filter(user=request.user)
        total = self.calculate_total(cart_items)
        serializer = self.get_serializer(data=request.data)
        express_order = request.data.get('express_order', False)
        order = serializer.save(user=request.user, total=total, express_order=express_order)
        
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
    
    def calculate_total(self, cart_items):
        total = Decimal(0)
        for item in cart_items:
            total += item.price
        return total
    
class CartView(generics.ListCreateAPIView):
    serializer_class = CartSerializer
    
    def get_queryset(self):
        user = self.request.user
        return Cart.objects.filter(user=user)
    
    def perform_create(self, serializer):
        product_name = self.request.data.get('product_name')
        quantity = self.request.data.get('quantity')
        unit_price = Products.objects.get(pk=product_name).price
        quantity = int(quantity)
        total_price = quantity * unit_price
        serializer.save(user=self.request.user, total_price=total_price)
    
    def delete(self,request):
        user = self.request.user
        Cart.objects.filter(user=user).delete()
        return Response({'Message' : 'Successfully deleted item/s'}, status=status.HTTP_204_NO_CONTENT)
    
class RatingView(viewsets.Modelviewset):
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
    
        