from django.db import models
from model_utils.models import TimeStampedModel
# import models
from applications.product.models import Product
from applications.user.models import User
# Create your models here.


class Cart(TimeStampedModel, models.Model):
    id_user = models.ForeignKey(User, verbose_name='ID del usuario', on_delete=models.CASCADE)
    subtotal = models.DecimalField('Subtotal', max_digits=8, decimal_places=2)
    
    def __str__(self):
        return str(self.id) +' '+ str(self.id_user)


class ProductCart(TimeStampedModel, models.Model):
    id_cart = models.ForeignKey(Cart, verbose_name='ID del carrito', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Producto', on_delete=models.CASCADE)
    amount = models.IntegerField('Cantidad')
    subtotal = models.DecimalField('Subtotal', max_digits=8, decimal_places=2)

    def __str__(self):
        return str(self.id) +' '+ str(self.product)
