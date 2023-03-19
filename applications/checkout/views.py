from django.views.generic import TemplateView, FormView, ListView
from django.urls import reverse_lazy
# import models
from .models import Cart
# imports forms
from .forms import CheckoutForm
# Create your views here.

class CheckoutView(FormView):
    template_name = 'checkout/checkout.html'
    form_class = CheckoutForm
    success_url = reverse_lazy('user_app:user_address')


class CartView(ListView):
    template_name = 'checkout/cart.html'
    model = Cart

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        return context