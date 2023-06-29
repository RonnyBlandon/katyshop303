from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3
# Import models
from .models import User, Country, State
# Import funtions
from .functions import validate_phone_number, validate_postal_code

class UserProfileForm(forms.ModelForm):
    current_password = forms.CharField(required=False,
    	widget = forms.PasswordInput(
            attrs= {
                'class': 'form-control'}
        )
    )
    new_password = forms.CharField(required=False,
    	widget = forms.PasswordInput(
            attrs= {
                'class': 'form-control'})
    )
    repeat_password = forms.CharField(required=False,
        widget = forms.PasswordInput(
            attrs= {
                'class': 'form-control'})
    )
    #captcha = ReCaptchaField(widget=ReCaptchaV3)

    # Form Meta classes
    class Meta:
        model = User
        fields = [
            'name',
            'last_name',
            'phone_number',
        ]
        widgets = {'name': forms.TextInput(
            attrs = {'class': 'form-control'}
        ),
        'last_name': forms.TextInput(
            attrs = {'class': 'form-control'}
        ),
        'phone_number': forms.TextInput(
            attrs = {'class': 'form-control'}
        )}
    

        # We rewrite the __init__ function to pass the user's email to the form from the view
    def __init__(self, id_user, *args, **kwargs):
        self.id_user = id_user
        super(UserProfileForm, self).__init__(*args, **kwargs)

    # Validating passwords and generic phone numbers
    def clean(self):
        phone_number = self.cleaned_data['phone_number']
        if phone_number:
            if not validate_phone_number(phone_number):
                self.add_error('phone_number', _('The phone number cannot contain characters.'))

        # we recover the old password of the user and we verify his old password is correct
        current_password = self.cleaned_data['current_password']
        new_password = self.cleaned_data['new_password']
        repeat_password = self.cleaned_data['repeat_password']
        if current_password:
            user = User.objects.get(id=self.id_user)
            if not check_password(current_password, user.password):
                self.add_error('current_password', _('The current password is not correct.'))
            UserRegisterForm.validate_password(self, new_password, repeat_password)
        else:
            if new_password or repeat_password:
                self.add_error('current_password', _('You must add the current password.'))


class UserAddressForm(forms.Form):
    country = forms.ModelChoiceField(
        queryset=Country.objects.all().values_list('name', flat=True),
        widget=forms.widgets.Select(attrs={'class': ' form-select', 'id': 'select-country'}),
        to_field_name='name'
    )
    state = forms.ModelChoiceField(
        queryset=State.objects.all().values_list('name', flat=True),
        widget=forms.widgets.Select(attrs={'class': 'form-select', 'id': 'select-state'}),
        to_field_name='name',
        required=False
    )
    city = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'maxlength': '30'})   
    )
    address_1 = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'maxlength': '60', 'placeholder': _('House number and street name')})   
    )
    address_2 = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control mt-3', 'maxlength': '60', 
                   'placeholder': _('Apt, suite, unit, building, floor, etc.')})   
    )
    postal_code = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'maxlength': '10'})   
    )

    # We validate the inputs country, state and postal code
    def clean(self):
        country = self.cleaned_data['country']
        if not Country.objects.filter(name=country):
            self.add_error('country', _('Please choose a country from the list.'))

        if country == "United States":
            if not State.objects.filter(name=self.cleaned_data['state']):
                self.add_error('state', _('This field is required for %(country)s') % {'country': country})
        # If Puerto Rico is selected, it is saved in None
        if country == "Puerto Rico":
            self.cleaned_data['state'] = None

        postal_code = self.cleaned_data["postal_code"]
        if postal_code:
            if not validate_postal_code(postal_code):
                self.add_error('postal_code', _('Please enter a valid postcode.'))


# Register Form of User
class UserRegisterForm(forms.ModelForm):
    # Password fields for the user registration form
    password = forms.CharField(required = True,
    	widget = forms.PasswordInput(
            attrs= {
                'class': 'form-register__input', 
                'placeholder': _('Password')})
    )

    repeat_password = forms.CharField(required = True,
    	widget = forms.PasswordInput(
            attrs= {
                'class': 'form-register__input', 
                'placeholder': _('Repeat Password')})
    )
    #captcha = ReCaptchaField(widget=ReCaptchaV3)

    # clases Meta del formulario
    class Meta:
        model = User
        fields = [
            'name',
            'last_name',
            'email',
        ]
        widgets = {'name': forms.TextInput(
            attrs = {'class': 'form-register__input', 'placeholder': _('Name')}
        ),
        'last_name': forms.TextInput(
            attrs = {'class': 'form-register__input', 'placeholder': _('Last name')}
        ),
        'email': forms.EmailInput(
            attrs = {'class': 'form-register__input', 'placeholder': _('Email')}
        )}
    
    # Validation of passwords when creating user
    def validate_password(self, new_password: str, repeat_password: str):

        space = False
        lower_case = False
        upper_case = False
        numbers = False

        for c in new_password:
            if c.isspace():
                space = True
            if c.islower():
                lower_case = True
            if c.isupper():
                upper_case = True
            if c.isnumeric():
                numbers = True

        if new_password != repeat_password:
            self.add_error('repeat_password', _('Passwords do not match.'))
        if len(new_password) < 8:
            self.add_error('repeat_password', _('The password must contain at least 8 characters.'))
        if space == True:
            self.add_error('repeat_password', _('The password must not contain spaces.'))
        if lower_case == False:
            self.add_error('repeat_password', _('The password must contain at least one lowercase letter.'))
        if upper_case == False:
            self.add_error('repeat_password', _('The password must contain at least one upper case.'))
        if numbers == False:
            self.add_error('repeat_password', _('The password must contain at least one number.'))
    
    def clean(self):
        # Validating if the email already exists in the database
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        repeat_password = self.cleaned_data['repeat_password']
        email_exists = User.objects.email_exists(email)
        if email_exists:
            self.add_error('email', _('An account with this email already exists.'))

        UserRegisterForm.validate_password(self, password, repeat_password)


# Login form of User
class UserLoginForm(forms.Form):

    email = forms.CharField(required = True,
        widget = forms.EmailInput(
            attrs= {
                'class': 'form-register__input', 
                'placeholder': _('Email')})
    )

    password = forms.CharField(required = True,
        widget = forms.PasswordInput(
            attrs= {
                'class': 'form-register__input', 
                'placeholder': _('Password')})
    )


    """ the function called clean is the first validation that django does in a form, that's why each
    function that is to validate data from a form must have the name "clean" or "clean_Filename"
    """

    # Validation of the user's email and password for login
    def clean(self):
        cleaned_data = super(UserLoginForm, self).clean()
        try:
            email = cleaned_data['email']
            password = cleaned_data['password']
        except:
            raise forms.ValidationError(_('The user data is not correct.'))

        if not authenticate(email=email, password=password):
            raise forms.ValidationError(_('The user data is not correct.'))

        return self.cleaned_data


class UserVerificationResendForm(forms.Form):
    email = forms.CharField( required=True,
        widget= forms.EmailInput(
            attrs={'class': 'form-register__input', 'placeholder': _('Email')})
    )

    def clean(self):
        email = self.cleaned_data['email']
        user = User.objects.email_exists(email)

        if not user:
            raise forms.ValidationError(_('No user is linked to this email.'))


class EmailPasswordForm(forms.Form):
    email = forms.CharField( required=True,
        widget= forms.EmailInput(
            attrs={'class': 'form-register__input', 'placeholder': _('Email')})
    )

    def clean(self):
        email = self.cleaned_data['email']
        user = User.objects.email_exists(email)

        if not user:
            raise forms.ValidationError(_('No user is linked to this email.'))


class ChangePasswordForm(forms.Form):
    new_password = forms.CharField( required=True,
        widget= forms.PasswordInput(
            attrs={'class': 'form-register__input', 'placeholder': _('New password')}
        )
    )
    repeat_password = forms.CharField( required=True,
        widget= forms.PasswordInput(
            attrs={'class': 'form-register__input', 'placeholder': _('Repeat new password')}
        )
    )

    def clean(self):
        new_password = self.cleaned_data['new_password']
        repeat_password = self.cleaned_data['repeat_password']
        UserRegisterForm.validate_password(self, new_password, repeat_password)
