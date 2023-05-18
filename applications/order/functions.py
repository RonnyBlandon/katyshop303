# import functions
from katyshop303.settings.base import get_secret
from applications.user.functions import create_html_mail

def send_order_to_user(order):
# We mail the order to the user.
    mail = create_html_mail(
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
            'user_email': order.id_user.email, 'user_name': order.id_user.name+" "+order.id_user.last_name
        }
    )
    mail.send(fail_silently=False)
    # Notify the administrators of the new order.
    mail_admin = create_html_mail(
        user_email=get_secret("EMAIL"),
        subject=f"[Katy Shop 303]: New order #{order.id}",
        template_name='send_email/admin-order.html',
        context={
            'id': order.id, 'created': order.created,
            'items': order.order_items.all, 'subtotal': order.subtotal, 
            'discount': order.discount, 'payment_method': order.payment_method,
            'total': order.total, 'name': order.order_address.first().name,
            'state': order.order_address.first().state, 'country': order.order_address.first().country,
            'city': order.order_address.first().city, 'address_1': order.order_address.first().address_1,
            'address_2': order.order_address.first().address_2, 'postal_code': order.order_address.first().postal_code,
            'user_email': order.id_user.email, 'user_name': order.id_user.name+" "+order.id_user.last_name
        }
    )
    mail_admin.send(fail_silently=False)