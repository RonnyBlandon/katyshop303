from django import forms
from django.utils.translation import gettext_lazy as _
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3


class ContactForm(forms.Form):
    # Password fields for the user registration form
    name = forms.CharField(
        required = True,
    	widget = forms.TextInput(
            attrs= {
                'class': 'form__input--size', 
                'placeholder': _('Name')
            }
        )
    )
    last_name = forms.CharField(
        required = True,
    	widget = forms.TextInput(
            attrs= {
                'class': 'form__input--size', 
                'placeholder': _('Last name')
            }
        )
    )
    email = forms.CharField(
        required = True,
    	widget = forms.EmailInput(
            attrs= {
                'class': 'form__input', 
                'placeholder': _('Email')
            }
        )
    )
    affair = forms.CharField(
        required = True,
    	widget = forms.TextInput(
            attrs= {
                'class': 'form__input', 
                'placeholder': _('affair')
            }
        )
    )
    message = forms.CharField(
        required = True,
    	widget = forms.Textarea(
            attrs= {
                'class': 'form__input', 
                'placeholder': _('Message')
            }
        )
    )
    captcha = ReCaptchaField(widget=ReCaptchaV3)
