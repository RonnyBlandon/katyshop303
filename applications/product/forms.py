from django.forms import ModelForm
# import models
from .models import Product

class ProductAdminForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
