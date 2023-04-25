#import models
from applications.order.models import Cart, CartItem

def user_cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(id_user=request.user.id).first()
        if not cart:
            Cart.objects.create_cart(subtotal=0.00, total=0.00, id_user=request.user)
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

    return {}