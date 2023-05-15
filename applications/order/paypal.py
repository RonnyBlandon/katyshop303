import requests
import random
import string
from katyshop303.settings.base import get_secret

class Paypal():
    def __init__(self):
        self.url_api = "https://api-m.sandbox.paypal.com"
        self.url_api_order = "https://api-m.sandbox.paypal.com/v2/checkout/orders/"
        self.auth_user = (get_secret('PAYPAL_CLIENT_ID'), get_secret('PAYPAL_CLIENT_SECRET'))
        self.success_url = "http://127.0.0.1:8000/paypal-payment/"
        self.cancel_url = "http://127.0.0.1:8000/paypal-payment/"


    def create_order(self, cart):
        # We prepare the list of cart items to create the paypal order
        items = []
        for product in cart.cart_items.all():
            item = {
                "name": product.product.name,
                "quantity": product.amount,
                "unit_amount": {"currency_code": "USD", "value": str(product.product.price)}    
            }
            items.append(item)

        # We prepare the request to create the order
        headers = {'Content-Type': 'application/json', 'PayPal-Request-Id': generator_paypal_request_id()}
        order = {
            'intent': 'CAPTURE',
            'purchase_units': [
                {
                    'amount': {
                        'currency_code': 'USD', 
                        'value': str(cart.subtotal),
                        'breakdown': {'item_total': {"currency_code": "USD", "value": str(cart.subtotal)}}
                    },
                    'items': items,
                }
            ],
            'payment_source': {
                'paypal': {
                    'experience_context': {
                        'brand_name': 'KatyShop303',
                        'shipping_preference': 'NO_SHIPPING',
                        'user_action': 'PAY_NOW',
                        'payment_method_preference': 'IMMEDIATE_PAYMENT_REQUIRED',
                        'return_url': self.success_url,
                        'cancel_url': self.cancel_url 
                    }
                }
            }
        }
        # we send the request
        resp = requests.post(self.url_api_order, auth=self.auth_user, json=order, headers=headers)
        if resp.status_code == 200:
            data = resp.json()
            for link in data["links"]:
                if link['rel'] == 'payer-action':
                    return link['href']
        else:
            print('Sorry, there was a connection failure. The reason:', resp.content)

    def capture_order(self, token):
        # We prepare the request to capture the order
        headers = {'Content-Type': 'application/json'}
        # we send the request
        url_capture_order = self.url_api_order+token+"/capture"
        resp = requests.post(url_capture_order, auth=self.auth_user, headers=headers)
        if resp.status_code == 201:
            info = resp.json()
            details = info['purchase_units'][0]['payments']['captures'][0] # sacamos los detalles de pago

            data = {'id': details['id'], 'status': details['status'], 'amount': details['amount']['value']}

            return data
        else:
            print('Lo sentimos, hubo un fallo en la conexión. La razón:', resp.content)
            return {'status': 'CANCELLED'}


def generator_paypal_request_id(size=25, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
