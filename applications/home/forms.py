from django import forms
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3


class ContactForm(forms.Form):
    # Password fields for the user registration form
    name = forms.CharField(
        required = True,
    	widget = forms.TextInput(
            attrs= {
                'class': 'form__input--size', 
                'placeholder': 'Name'
            }
        )
    )
    last_name = forms.CharField(
        required = True,
    	widget = forms.TextInput(
            attrs= {
                'class': 'form__input--size', 
                'placeholder': 'Last name'
            }
        )
    )
    email = forms.CharField(
        required = True,
    	widget = forms.EmailInput(
            attrs= {
                'class': 'form__input', 
                'placeholder': 'Email'
            }
        )
    )
    affair = forms.CharField(
        required = True,
    	widget = forms.TextInput(
            attrs= {
                'class': 'form__input', 
                'placeholder': 'affair'
            }
        )
    )
    message = forms.CharField(
        required = True,
    	widget = forms.Textarea(
            attrs= {
                'class': 'form__input', 
                'placeholder': 'Message'
            }
        )
    )
    captcha = ReCaptchaField(widget=ReCaptchaV3)
