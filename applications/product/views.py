from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from django.shortcuts import redirect
# import models
from .models import Product, Category
# Create your views here.
class StoreView(ListView):
    template_name = 'product/store.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 15
    ordering = '-modified'

    def get_queryset(self):
        # Get search string from session variable
        kword = self.request.GET.get("kword")
        products = Product.objects.search_product_trgm(kword)
        if not products:
            return Product.objects.all().order_by('-modified')
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ProductView(DetailView):
    template_name = 'product/product.html'
    model = Product


class CategoryView(DetailView):
    template_name = 'product/category.html'
    model = Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        list_product = Product.objects.prdoucts_by_category(self.kwargs['slug']).order_by('-modified')
        paginator = Paginator(list_product, 15)
        page = self.request.GET.get('page')
        context['products'] = paginator.get_page(page)
        context['categories'] = Category.objects.all()
        return context