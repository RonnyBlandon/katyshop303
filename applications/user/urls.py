from django import views
from django.urls import path
from . import views

app_name = "user_app"

urlpatterns = [
    path(
        'user-register/', 
        views.UserRegisterView.as_view(), 
        name='user_register'
        ),
    path(
        'user-login/', 
        views.UserLoginView.as_view(),
        name='user_login'
        ),
    path(
        'user-login-checkout/', 
        views.UserLoginView.as_view(), 
        {"page": "checkout"},
        name='user_login_checkout'
        ),
    path(
        'logout/', 
        views.LogoutView.as_view(), 
        name='user_logout'
        ),
    path(
        'my-account/orders/', 
        views.UserOrderView.as_view(), 
        name='user_orders'
        ),
    path(
        'my-account/orders/<pk>/', 
        views.OrderDetailsView.as_view(), 
        name='order_details'
        ),
    path(
        'my-account/profile/', 
        views.UserProfileView.as_view(), 
        name='user_profile'
        ),
    path(
        'my-account/address/', 
        views.UserAddressView.as_view(), 
        name='user_address'
        ),
    path(
        'my-account/points/', 
        views.UserPointView.as_view(), 
        name='user_points'
        ),
    path(
        'verification-code/<id>/<code>/', 
        views.CodeVerificationView.as_view(), 
        name='user_verification'
        ),
    path(
        'thank-you/', 
        views.UserThankYouView.as_view(), 
        name='user_thank_you'
        ),
    path(
        'resend-email-user/', 
        views.UserVerificationResendView.as_view(), 
        name='user_resend_email'
        ),
    path(
        'recover-password/', 
        views.RecoverAccountView.as_view(), 
        name='recover_password'
        ),
    path(
        'change-password/<id>/<code>/', 
        views.ChangePasswordView.as_view(), 
        name='user_change_password'
        ),
]
