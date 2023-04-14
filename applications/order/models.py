from django.db import models
from model_utils.models import TimeStampedModel
# import models
from applications.product.models import Product
from applications.user.models import User, Country, State
#import signals

# Create your models here.

ORDER_STATUS = (('On hold', 'On hold'), ('Shipped', 'Shipped'), ('Cancelled', 'Cancelled'), ('Refunded', 'Refunded'))
PAYMENT_METHODS = (('Paypal', 'Paypal'), ('Stripe', 'Stripe'))

# Order Models
class Order(models.Model):
    created = models.DateTimeField('Fecha de creación')
    status = models.CharField('Estado', max_length=12, choices=ORDER_STATUS)
    id_user = models.ForeignKey(User, verbose_name='ID del usuario', on_delete=models.CASCADE)
    subtotal = models.DecimalField('Subtotal', max_digits=8, decimal_places=2)
    discount = models.DecimalField('Descuento por puntos', max_digits=8, decimal_places=2, default=0.00)
    total = models.DecimalField('Total', max_digits=8, decimal_places=2)
    payment_method = models.CharField('Metodo de Pago', max_length=20, blank=True, null=True, choices=PAYMENT_METHODS)
    transaction_id = models.CharField('ID Transacción', max_length=50, blank=True, null=True)
    def __str__(self):
        return str(self.id) +' '+ str(self.id_user)


class OrderAddress(models.Model):
    name = models.CharField('Nombre del destinatario', max_length=60)
    country = models.ForeignKey(Country, verbose_name='Pais', on_delete=models.CASCADE)
    state = models.ForeignKey(State, verbose_name='Estado', on_delete=models.CASCADE, blank=True, null=True)
    city = models.CharField('Ciudad', max_length=30)
    # This address_1 is street address
    address_1 = models.CharField('Dirección de calle', max_length=60)
    # This address_2 is apt, suite, unit, building, floor, etc.
    address_2 = models.CharField('Numero de edificio, casa etc.', max_length=60, blank=True, null=True) 
    postal_code = models.CharField('Codigo Postal', max_length=10)
    id_order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_address')

    class Meta:
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return str(self.id) +' '+ self.city +' '+ str(self.state) +' '+ str(self.country) +' '+ str(self.id_order)


class OrderItem(models.Model):
    id_order = models.ForeignKey(Order, verbose_name='ID del pedido', on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, verbose_name='Producto', on_delete=models.CASCADE)
    amount = models.IntegerField('Cantidad')
    unit_price = models.DecimalField('Precio unitario', max_digits=8, decimal_places=2)
    subtotal = models.DecimalField('Subtotal', max_digits=8, decimal_places=2)

    def __str__(self):
        return str(self.id) +' '+ str(self.product)


# Shipping Provider Models
class ShippingCompany(models.Model):
    name = models.CharField('Empresa de envio', max_length=30)
    tracking_link = models.URLField('Enlace para el tracking', max_length=200, blank=True)

    def __str__(self):
        return str(self.id) +' '+ str(self.name)
    

class Tracking(models.Model):
    shipping_company = models.ForeignKey(ShippingCompany, verbose_name='Empresa de envio', on_delete=models.CASCADE)
    id_order = models.ForeignKey(Order, verbose_name='ID Orden', on_delete=models.CASCADE, related_name='order_tracking')
    tracking = models.CharField('Tracking', max_length=50)
    shipping_date = models.DateField('Fecha de envio')
    tracking_link = models.URLField('Enlace del tracking', max_length=200, blank=True)

    def __str__(self):
        return str(self.id) +' '+ str(self.tracking) +' '+str(self.tracking_link)

# Cart models
class Cart(models.Model):
    id_user = models.ForeignKey(User, verbose_name='ID del usuario', on_delete=models.CASCADE)
    subtotal = models.DecimalField('Subtotal', max_digits=8, decimal_places=2)
    total = models.DecimalField('Total', max_digits=8, decimal_places=2)

    def __str__(self):
        return str(self.id)+' '+str(self.id_user)


class CartItem(models.Model):
    id_cart = models.ForeignKey(Order, verbose_name='ID del pedido', on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, verbose_name='Producto', on_delete=models.CASCADE)
    amount = models.IntegerField('Cantidad')
    subtotal = models.DecimalField('Subtotal', max_digits=8, decimal_places=2)

    def __str__(self):
        return str(self.id) +' '+ str(self.product)