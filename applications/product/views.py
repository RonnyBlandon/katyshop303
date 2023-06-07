from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
# import models
from .models import Product, Category
from applications.points.models import PointsSetting
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
            return Product.objects.all().order_by('-created')
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ProductView(DetailView):
    template_name = 'product/product.html'
    model = Product

    def get_context_data(self, **kwargs):
        # We add to the context the points that can be earned if you buy the product
        points_setting = PointsSetting.objects.get_point_setting()
        context = super(ProductView, self).get_context_data(**kwargs)
        context['product_points'] = round(kwargs['object'].price * points_setting.earning_points_rate)
        return context
    


class CategoryView(DetailView):
    template_name = 'product/category.html'
    model = Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        list_product = Product.objects.products_by_category(self.kwargs['slug']).order_by('-modified')
        paginator = Paginator(list_product, 15)
        page = self.request.GET.get('page')
        context['products'] = paginator.get_page(page)
        context['categories'] = Category.objects.all()
        return context