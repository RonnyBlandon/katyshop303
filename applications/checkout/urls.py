from django.urls import path
from . import views

app_name = "checkout_app"

urlpatterns = [
    path(
        'checkout/', 
        views.CheckoutView.as_view(), 
        name='checkout'
        ),
    path(
        'cart/', 
        views.CartView.as_view(), 
        name='cart'
        )
]