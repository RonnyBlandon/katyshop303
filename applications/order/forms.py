from django import forms
from django.utils.translation import gettext_lazy as _
# Imports forms
from applications.user.forms import UserAddressForm

# website forms
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
            attrs={'class': 'input-additional-info', 'placeholder': _('Notes about your order, for example, special notes for delivery.')})
        )

    PAYMENT_METHODS = [('Paypal', 'Paypal'), ('Stripe', _('Credit or debit card'))]
    payment_method = forms.ChoiceField(
        required=True,
        choices=PAYMENT_METHODS,
        widget=forms.RadioSelect()
    )
