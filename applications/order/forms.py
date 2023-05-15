from django import forms
# Imports forms
from applications.user.forms import UserAddressForm

class CheckoutForm(UserAddressForm):
    name = forms.CharField(
        widget=forms.TextInput(
        attrs={'class': 'form-control', 'maxlength': '40'})
    )

    last_name = forms.CharField(
        widget=forms.TextInput(
        attrs={'class': 'form-control', 'maxlength': '40'})
    )

    additional_info = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'class': 'input-additional-info', 'placeholder': 'Notas sobre su pedido, por ejemplo, notas especiales para la entrega.'})
        )

    PAYMENT_METHODS = [('Paypal', 'Paypal'), ('Stripe', 'Tarjeta de Crédito o Débito')]
    payment_method = forms.ChoiceField(
        required=True,
        choices=PAYMENT_METHODS,
        widget=forms.RadioSelect()
    )
