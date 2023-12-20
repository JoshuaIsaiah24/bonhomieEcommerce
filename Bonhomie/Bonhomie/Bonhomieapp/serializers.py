from rest_framework import serializers
from .models import User, Category, Products, Order, Orderitem, Cart
from .models import Address, PaymentMethod, Payment, Ratings, DiscountCode
from .models import Shipping, Promotions


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
     class Meta:
         model = Category
         fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source= 'category.title', read_only=True)
    class Meta:
        model = Products
        fields = ['product_name', 'description', 'price', 'stock', 'category', 'featured', 'on_sale']

class OrderSerializer(serializers.ModelSerializer):
    total_price = serializers.DecimalField(max_digits=6, decimal_places=2, read_only= True)
    order_date = serializers.DateTimeField(format="%m/%d/%Y", input_formats=["%m/%d/%Y"])
    user = serializers.CharField(source= User.username, read_only=True)
    total_price = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)
    
    class Meta:
        model = Order
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField(read_only=True)
    product_name = serializers.CharField(read_only=True)
    
    class Meta:
        model = Orderitem
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source = User.username, read_only=True)
    
    class Meta:
        model= Cart
        fields = '__all__'
        
class RatingSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source = User.username, read_only=True)
    product_name = serializers.CharField(source = Products.product_name, read_only=True)
    
    class Meta:
        model = Ratings
        fields = '__all__'

class ShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipping
        fields = '__all__'
        
class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotions
        fields = '__all__'
        
class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountCode
        fields = '__all__'

    
    

         