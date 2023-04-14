from django.db import models
from .managers import UserManager, AddressManager

# Create your models here.
# we import the libraries for user control
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from model_utils.models import TimeStampedModel

class User(TimeStampedModel, AbstractBaseUser, PermissionsMixin):
    name = models.CharField('Nombre', max_length=40)
    last_name = models.CharField('Apellido', max_length=40)
    email = models.EmailField('Correo Electronico', max_length=60, unique=True)
    phone_number = models.CharField('Numero de Telefono', max_length=20, blank=True, null=True)
    id_customer_stripe = models.CharField('ID customer stripe', max_length=25, blank=True, null=True)
    validation_code = models.CharField('Código de Validación', max_length=6)
    # We create the column staff in model for the creation of superusers
    is_staff = models.BooleanField(default=False)
    # new column to check if the mail is real
    is_active = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return str(self.id) + ' - ' + self.name + ' ' + self.last_name + ' - ' + self.email


class Country(models.Model):
    name = models.CharField('Nombre del Pais:', max_length=20, unique=True)
    class Meta:
        verbose_name_plural = 'Countries'

    def __str__(self):
        return str(self.id) + ' '+ self.name


class State(models.Model):
    name = models.CharField('Nombre del Estado:', max_length=20, unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) +' '+ self.name +' - '+ str(self.country)


class Address(models.Model):
    country = models.ForeignKey(Country, verbose_name='Pais', on_delete=models.CASCADE)
    state = models.ForeignKey(State, verbose_name='Estado', on_delete=models.CASCADE, blank=True, null=True)
    city = models.CharField('Ciudad', max_length=30)
    # This address_1 is street address
    address_1 = models.CharField('Dirección de calle', max_length=60)
    # This address_2 is apt, suite, unit, building, floor, etc.
    address_2 = models.CharField('Numero de edificio, casa etc.', max_length=60, blank=True, null=True) 
    postal_code = models.CharField('Codigo Postal', max_length=10)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Addresses'

    objects = AddressManager()

    def __str__(self):
        return str(self.id) +' '+ self.city +' '+ str(self.state) +' '+ str(self.country) +' '+ str(self.id_user)
