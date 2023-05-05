from django.views.generic import FormView
from django.contrib import messages
from django.urls import reverse_lazy
# imports forms
from .forms import CheckoutForm
# Create your views here.

class CheckoutView(FormView):
    template_name = 'order/checkout.html'
    form_class = CheckoutForm
    success_url = reverse_lazy('user_app:user_address')
