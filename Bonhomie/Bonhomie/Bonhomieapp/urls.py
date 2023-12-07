from django.urls import path
from . import views

urlpatters = [
    path('category', views.CategoryView.as_view()),
    path('products', views.Productview.as_view()),
    path('orders', views.OrderView.as_view()),
    path('Cart', views.CartView.as_view()),
    
]