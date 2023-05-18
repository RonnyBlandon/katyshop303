from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

app_name = "order_app"

urlpatterns = [
    path(
        'checkout/', 
        views.CheckoutView.as_view(), 
        name='checkout'
        ),
    path(
        'paypal-payment/',
        views.CapturePaypalPayment,
        name='capture_paypal_payment'
        ),
    path(
        'webhook-stripe/',
        csrf_exempt(views.WebhookStripeView),
        name='webhook_stripe'
        ),
]