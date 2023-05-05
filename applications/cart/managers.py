from django.db import models

class CartManager(models.Manager):
    """ procedures for Cart """
    def create_cart(self, subtotal, total, user):
        cart = self.model(
            subtotal=subtotal,
            total=total,
            id_user=user
        )
        cart.save(using=self.db)
        return cart