from django.db import models
from .managers import UserManager

# Create your models here.
# we import the libraries for user control
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from model_utils.models import TimeStampedModel

class User(TimeStampedModel, AbstractBaseUser, PermissionsMixin):
    
    name = models.CharField('Nombre', max_length=20)
    last_name = models.CharField('Apellido', max_length=20)
    email = models.EmailField('Correo Electronico', max_length=60, unique=True)
    phone_number = models.CharField('Numero de Telefono', max_length=20, blank=True, null=True)
    id_customer_stripe = models.CharField('ID customer stripe', max_length=25, blank=True, null=True)
    country = models.CharField('Pais', max_length=20, blank=True, null=True)
    state = models.CharField('Estado', max_length=20, blank=True, null=True)
    city = models.CharField('Ciudad', max_length=20, blank=True, null=True)
    address = models.CharField('Dirección', max_length=70, blank=True, null=True)
    postal_code = models.CharField('Codigo Postal', max_length=10, blank=True, null=True)
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

    def get_full_name(self):
        return self.first_name + " " + self.last_name
