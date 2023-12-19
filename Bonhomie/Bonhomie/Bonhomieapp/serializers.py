from rest_framework import serializers
from .models import User, Category, Products, Order, Orderitem, Cart
from .models import Address, PaymentMethod, Payment, Ratings, DiscountCode
from .models import Shipping, Promotions


class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = '__all__'


class CategorySerializer(serializers.Serializer):
     class Meta:
         model = Category
         fields = '__all__'

class ProductSeriliazer(serializers.Serializer):
    category = serializers.CharField(source= Category.category, read_only=True)
    price = serializers.DecimalField(decimal_places=2, source = Products.price, read_only=True)
    product_name = serializers.CharField(source= Products.product_name, read_only=True)
    
    class Meta:
        model = Products
        fields = '__all__'

class OrderSerializer(serializers.Serializer):
    total_price = serializers.DecimalField(max_digits=6, decimal_places=2, read_only= True)
    order_date = serializers.DateTimeField(format="%m/%d/%Y", input_formats=["%m/%d/%Y"])
    user = serializers.CharField(source= User.username, read_only=True)
    total_price = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)
    
    class Meta:
        model = Order
        fields = '__all__'

class OrderItemSerializer(serializers.Serializer):
    order_id = serializers.IntegerField(read_only=True)
    product_name = serializers.CharField(read_only=True)
    
    class Meta:
        model = Orderitem
        fields = '__all__'

class CartSerializer(serializers.Serializer):
    user = serializers.CharField(source = User.username, read_only=True)
    
    class Meta:
        model= Cart
        fields = '__all__'
        
class RatingSerializer(serializers.Serializer):
    user = serializers.CharField(source = User.username, read_only=True)
    product_name = serializers.CharField(source = Products.product_name, read_only=True)
    
    class Meta:
        model = Ratings
        fields = '__all__'

class ShippingSerializer(serializers.Serializer):
    class Meta:
        model = Shipping
        fields = '__all__'
        
class PromotionSerializer(serializers.Serializer):
    class Meta:
        model = Promotions
        fields = '__all__'
        
class DiscountSerializer(serializers.Serializer):
    class Meta:
        model = DiscountCode
        fields = '__all__'

    
    

         