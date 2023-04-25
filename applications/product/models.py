# import python
from datetime import datetime, timedelta
# import django
from django.db import models
from model_utils.models import TimeStampedModel
from django.template.defaultfilters import slugify
from ckeditor.fields import RichTextField
from applications.product.managers import ProductManager
# Create your models here.

class Category(TimeStampedModel, models.Model):
    name = models.CharField('Categoria', max_length=20)
    slug = models.SlugField(editable=False, max_length=100)

    def __str__(self):
        return str(self.id)+' '+self.name
    
    # Added unique slugs to categories
    def save(self, *args, **kwargs):
        #We join the product name with the id to create the unique slug
        slug_unique = f"{self.name} {self.id}"
        self.slug = slugify(slug_unique)
        super(Category, self).save(*args, **kwargs)


class Product(TimeStampedModel,models.Model):
    name = models.CharField('Titulo', max_length=50)
    description = RichTextField()
    price = models.DecimalField('Precio', max_digits=7, decimal_places=2)
    stock = models.BooleanField('Disponible')
    amount_stock = models.IntegerField('Cantidad', blank=True, null=True)
    slug = models.SlugField(editable=False, max_length=300)
    category = models.ManyToManyField(Category, verbose_name='Categoria')
    active = models.BooleanField('Producto visible')

    objects = ProductManager()

    def __str__(self):
        return str(self.id)+' - '+self.name
    
    # Added unique slugs to products
    def save(self, *args, **kwargs):
        #We join the product name with the id to create the unique slug
        slug_unique = f"{self.name} {self.id}"
        self.slug = slugify(slug_unique)
        super(Product, self).save(*args, **kwargs)


class ProductImage(models.Model):
    image = models.ImageField(upload_to='product_images/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_image')

    def __str__(self):
        return str(self.id)+' '+str(self.image)+' '+str(self.product)
