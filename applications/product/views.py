from django.views.generic import ListView, DetailView
# import models
from .models import Product, Category
# Create your views here.
class StoreView(ListView):
    template_name = 'product/store.html'
    model = Product
    context_object_name = 'products'


class ProductView(DetailView):
    template_name = 'product/product.html'
    model = Product
    context_object_name = 'product'


