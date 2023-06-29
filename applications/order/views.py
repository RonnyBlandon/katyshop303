import stripe
from django.views.generic import FormView
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext_lazy as _
# import models
from applications.cart.models import Cart
from applications.user.models import Address
from applications.order.models import Order, OrderAddress, OrderItem
from applications.points.models import UserPoint, PointsHistory, PointsSetting
# imports forms
from .forms import CheckoutForm
# import functions
from katyshop303.settings.base import get_secret
from .paypal import Paypal
from .stripe import Stripe
from applications.cart.shopping_cart import calculate_cart
from applications.order.functions import send_order_to_user
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

        # We register the order
        order = Order.objects.create_order_from_cart(cart, payment_method)
        order_address = OrderAddress.objects.create_address(order, shipment_info)
        order_items = OrderItem.objects.create_item_list(order, cart_items)

        if order and order_address and order_items:
        # We create the payment order
            if payment_method == "Paypal":
                checkout = Paypal()
                link_payment = checkout.create_order(order)
                if link_payment:
                    return HttpResponseRedirect(link_payment)
                else:
                    order.delete()
                    messages.add_message(request=self.request, level=messages.ERROR, message=_("An error occurred while processing your payment."))
                    return HttpResponseRedirect(reverse('order_app:checkout'))
            if payment_method == "Stripe":
                checkout = Stripe(id_user=self.request.user.id)
                link_payment = checkout.create_order(order)
                if link_payment:
                    return HttpResponseRedirect(link_payment)
                else:
                    order.delete()
                    messages.add_message(request=self.request, level=messages.ERROR, message=_("An error occurred while processing your payment."))
                    return HttpResponseRedirect(reverse('order_app:checkout'))
        else:
            try:
                order.delete()
                messages.add_message(request=self.request, level=messages.ERROR, message=_("An error occurred while processing your payment."))
            except Exception as err:
                messages.add_message(request=self.request, level=messages.ERROR, message=_("An error occurred while processing your payment."))

        return super(CheckoutView, self).form_valid(form)


def CapturePaypalPayment(request):
    # We collect the variables of the url that paypal returns to us when canceling or approving the payment
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
                # If there is a discount applied, deduct the points corresponding to the user.
                points_setting = PointsSetting.objects.get_point_setting()
                if order.discount > 0.00:
                    user_points = UserPoint.objects.deduct_points_to_user(order.discount, points_setting.redemption_rate, request.user.id)
                    PointsHistory.objects.points_deducted(order.discount, points_setting.redemption_rate, 
                                                _('Redeemed Points'), order, user_points)
                # We add the points earned to the user
                user_points = UserPoint.objects.add_points_to_user(order.total, points_setting.earning_points_rate, request.user.id)
                PointsHistory.objects.points_added(order.total, points_setting.earning_points_rate, 
                                                _('Points Earned For Purchase'), order, user_points)
                
                messages.add_message(request=request, level=messages.SUCCESS, message=_("The payment has been completed successfully."))
                # We mail the order to the user and notify the administrators of the new order.
                send_order_to_user(order)

            else:
                order.delete()
                messages.add_message(request=request, level=messages.ERROR, message=_("An error occurred while processing your payment."))
    return HttpResponseRedirect(reverse("user_app:user_orders"))


def WebhookStripeView(request):
    if request.method == 'POST':
        endpoint_secret = get_secret('STRIPE_ENDPOINT_SECRET')
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        event = None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError as err:
            # Invalid payload
            print("Invalid payload: ", err)
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as err:
            # Invalid signature
            print("Invalid Signature: ", err)
            return HttpResponse(status=400)
        except Exception as err:
            # any errors
            print("Error coming from stripe.Webhook.construct_event(): ", err)
            return HttpResponse(status=400)

        # Handle the checkout.session.completed event
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            id_user = session['metadata']['id_user']
            order = Order.objects.filter(id_user=id_user).last()
            # We create the import of the first vps payment with the relevant information
            transaction_id = session["payment_intent"]
            # We update the order
            order.status = "On hold"
            order.transaction_id = transaction_id
            order.save()
            # We reset the cart
            Cart.objects.clean_cart(id_user=id_user)
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
            # If there is a discount applied, deduct the points corresponding to the user.
            points_setting = PointsSetting.objects.get_point_setting()
            if order.discount > 0.00:
                user_points = UserPoint.objects.deduct_points_to_user(order.discount, points_setting.redemption_rate, order.id_user.id)
                PointsHistory.objects.points_deducted(order.discount, points_setting.redemption_rate, 
                                            _('Redeemed Points'), order, user_points)
            # We add the points earned to the user
            user_points = UserPoint.objects.add_points_to_user(order.total, points_setting.earning_points_rate, order.id_user.id)
            PointsHistory.objects.points_added(order.total, points_setting.earning_points_rate, 
                                            _('Points Earned For Purchase'), order, user_points)
        
            # We mail the order to the user and notify the administrators of the new order.
            send_order_to_user(order)

        return HttpResponse(status=200)
    
    if request.method == 'GET':
        id_user = request.GET.get("id_user")
        order = Order.objects.filter(id_user=id_user).last()
        # If the order already has the transaction_id, a success message is added. Otherwise, an error message is added.
        if order.transaction_id:
            messages.add_message(request=request, level=messages.SUCCESS, message=_("The payment has been completed successfully."))
        else:
            messages.add_message(request=request, level=messages.ERROR, message=_("An error occurred while processing your payment."))

    return HttpResponseRedirect(reverse("user_app:user_orders"))
