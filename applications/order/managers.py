from datetime import datetime
from django.db import models
# import models
from applications.user.models import Country

class OrderManager(models.Manager):
    """ procedures for Order """
    def create_order_from_cart(self, cart, payment_method):
        order = self.create(
            created = datetime.now(),
            status = "Failed",
            id_user = cart.id_user,
            subtotal = cart.subtotal,
            discount = cart.discount,
            total = cart.total,
            payment_method = payment_method,
            transaction_id = '',
        )
        return order


class OrderAddressManager(models.Manager):
    """ procedures for OrderAddress """
    def create_address(self, order, shipment_info):
        country = Country.objects.filter(name=shipment_info["country"]).first()
        state = country.state.filter(name=shipment_info["state"]).first()
        
        order_address = self.create(
            name = shipment_info["name"] +" "+shipment_info["last_name"],
            country = country,
            state = state,
            city = shipment_info["city"],
            address_1 = shipment_info["address_1"],
            address_2 = shipment_info["address_2"],
            postal_code = shipment_info["postal_code"],
            id_order = order
        )
        return order_address


class OrderItemManager(models.Manager):
    """ procedures for OrderItem """
    def create_item_list(self, order, cart_items):
        order_items = []
        for item in cart_items:
            order_item = self.create(
                id_order = order,
                product_name = item.product.name,
                amount = item.amount,
                unit_price = item.product.price,
                subtotal = item.subtotal
            )
            order_items.append(order_item)
        return order_items