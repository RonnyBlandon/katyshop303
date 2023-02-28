from django.db import models
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager, models.Manager):

    def _create_user(self, name, last_name, email, password, is_staff, is_superuser, is_active, **extra_fields):
        user = self.model(
            name=name,
            last_name=last_name,
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=is_active,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user


    def create_user(self, name, last_name, email, password, **extra_fields):
        return self._create_user(name, last_name, email, password, False, False, False, **extra_fields)


    def create_superuser(self, name, last_name, email, password=None, **extra_fields):
        return self._create_user(name, last_name, email, password, True, True, True, **extra_fields)


    def cod_validation(self, id_user: int, validation_code: str):
        user = self.filter(id=id_user, validation_code=validation_code)
        if user:
            return user
        else:
            return False


    def email_exists(self, email: str):
        user = self.filter(email=email)
        if user:
            return user[0]
        else:
            return False


    def get_id_customer_stripe(self, id_user: int):
        user = self.get(id=id_user)
        id_customer = user.id_customer_stripe
        if id_customer:
            return id_customer


class AddressManager(models.Manager):

    def update_address_user(self, id_user, country, state, city, address_1, address_2, postal_code):
        address = self.filter(id_user=id_user)
        address.update(
            country=country,
            state=state,
            city=city,
            address_1=address_1,
            address_2=address_2,
            postal_code=postal_code
        )
        return address
