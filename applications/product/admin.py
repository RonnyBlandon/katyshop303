from django.contrib import admin
from django.utils.html import format_html
# import models
from .models import Category, Product, ProductImage
from applications.cart.models import Cart
# import functions
from applications.cart.shopping_cart import calculate_cart
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
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
        'active'
    )

    list_filter = ('category', 'stock', 'active')

    # We added a search engine by product name
    search_fields = ['name']

    def product_image(self, obj):
        return format_html('<a href="{}"><img src="{}" style="width: 5rem; height: 5rem; object-fit: contain;"/></a>', obj.product_image.first().image.url, obj.product_image.first().image.url)
    product_image.short_description = 'Product Image'  # Set a custom column header

    def save_model(self, request, obj, form, change):
        if change:  # Check if an existing object is being edited
            if form.has_changed():
                if 'price' in form.changed_data:
                    # The carts of all users who have this product are updated with the new price.
                    cart_list = Cart.objects.filter(cart_items__product=obj.id)
                    for cart in cart_list:
                        cart_item = cart.cart_items.filter(product=obj.id).first()
                        cart_item.subtotal = form.cleaned_data["price"] * cart_item.amount
                        cart_item.save()
                        calculate_cart(cart)

        super().save_model(request, obj, form, change)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)