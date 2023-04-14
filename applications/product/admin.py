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


class ProductImageAdmin(admin.StackedInline):
    model = ProductImage
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin,]

    list_display = (
        'id',
        'product_image',
        'name',
        'price',
        'stock',
        'amount_stock',
        'active',
    )

    list_filter = ('category', 'stock', 'active')

    def product_image(self, obj):
        return format_html('<a href="{}"><img src="{}" style="width: 5rem; height: 5rem; object-fit: contain;"/></a>', obj.product_image.first().image.url, obj.product_image.first().image.url)
    product_image.short_description = 'Product Image'  # Set a custom column header

    # We added a search engine by product name
    search_fields = ['name']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)