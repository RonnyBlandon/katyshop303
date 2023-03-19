from django import forms
# Import models
from applications.user.models import User, Address, Country, State
# Imports forms
from applications.user.forms import UserAddressForm

class CheckoutForm(UserAddressForm):
    additional_info = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'input-additional-info', 'placeholder': 'Notas sobre su pedido, por ejemplo, notas especiales para la entrega.'})
        )

    PAYMENT_METHODS = [('paypal', 'paypal'), ('stripe', 'Tarjeta de Crédito o Débito')]
    payment_method = forms.ChoiceField(
        required=True,
        choices=PAYMENT_METHODS,
        widget=forms.RadioSelect()
    )
