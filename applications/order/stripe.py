import stripe
from katyshop303.settings.base import get_secret
# import models
from applications.user.models import User

class Stripe():
    def __init__(self, id_user):
        stripe.api_key = get_secret("STRIPE_PRIVATE_KEY")
        self.id_user = id_user
        self.success_url = "https://katyshop303.com/webhook-stripe/?id_user="+str(self.id_user)
        self.cancel_url = "https://katyshop303.com/webhook-stripe/?id_user="+str(self.id_user)

    def create_customer_stripe(self):
        user = User.objects.filter(id=self.id_user).first()
        email = user.email
        name = user.name
        last_name = user.last_name

        customer = stripe.Customer.create(
            description="Este usuario es cliente de katyshop303.com",
            email=email,
            name=name+" "+last_name
        )
        user.id_customer_stripe=customer['id']
        user.save()

        return user.id_customer_stripe


    # Function to check if the user's id_customer_stripe exists in the database and in stripe.
    def verify_id_customer_stripe(self):

        id_customer = User.objects.get_id_customer_stripe(self.id_user)
        user = User.objects.filter(id=self.id_user).first()
        email = user.email
        # If the user does not have id_customer in the database, we verify that one exists in stripe with the email.
        if not id_customer:
            customers_exists = stripe.Customer.search(query=f"email:'{email}'",)

            if customers_exists['data']: 
                # If it finds one, we update the user with the id_customer_stripe in the database. 
                user.id_customer_stripe=customers_exists['data'][0].id
                user.save()
                id_customer = customers_exists['data'][0].id
            else:    
                id_customer = self.create_customer_stripe()
    
        else:
            # We verify that the id_customer_stripe that the user has exists in stripe.
            customers_exists = stripe.Customer.search(query=f"email:'{email}'",)
            if not customers_exists['data']:
                id_customer = self.create_customer_stripe()
            else:
                data_customer = customers_exists['data'][0]
                # If the id of the database does not match that of stripe, we update the id of the database.
                if data_customer['id'] != id_customer:
                    user.id_customer_stripe=customers_exists['data'][0].id
                    user.save()
                    id_customer = customers_exists['data'][0].id

        return id_customer


    def create_order(self, order):
    #Since stripe only recognizes the prices of products and services in cents, you only have to send them numbers
    #integers, the amount must be multiplied by 100 to make it the equivalent price from dollars to cents.

        # We prepare the list of cart items to create the paypal order
        items = []
        for product in order.order_items.all():
            item = {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': product.product_name},
                    'unit_amount': int(product.unit_price * 100)
                },
                'quantity': product.amount
            }
            items.append(item)

        # We get the id_customer
        id_customer = self.verify_id_customer_stripe()
        # We create the coupon so that the discount of points in stripe is applied
        if order.discount > 0:
            discount = stripe.Coupon.create(
                amount_off=int(order.discount * 100),
                currency="USD",
                duration="once",
                name="Points Discount"
            )
            # create the payment session for the user
            session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items= items,
            mode='payment',
            customer=id_customer,
            metadata={'id_user': order.id_user.id},
            success_url=self.success_url,
            cancel_url=self.cancel_url,
            discounts=[{'coupon': discount['id']}]
            )
            return session.url
        
        # create the payment session for the user
        session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items= items,
        mode='payment',
        customer=id_customer,
        metadata={'id_user': order.id_user.id},
        success_url=self.success_url,
        cancel_url=self.cancel_url
        )
        return session.url

