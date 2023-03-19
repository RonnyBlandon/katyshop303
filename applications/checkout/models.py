from django.db import models
from model_utils.models import TimeStampedModel
# import models
from applications.product.models import Product
# Create your models here.

class Cart(TimeStampedModel, models.Model):
    products = models.ManyToManyField(Product, verbose_name='Products')

    def __str__(self):
        return str(self.id) +' '+ str(self.products)
    