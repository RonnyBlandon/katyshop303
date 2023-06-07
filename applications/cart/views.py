from django.views.generic import ListView
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.urls import reverse
# import models
from .models import Cart
from applications.product.models import Product
# import cart
from .shopping_cart import ShoppingCartCookies, calculate_cart
# Create your views here.

class CartView(ListView):
    template_name = 'cart/cart.html'
    model = Cart


# cart views with authenticated user
def AddCartProductView(request, product_id):
    product = Product.objects.filter(id=product_id).first()
    # if the user is authenticated it is saved in the database
    if request.user.is_authenticated:
        cart = Cart.objects.get(id_user=request.user.id)
        item = cart.cart_items.filter(product__id=product.id).first()
        # if the user adds from the product page we get the value of the input
        quantity_product = int(request.POST.get("quantity-product"))
        #add the quantity of the product
        if not item:
            cart.cart_items.create(product=product, amount=quantity_product, subtotal=product.price * quantity_product)
            # We add the message that it was added successfully
            messages.add_message(request=request, level=messages.SUCCESS, message="Product added to cart successfully.", extra_tags="success-add-cart")
        else:
            if product.amount_stock == None or item.amount < product.amount_stock:
                quantity = item.amount + quantity_product
                # if the product has quantity in stock
                if product.amount_stock:
                    if quantity > product.amount_stock:
                        item.amount = product.amount_stock
                        item.subtotal = product.price * product.amount_stock
                        item.save()
                        messages.add_message(request=request, level=messages.SUCCESS, message="You cannot add more than the units that are available.", extra_tags="alert-add-cart")
                    else:
                        item.amount += quantity_product
                        item.subtotal += product.price * quantity_product
                        item.save()
                        messages.add_message(request=request, level=messages.SUCCESS, message="Product added to cart successfully.", extra_tags="success-add-cart")
                else:
                    #If you have not defined the quantity of stock, add a limit of a maximum of 10 units of the product
                    if quantity > 10:
                        item.amount = 10
                        item.subtotal = product.price * 10
                        item.save()
                        #We added the message of the amount that you can add as a maximum per product
                        messages.add_message(request=request, level=messages.SUCCESS, message="You can only add 10 maximum for this product.", extra_tags="alert-add-cart")         
                    else:
                        item.amount += quantity_product
                        item.subtotal += product.price * quantity_product
                        item.save()
                        messages.add_message(request=request, level=messages.SUCCESS, message="Product added to cart successfully.", extra_tags="success-add-cart")

        calculate_cart(cart)
        return redirect(request.META.get('HTTP_REFERER'))
    # Otherwise the user is not authenticated, the data will be saved in the browser's cookies
    else:
        cart = ShoppingCartCookies(request)
        return cart.add_from_product(product)


def AddCartStoreView(request, product_id, page):
    product = Product.objects.filter(id=product_id).first()
    # if the user is authenticated it is saved in the database
    if request.user.is_authenticated:
        cart = Cart.objects.get(id_user=request.user.id)
        item = cart.cart_items.filter(product__id=product.id).first()
        #add the quantity of the product
        if not item:
                cart.cart_items.create(product=product, amount=1, subtotal=product.price)
        else:
            if product.amount_stock:
                if item.amount < product.amount_stock:
                    item.amount += 1
                    item.subtotal += product.price
                    item.save()
                    if page == "store":
                        messages.add_message(request=request, level=messages.SUCCESS, message="Product added to cart successfully.", extra_tags="success-add-cart")
                else:
                    #We added the message of the amount that you can add as a maximum per product
                    messages.add_message(request=request, level=messages.SUCCESS, message="You cannot add more than the units that are available.", extra_tags="alert-add-cart")
            else:
                if item.amount < 10:
                    item.amount += 1
                    item.subtotal += product.price
                    item.save()
                    if page == "store":
                        messages.add_message(request=request, level=messages.SUCCESS, message="Product added to cart successfully.", extra_tags="success-add-cart")
                else:
                    #We added the message of the amount that you can add as a maximum per product
                    messages.add_message(request=request, level=messages.SUCCESS, message="You can only add 10 maximum for this product.", extra_tags="alert-add-cart")
        
        quantity_items = calculate_cart(cart)
        if page == "store":
            return redirect(request.META.get('HTTP_REFERER'))
        elif page == "cart":
            return JsonResponse({"success": True, "item_amount": item.amount, "item_subtotal": item.subtotal, 
                "cart_subtotal": cart.subtotal, "cart_total": cart.total, "cart_discount": cart.discount, 
                "quantity_items": quantity_items})
    # Otherwise the user is not authenticated, the data will be saved in the browser's cookies
    else:
        cart = ShoppingCartCookies(request)
        return cart.add_from_store(product, page)


def SubtractProductCartView(request, product_id):
    product = Product.objects.filter(id=product_id).first()
    if request.user.is_authenticated:
        cart = Cart.objects.get(id_user=request.user.id)
        item = cart.cart_items.filter(product__id=product_id).first()
        #we subtract the quantity of the product
        if item.amount > 1:
            item.amount -= 1
            item.subtotal -= product.price
            item.save()

        quantity_items = calculate_cart(cart)
        return JsonResponse({"success": True, "item_amount": item.amount, "item_subtotal": item.subtotal, 
            "cart_subtotal": cart.subtotal, "cart_total": cart.total, "cart_discount": cart.discount,
            "quantity_items": quantity_items})
    else:
        cart = ShoppingCartCookies(request)
        return cart.subtract(product)


# Mini cart page in the header
def DeleteProductCartView(request, product_id, page):
    product = Product.objects.filter(id=product_id).first()
    if request.user.is_authenticated:
        cart = Cart.objects.get(id_user=request.user.id)
        # we remove the product from the cart
        cart.cart_items.filter(product__id=product.id).first().delete()

        quantity_items = calculate_cart(cart)

        if page == "cart":
            messages.add_message(request, level=messages.SUCCESS, message="Product successfully removed.", extra_tags="success-add-cart")
            return HttpResponseRedirect(reverse("cart_app:cart"))
        elif page == "mini-cart":
            return JsonResponse({"delete_product": True, "cart_subtotal": cart.subtotal, "quantity_items": quantity_items})
    else:
        cart = ShoppingCartCookies(request)
        return cart.delete(product, page)
