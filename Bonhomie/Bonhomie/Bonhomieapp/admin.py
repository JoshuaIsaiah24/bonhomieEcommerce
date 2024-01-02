from django.contrib import admin
from .models import CustomUser, Category, Products, Shipping, Order, Orderitem
from .models import Cart, PaymentMethod, Payment, Ratings, DiscountCode, Promotions

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']
class CustomUserAdmin(UserAdmin):
    model= CustomUser
    list_display=['username', 'email']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Category)
admin.site.register(Products)
admin.site.register(Shipping)
admin.site.register(Order)
admin.site.register(Orderitem)
admin.site.register(Cart)
admin.site.register(PaymentMethod)
admin.site.register(Payment)
admin.site.register(Ratings)
admin.site.register(DiscountCode)
admin.site.register(Promotions)