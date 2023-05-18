import json
from decimal import Decimal
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages
# import models
from .models import Cart
from applications.product.models import Product

# This ShoppingCartCookies class is for users who are not authenticated on the website.
class ShoppingCartCookies():
    def __init__(self, request):
        self.request = request
        self.cookies = request.COOKIES

        if "cart" in request.COOKIES:
            self.cart = json.loads(request.COOKIES.get("cart"))
            self.cart_items = self.cart["cart_items"]
        else:
            self.cart = {"subtotal": 0.00, "total": 0.00}
            self.cart_items = {}


    def add_from_product(self, product):
        id = str(product.id)
        # we get the input of the number of units that the user wants to add
        quantity_product = int(self.request.POST.get("quantity-product"))
        #add the quantity of the product
        if not id in self.cart_items:
            self.cart_items[id] = {
                "amount": quantity_product,
                "accumulated": product.price * quantity_product
            }
            # We add the message that it was added successfully
            messages.add_message(request=self.request, level=messages.SUCCESS, message="Producto agregado al carrito exitosamente.", extra_tags="success-add-cart")
        else:
            # we convert the string in decimal
            self.cart_items[id]["accumulated"] = Decimal(self.cart_items[id]["accumulated"])
            quantity = self.cart_items[id]["amount"] + quantity_product
            # if the product has quantity in stock
            if product.amount_stock:
                if quantity > product.amount_stock:
                    self.cart_items[id]["amount"] = product.amount_stock
                    self.cart_items[id]["accumulated"] = product.price * product.amount_stock
                    messages.add_message(request=self.request, level=messages.SUCCESS, message="No puede agregar más de las unidades que hay disponibles.", extra_tags="alert-add-cart")        
                else:
                    self.cart_items[id]["amount"] += quantity_product
                    self.cart_items[id]["accumulated"] += product.price * quantity_product
                    messages.add_message(request=self.request, level=messages.SUCCESS, message="Producto agregado al carrito exitosamente.", extra_tags="success-add-cart")
            else:
                #If you have not defined the quantity of stock, add a limit of a maximum of 10 units of the product
                if quantity > 10:
                    self.cart_items[id]["amount"] = 10
                    self.cart_items[id]["accumulated"] = product.price * 10
                    #We added the message of the amount that you can add as a maximum per product
                    messages.add_message(request=self.request, level=messages.SUCCESS, message="Solo puede agregar 10 como máximo para este producto.", extra_tags="alert-add-cart")  
                else:
                    self.cart_items[id]["amount"] += quantity_product
                    self.cart_items[id]["accumulated"] += product.price * quantity_product
                    messages.add_message(request=self.request, level=messages.SUCCESS, message="Producto agregado al carrito exitosamente.", extra_tags="success-add-cart")

        self.calculate_cart()
        # Encode the data to JSON
        self.cart_items[id]["accumulated"] = str(self.cart_items[id]["accumulated"])
        self.cart["cart_items"] = self.cart_items
        data_json = json.dumps(self.cart)

        response = redirect(self.request.META.get('HTTP_REFERER'))
        response.set_cookie("cart", data_json, max_age=2592000)
        return response


    def add_from_store(self, product, page):
        id = str(product.id)
        #add the quantity of the product
        if not id in self.cart_items:
            self.cart_items[id] = {
                "amount": 1,
                "accumulated": product.price
            }
            # We add the message that it was added successfully
            messages.add_message(request=self.request, level=messages.SUCCESS, message="Producto agregado al carrito exitosamente.", extra_tags="success-add-cart")
        else:
            # we convert the string in decimal
            self.cart_items[id]["accumulated"] = Decimal(self.cart_items[id]["accumulated"])
            if product.amount_stock:
                if self.cart_items[id]["amount"] < product.amount_stock:
                    self.cart_items[id]["amount"] += 1
                    self.cart_items[id]["accumulated"] += product.price
                    if page == "store":
                        messages.add_message(request=self.request, level=messages.SUCCESS, message="Producto agregado al carrito exitosamente.", extra_tags="success-add-cart")
                else:
                    #We added the message of the amount that you can add as a maximum per product
                    messages.add_message(request=self.request, level=messages.SUCCESS, message="No puede agregar más de las unidades que hay disponibles.", extra_tags="alert-add-cart")
            else:
                if self.cart_items[id]["amount"] < 10:
                    self.cart_items[id]["amount"] += 1
                    self.cart_items[id]["accumulated"] += product.price
                    if page == "store":
                        messages.add_message(request=self.request, level=messages.SUCCESS, message="Producto agregado al carrito exitosamente.", extra_tags="success-add-cart")
                else:
                    #We added the message of the amount that you can add as a maximum per product
                    messages.add_message(request=self.request, level=messages.SUCCESS, message="Solo puede agregar 10 como máximo para este producto.", extra_tags="alert-add-cart")
    
        quantity_items = self.calculate_cart()
        # Encode the data to JSON
        self.cart_items[id]["accumulated"] = str(self.cart_items[id]["accumulated"])
        self.cart["cart_items"] = self.cart_items
        data_json = json.dumps(self.cart)

        if page == "store":
            response = redirect(self.request.META.get('HTTP_REFERER'))
            response.set_cookie("cart", data_json, max_age=2592000)
            return response
        elif page == "cart":
            response = JsonResponse({"success": True, "item_amount": self.cart_items[id]["amount"], "item_subtotal": self.cart_items[id]["accumulated"], "cart_subtotal": self.cart["subtotal"], "quantity_items": quantity_items})
            response.set_cookie("cart", data_json, max_age=2592000)
            return response


    def calculate_cart(self):
        #We extract the subtotal of all the products in the cart
        self.cart["subtotal"] = 0
        quantity_items = 0
        for item in self.cart_items:
            self.cart["subtotal"] += Decimal(self.cart_items[item]["accumulated"])
            # Calculate the number of items in the cart to update the template.
            quantity_items += self.cart_items[item]["amount"]
        
        self.cart["subtotal"] = str(self.cart["subtotal"])
        return quantity_items


    def delete(self, product, page):
        id = str(product.id)
        if id in self.cart_items:
            del self.cart_items[id]

        quantity_items = self.calculate_cart()

        # Encode the data to JSON
        self.cart["cart_items"] = self.cart_items
        data_json = json.dumps(self.cart)

        if page == "cart":
            messages.add_message(self.request, level=messages.SUCCESS, message="Producto eliminado con éxito.", extra_tags="success-add-cart")
            response = HttpResponseRedirect(reverse("cart_app:cart"))
            response.set_cookie("cart", data_json, max_age=2592000)
            return response
        elif page == "mini-cart":
            response = JsonResponse({"delete_product": True, "cart_subtotal": self.cart["subtotal"], "quantity_items": quantity_items})
            response.set_cookie("cart", data_json, max_age=2592000)
            return response 


    def subtract(self, product):
        id = str(product.id)
        if id in self.cart_items.keys():
            # we convert the string in decimal
            self.cart_items[id]["accumulated"] = Decimal(self.cart_items[id]["accumulated"])
            if self.cart_items[id]["amount"] > 1:
                self.cart_items[id]["amount"] -= 1
                self.cart_items[id]["accumulated"] -= product.price

        quantity_items = self.calculate_cart()
        # Encode the data to JSON
        self.cart_items[id]["accumulated"] = str(self.cart_items[id]["accumulated"])
        self.cart["cart_items"] = self.cart_items
        data_json = json.dumps(self.cart)

        response = JsonResponse({"success": True, "item_amount": self.cart_items[id]["amount"], "item_subtotal": self.cart_items[id]["accumulated"], "cart_subtotal": self.cart["subtotal"], "quantity_items": quantity_items})
        response.set_cookie("cart", data_json, max_age=2592000)
        return response


    def cookie_cart_to_database(self, id_user):
        database_cart = Cart.objects.filter(id_user=id_user).first()
        database_cart_items = database_cart.cart_items.all().order_by("-id")
        for id_item in self.cart_items:
            # Cart products in cookies that are not in the cart database are copied
            if not database_cart_items.filter(product=id_item):
                product = Product.objects.filter(id=id_item).first()
                quantity_product = self.cart_items[id_item]["amount"]
                database_cart.cart_items.create(product=product, amount=quantity_product, subtotal=product.price * quantity_product)
            calculate_cart(database_cart)


# function to calculate or recalculate the cart each time products are added or removed from the cart
def calculate_cart(cart):
    #We extract the subtotal of all the products in the cart
    cart.subtotal = 0
    cart_items = cart.cart_items.all()
    quantity_items = 0
    for item in cart_items:
        cart.subtotal += item.subtotal
        # Calculate the number of items in the cart to update the template.
        quantity_items += item.amount
    cart.total = cart.subtotal - cart.discount
    cart.save()
    return quantity_items

