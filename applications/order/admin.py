from django.contrib import admin
from applications.user.functions import create_mail
# imports models
from .models import Order, OrderAddress, OrderItem, ShippingCompany, Tracking
# Register your models here.

class OrderAddresAdmin(admin.StackedInline):
    model = OrderAddress
    extra = 0
    max_num = 1


class OrderItemAdmin(admin.TabularInline):
    model = OrderItem
    extra = 0


class TrackingAdmin(admin.TabularInline):
    model = Tracking
    extra = 0
    max_num = 1


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderAddresAdmin, OrderItemAdmin, TrackingAdmin]

    list_display = ('id', 'user', 'created', 'status', 'total')
    list_filter = ('status', 'payment_method')

    def user(self, obj):
        return obj.id_user.name +' '+ obj.id_user.last_name

    def send_order_tracking_email(self, request, queryset):
        for order in queryset:
            # Send the email
            mail = create_mail(
                user_email=order.id_user.email,
                subject=f"Your Katy Shop 303 order is now complete",
                template_name='send_email/customer-order-tracking.html',
                context={
                    'id': order.id, 'created': order.created, 'status': order.status,
                    'tracking':order.order_tracking.first().tracking, 'shipping_date': order.order_tracking.first().shipping_date,
                    'shipping_company': order.order_tracking.first().shipping_company, 'tracking_link': order.order_tracking.first().tracking_link,
                    'items': order.order_items.all, 'subtotal': order.subtotal, 
                    'discount': order.discount, 'payment_method': order.payment_method,
                    'total': order.total, 'name': order.order_address.first().name,
                    'state': order.order_address.first().state, 'country': order.order_address.first().country,
                    'city': order.order_address.first().city, 'address_1': order.order_address.first().address_1,
                    'address_2': order.order_address.first().address_2, 'postal_code': order.order_address.first().postal_code,
                    'user_email': order.id_user.email
                }
            )
            mail.send(fail_silently=False)

        self.message_user(request, "Los correos del tracking han sido enviados.")
    
    def resend_order_email(self, request, queryset):
        for order in queryset:
            # Send the email
            mail = create_mail(
                user_email=order.id_user.email,
                subject=f"Order #{order.id} on Katy Shop 303",
                template_name='send_email/customer-order.html',
                context={
                    'id': order.id, 'created': order.created,
                    'items': order.order_items.all, 'subtotal': order.subtotal, 
                    'discount': order.discount, 'payment_method': order.payment_method,
                    'total': order.total, 'name': order.order_address.first().name,
                    'state': order.order_address.first().state, 'country': order.order_address.first().country,
                    'city': order.order_address.first().city, 'address_1': order.order_address.first().address_1,
                    'address_2': order.order_address.first().address_2, 'postal_code': order.order_address.first().postal_code,
                    'user_email': order.id_user.email
                }
            )
            mail.send(fail_silently=False)

        self.message_user(request, "Los correos de las ordenes se han reenviado.")

    send_order_tracking_email.short_description = "Send order tracking by email"
    resend_order_email.short_description = "Resend orders by email"
    actions = [send_order_tracking_email, resend_order_email]

class ShippingCompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'tracking_link')


admin.site.register(Order, OrderAdmin)
admin.site.register(ShippingCompany, ShippingCompanyAdmin)
