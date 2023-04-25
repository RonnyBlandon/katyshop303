from django.db import models

class CartManager(models.Manager):
    """ procedures for Cart """
    def create_cart(self, subtotal, total, id_user):
        cart = self.model(
            subtotal=subtotal,
            total=total,
            id_user=id_user
        )
        cart.save(using=self.db)
        return cart
