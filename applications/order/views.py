from django.views.generic import View, FormView
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
# import models
from applications.cart.models import Cart, CartItem
from applications.user.models import Address
from applications.order.models import Order, OrderAddress, OrderItem
# imports forms
from .forms import CheckoutForm
# import functions
from .paypal import Paypal
from applications.cart.shopping_cart import calculate_cart
# Create your views here.

class CheckoutView(FormView):
    template_name = 'order/checkout.html'
    form_class = CheckoutForm
    success_url = reverse_lazy('user_app:user_orders')

    def get_initial(self):
        initial = super().get_initial()
        address = Address.objects.filter(id_user=self.request.user.id).first()
        if self.request.user.is_authenticated:
            initial["name"] = self.request.user.name
            initial["last_name"] = self.request.user.last_name
        if address:
            initial['country'] = address.country.name
            initial['state'] = address.state
            initial['city'] = address.city
            initial['address_1'] = address.address_1
            initial['address_2'] = address.address_2
            initial['postal_code'] = address.postal_code
        
        return initial

    def form_valid(self, form):
        payment_method = form.cleaned_data["payment_method"]
        cart = Cart.objects.filter(id_user=self.request.user.id).first()
        cart_items = cart.cart_items.all()
        shipment_info = form.cleaned_data

        if payment_method == "Paypal":
            # We register the order
            order = Order.objects.create_order_from_cart(cart, payment_method)
            order_address = OrderAddress.objects.create_address(order, shipment_info)
            order_items = OrderItem.objects.create_item_list(order, cart_items)
            # We create the payment order
            if order and order_address and order_items:
                checkout = Paypal()
                link_payment = checkout.create_order(cart)
                return HttpResponseRedirect(link_payment)
            else:
                messages.add_message(request=self.request, level=messages.ERROR, message="Ocurrió un error al procesar tu pago.")

        return super(CheckoutView, self).form_valid(form)


def CapturePaypalPayment(request):
    # Recogemos las variables de la url que nos devuelve paypal al cancelar o aprobar el pago
    token = request.GET.get('token')
    order = Order.objects.filter(id_user=request.user.id).last()
    if token:
        checkout = Paypal()
        details = checkout.capture_order(token)
        if details:
            if details["status"] == "COMPLETED":
                # We update the order
                order.status = "On hold"
                order.transaction_id = details["id"]
                order.save()
                # We reset the cart
                Cart.objects.clean_cart(id_user=request.user.id)
                # We update the inventory
                items = order.order_items.all().order_by('-id')
                for item in items:
                    if item.product.amount_stock:
                        if item.amount < item.product.amount_stock:
                            item.product.amount_stock = item.product.amount_stock - item.amount
                        else:
                            item.product.amount_stock = 0
                        item.product.save()
                        # We take the opportunity to update the carts of all users who have products with limited inventory.
                        cart_list = Cart.objects.filter(cart_items__product=item.product, cart_items__amount__gt=item.product.amount_stock)
                        for cart in cart_list:
                                cart_item = cart.cart_items.filter(product=item.product.id).first()
                                cart_item.amount = item.product.amount_stock
                                cart_item.subtotal = item.product.price * item.product.amount_stock
                                cart_item.save()
                                calculate_cart(cart) 
                messages.add_message(request=request, level=messages.SUCCESS, message="El pago se ha completado exitosamente.")
            else:
                order.delete()
                messages.add_message(request=request, level=messages.ERROR, message="Ocurrió un error al procesar tu pago.")
    return HttpResponseRedirect(reverse("user_app:user_orders"))