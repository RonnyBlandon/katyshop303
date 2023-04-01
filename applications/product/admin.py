from django.contrib import admin
from django.utils.html import format_html
# import models
from .models import Category, Product, ProductImage
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',
    )
    # We added a search engine by category name
    search_fields = ['name']


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'price',
        'stock',
        'amount_stock',
        'active',
    )

    list_filter = ('category', 'stock', 'active')
    # We added a search engine by product name
    search_fields = ['name']


class ProductImageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'photo',
        'product',
    )

    # We added a search engine by product name
    search_fields = ['product__name']
    raw_id_fields = ("product",)
    # function show product images
    def photo(self, obj):
        print(obj)
        return format_html('<a href={}><img src={} style="width: 6rem; height: 6rem; object-fit: contain;"></a>', obj.image.url, obj.image.url)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)