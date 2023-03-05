from django.db import models
from model_utils.models import TimeStampedModel
# Create your models here.

class Category(TimeStampedModel, models.Model):
    name = models.CharField('Categoria', max_length=20)
    def __str__(self):
        return str(self.id)+' '+self.name


class Product(models.Model):
    name = models.CharField('Titulo', max_length=50)
    description = models.TextField('Description', blank=True)
    price = models.DecimalField('Precio', max_digits=7, decimal_places=2)
    stock = models.BooleanField('Disponible')
    amount_stock = models.IntegerField('Cantidad en existencia.')
    active = models.BooleanField('Producto visible')
    category = models.ManyToManyField(Category, verbose_name='Categoria')


    def __str__(self):
        return str(self.id)+' '+self.name+' '+str(self.price)+''+str(self.stock)+' '+str(self.active)
