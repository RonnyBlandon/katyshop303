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
    
    def clean_cart(self, id_user):
        cart = self.filter(id_user=id_user).first()
        cart.subtotal = 0.00
        cart.discount = 0.00
        cart.total = 0.00
        cart.cart_items.all().delete()
        cart.save()
        return cart
