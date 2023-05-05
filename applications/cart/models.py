from django.db import models
# import managers
from applications.cart.managers import CartManager
# import models
from applications.user.models import User
from applications.product.models import Product
# Create your models here.

# Cart models
class Cart(models.Model):
    subtotal = models.DecimalField('Subtotal', max_digits=8, decimal_places=2, default=0.00)
    total = models.DecimalField('Total', max_digits=8, decimal_places=2, default=0.00)
    id_user = models.ForeignKey(User, verbose_name='ID del usuario', on_delete=models.CASCADE)

    objects = CartManager()

    def __str__(self):
        return str(self.id)+' '+str(self.id_user)


class CartItem(models.Model):
    id_cart = models.ForeignKey(Cart, verbose_name='ID del pedido', on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, verbose_name='Producto', on_delete=models.CASCADE)
    amount = models.IntegerField('Cantidad')
    subtotal = models.DecimalField('Subtotal', max_digits=8, decimal_places=2)

    def __str__(self):
        return str(self.id) +' '+ str(self.product)