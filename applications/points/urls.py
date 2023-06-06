from django.urls import path
from . import views

app_name = "points_app"

urlpatterns = [
    path(
        'redeem-points/<int:points>/', 
        views.PointsView.as_view(), 
        name='redeem_points'
        ),
    path(
        'remove-discount-checkout/', 
        views.RemoveDiscountView.as_view(),
        {'page':'checkout'},
        name='remove_discount_checkout'
        ),
    path(
        'remove-discount-cart/', 
        views.RemoveDiscountView.as_view(),
        {'page':'cart'},
        name='remove_discount_cart'
        ),
]