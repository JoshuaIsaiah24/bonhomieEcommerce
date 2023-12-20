from django.contrib import admin
from .models import User, Category, Products, Shipping, Order, Orderitem
from .models import Cart, Address, PaymentMethod, Payment, Ratings, DiscountCode, Promotions

# Register your models here.

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Products)
admin.site.register(Shipping)
admin.site.register(Order)
admin.site.register(Orderitem)
admin.site.register(Cart)
admin.site.register(Address)
admin.site.register(PaymentMethod)
admin.site.register(Payment)
admin.site.register(Ratings)
admin.site.register(DiscountCode)
admin.site.register(Promotions)