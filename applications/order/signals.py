from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Tracking, ShippingCompany

@receiver(pre_save, sender=Tracking)
def tracking_presave(sender, instance, **kwargs):
    if not instance.tracking_link: # We fill the field only if the field is empty
        #Here we set the value of the tracking_link field based on the values ​​of the shipping_company and tracking fields
        link = ShippingCompany.objects.filter(name=instance.shipping_company.name)[0]
        instance.tracking_link =  link.tracking_link + instance.tracking
        # We change the status to Sent
        order_instance = instance.id_order
        order_instance.status = 'Shipped'
        order_instance.save()

