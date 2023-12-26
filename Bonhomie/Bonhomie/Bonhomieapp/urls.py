from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index, name='home'),
    path('category', views.CategoryView.as_view()),
    path('products', views.Productview.as_view()),
    path('orders', views.OrderView.as_view()),
    path('cart', views.CartView.as_view()),
    path('promotions', views.PromotionView.as_view()),
    path('promotions/<int:pk>', views.PromotionView.as_view()),
    path('shipping', views.ShippingView.as_view()),
    path('discounts', views.DiscountView.as_view()),

]