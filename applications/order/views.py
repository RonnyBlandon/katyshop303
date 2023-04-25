from django.views.generic import View, FormView, ListView
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
#from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
# import models
from .models import Order, Cart
from applications.product.models import Product
# imports forms
from .forms import CheckoutForm
# Create your views here.

class CheckoutView(FormView):
    template_name = 'order/checkout.html'
    form_class = CheckoutForm
    success_url = reverse_lazy('user_app:user_address')


class CartView(ListView):
    template_name = 'order/cart.html'
    model = Cart


# cart views
def AddCartView(request, product_id, page):
    cart = Cart.objects.get(id_user=request.user.id)
    product = Product.objects.filter(id=product_id).first()
    item = cart.cart_items.filter(product__id=product.id).first()
    # if the user adds from the product page we get the value of the input
    if page == "product":
        quantity_product = int(request.POST.get("quantity-product"))
        #add the quantity of the product
        if not item:
            cart.cart_items.create(product=product, amount=quantity_product, subtotal=product.price * quantity_product)
        else:
            if product.amount_stock == None or item.amount < product.amount_stock:
                quantity = item.amount + quantity_product
                if quantity > product.amount_stock:
                    item.amount = product.amount_stock
                    item.subtotal = product.price * product.amount_stock
                    item.save()
                else:
                    item.amount += quantity_product
                    item.subtotal += product.price * quantity_product
                    item.save()
    else:
        #add the quantity of the product
        if not item:
            cart.cart_items.create(product=product, amount=1, subtotal=product.price)
        else:
            if product.amount_stock == None or item.amount < product.amount_stock:
                item.amount += 1
                item.subtotal += product.price
                item.save()

    #We extract the subtotal of all the products in the cart
    cart.subtotal = 0
    for item in cart.cart_items.all():
        cart.subtotal += item.subtotal
    #Calculate the number of items in the cart
    cart_items = cart.cart_items.all()
    quantity_items = 0
    item_subtotal = 0
    for item in cart_items:
        quantity_items += item.amount
        item_subtotal += item.subtotal
    
    cart.save()

    if page == "store" or page == "product":
        # We add the message that it was added successfully
        messages.add_message(request=request, level=messages.SUCCESS, message="Producto agregado al carrito exitosamente.", extra_tags="success-add-cart")
        return redirect(request.META.get('HTTP_REFERER'))
    elif page == "cart":
        return JsonResponse({"success": True, "item_amount": item.amount, "item_subtotal": item.subtotal, "cart_subtotal": cart.subtotal, "quantity_items": quantity_items})


def SubtractProductCartView(request, product_id):
    cart = Cart.objects.get(id_user=request.user.id)
    product = Product.objects.filter(id=product_id).first()
    item = cart.cart_items.filter(product__id=product_id).first()
    #we subtract the quantity of the product
    if item.amount > 1:
        item.amount -= 1
        item.subtotal -= product.price
        item.save()

    #We extract the subtotal of all the products in the cart
    cart.subtotal = 0
    for item in cart.cart_items.all():
        cart.subtotal += item.subtotal
    #Calculate the number of items in the cart
    cart_items = cart.cart_items.all()
    quantity_items = 0
    item_subtotal = 0
    for item in cart_items:
        quantity_items += item.amount
        item_subtotal += item.subtotal
    
    cart.save()
    return JsonResponse({"success": True, "item_amount": item.amount, "item_subtotal": item.subtotal, "cart_subtotal": cart.subtotal, "quantity_items": quantity_items})


# Mini cart page in the header
def DeleteProductCartView(request, product_id, page):
    cart = Cart.objects.get(id_user=request.user.id)
    product = Product.objects.filter(id=product_id).first()
    # we remove the product from the cart
    cart.cart_items.filter(product__id=product.id).first().delete()

    #We extract the subtotal of all the products in the cart
    cart.subtotal = 0
    for item in cart.cart_items.all():
        cart.subtotal += item.subtotal
    #Calculate the number of items in the cart
    cart_items = cart.cart_items.all()
    quantity_items = 0
    for item in cart_items:
        quantity_items += item.amount

    cart.save()

    if page == "cart":
        messages.add_message(request, level=messages.SUCCESS, message="Producto eliminado con éxito.", extra_tags="success-add-cart")
        return HttpResponseRedirect(reverse("order_app:cart"))
    elif page == "mini-cart":
        return JsonResponse({"delete_product": True, "cart_subtotal": cart.subtotal, "quantity_items": quantity_items})


def CleanCartView(request, product_id):
    cart = Cart.objects.get(id_user=request.user.id)
    # we clean the cart leaving the default fields
    cart.subtotal = 0.00
    cart.total = 0.00
    cart.cart_items.delete()
    cart.save()
