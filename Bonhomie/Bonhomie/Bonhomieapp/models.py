from django.db import models
from django.contrib.auth.models import User, AbstractUser
from datetime import datetime

# Create your models here.

class CustomUser(AbstractUser):
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, null=False, unique=True)
    password = models.CharField(max_length=100, null=False)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']
    
    def __str__(self) -> str:
        return self.username

class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255, db_index=True)
    
    def __str__(self) -> str:
        return self.title

class Products(models.Model):
    product_name = models.CharField(max_length=100, null=False, db_index=True)
    description = models.CharField(max_length=600, null=False)
    price = models.DecimalField(max_digits=6, decimal_places=2, db_index=True)
    stock = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    featured = models.BooleanField(db_index=True)
    on_sale = models.BooleanField(db_index=True)
    
    def __str__(self) -> str:
        return self.product_name
    
class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product_name = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    total_price =  models.DecimalField(max_digits=6, decimal_places=2)
    
class Shipping(models.Model):
    carriers = models.CharField(max_length=100, db_index=True)
    rates = models.DecimalField(max_digits=3, decimal_places=2)
    express_delivery = models.BooleanField(default=False)

    
class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    order_date = models.DateTimeField(db_index=True, auto_now_add=True)
    order_id = models.CharField(max_length=10, unique=True)
    total_price = models.DecimalField(max_digits=6, decimal_places=2)
    carriers = models.ForeignKey(Shipping, on_delete=models.CASCADE)
    
    def get_delivery_date(self):
        if self.carriers.express_delivery:
            return ("Express Delivery: Your order will arrive in the next 48 hours")
        else:
            return ("Standard Delivery: Your order will arrive in 10 days")

class Orderitem(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_name = models.ForeignKey(Products, on_delete=models.PROTECT)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    total_price = models.DecimalField(max_digits=6, decimal_places=2)
    
    class Meta:
        unique_together = ('product_name', 'order_id')

#class Address(models.Model):
    #shipping_address = models.ForeignKey(User, related_name='shipping_addresses', on_delete=models.CASCADE)
    #billing_address = models.ForeignKey(User, related_name='billing_addresses', on_delete=models.CASCADE)

class PaymentMethod(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    payment_method= models.CharField(max_length=255, db_index=True)
    card_number = models.CharField(max_length=17, null=False)
    expiration_date = models.DateField()
    cvv = models.SmallIntegerField(null=False)
    
    def __str__(self):
        return self.user
    
class Payment(models.Model):
    total_price = models.ForeignKey(Order, related_name= 'total_price_payments', on_delete=models.CASCADE, db_index=True)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_id_payments', db_index=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')])
    timestamp = models.DateField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.status}"

class Ratings(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product_name = models.ForeignKey(Products, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    comment = models.TextField(max_length=1000, null=False)

class DiscountCode(models.Model):
    discount_code = models.CharField(max_length=10, db_index=True)
    discount_percentage = models.IntegerField(db_index=True)
    activation_date = models.DateTimeField()
    expiration_date = models.DateTimeField()
 
class Promotions(models.Model):
    promotion_name = models.CharField(max_length=255, db_index=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    discount_rate = models.IntegerField()
    
    def calculate_discount_price(self, price):
        return price - (price *(self.discount_rate / 100))
    
    