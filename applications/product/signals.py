from django.db.models.signals import post_save
from django.dispatch import receiver
# import of functions
from applications.user.functions import notification_admin_by_mail
# mport models
from .models import Product


@receiver(post_save, sender=Product)
def product_postsave(sender, instance, **kwargs):

    if instance.stock and instance.amount_stock and instance.amount_stock <= 3:
        # We send an email notifying the administrator that the stock of this product is running out.
        affair_admin = "ALERTA DE AGOTAMIENTO DE STOCK"
        message_admin = f'Kary Mcfred \n\nEste correo es para informarle que el producto "{instance.name}" se está agotando, solo quedan {instance.amount_stock} unidades. Le recomendamos aumentar el stock y evitar posibles interrupciones en el suministro.\n\n Enviado por el sistema de admin de KatyShop303.'
        notification_admin_by_mail(affair_admin, message_admin)
