from django.urls import path
from . import views

app_name = "cart_app"

urlpatterns = [
    path(
        'cart/', 
        views.CartView.as_view(), 
        name='cart'
        ),
    path('add-cart-product/<int:product_id>/', views.AddCartProductView, name='add_cart_product'),
    path('add-cart-store/<int:product_id>/', views.AddCartStoreView, {'page': 'store'}, name='add_cart_store'),
    path('add-cart/<int:product_id>/', views.AddCartStoreView, {'page': 'cart'}, name='add_cart'),
    path('subtract-cart/<int:product_id>/', views.SubtractProductCartView, name='subtract_cart'),
    path('delete-mini-cart/<int:product_id>/', views.DeleteProductCartView, {'page':'mini-cart' }, name='delete_mini_cart'),
    path('delete-cart/<int:product_id>/', views.DeleteProductCartView, {'page': 'cart'}, name='delete_cart'),
]