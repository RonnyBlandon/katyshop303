from django.urls import path
from . import views

app_name = "order_app"

urlpatterns = [
    path(
        'checkout/', 
        views.CheckoutView.as_view(), 
        name='checkout'
        ),
]