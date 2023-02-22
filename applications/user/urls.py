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
        'logout/', 
        views.LogoutView.as_view(), 
        name='user_logout'
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
