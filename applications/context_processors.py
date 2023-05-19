import json
#import models
from applications.cart.models import Cart
from applications.product.models import Product

def user_cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(id_user=request.user.id).first()
        if not cart:
            Cart.objects.create_cart(subtotal=0.00, total=0.00, user=request.user)
        #Calculate the number of items in the cart
        cart_items = cart.cart_items.all()
        quantity_items = 0
        for item in cart_items:
            quantity_items += item.amount
        
        return {"cart_id": cart.id, 
            "cart_subtotal": cart.subtotal,
            "cart_total": cart.total,
            "cart_items": cart.cart_items.all().order_by("-id"),
            "quantity_items": quantity_items
        }
    
    if "cart" in request.COOKIES:
        cart = json.loads(request.COOKIES.get("cart"))
        cart_items = cart["cart_items"]

        # get the id of the cart products
        product_ids = list(cart_items.keys())
        cart_products = Product.objects.filter(id__in=product_ids).order_by("-id")
        # Add the amount field to each record in the query
        for register in cart_products:
            if cart_items[str(register.id)]:
                register.amount = cart_items[str(register.id)]["amount"]
                register.accumulated = cart_items[str(register.id)]["accumulated"]
        
        quantity_items = 0
        for item in cart_items:
            quantity_items += cart_items[item]["amount"]

        return {"cart_subtotal": cart["subtotal"],
            "cart_total": cart["total"],
            "cart_items": cart_products,
            "quantity_items": quantity_items
        }
    
    return {}
