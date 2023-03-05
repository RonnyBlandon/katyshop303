from django.urls import path
from . import views

app_name = "product_app"

urlpatterns = [
    path(
        'store/', 
        views.StoreView.as_view(), 
        name='store'
        ),
    path(
        'product/<pk>/', 
        views.ProductView.as_view(), 
        name='product'
        ),
]