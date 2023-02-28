from django import forms
#from django.forms import widgets
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3
# Import models
from .models import User, Address, Country, State
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
                self.add_error('phone_number', 'El numero de telefono no puede contener caracteres.')

        # we recover the old password of the user and we verify his old password is correct
        current_password = self.cleaned_data['current_password']
        new_password = self.cleaned_data['new_password']
        repeat_password = self.cleaned_data['repeat_password']
        if current_password:
            user = User.objects.get(id=self.id_user)
            if not check_password(current_password, user.password):
                self.add_error('current_password', 'La contraseña actual no es correcta.')
            UserRegisterForm.validate_password(self, new_password, repeat_password)
        else:
            if new_password or repeat_password:
                self.add_error('current_password', 'Debe agregar la contraseña actual.')


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
            attrs={'class': 'form-control', 'maxlength': '60', 'placeholder': 'Numero de Casa y nombre de la calle'})   
    )
    address_2 = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control mt-3', 'maxlength': '60', 
                   'placeholder': 'Depto, unidad, edificio, piso, etc.'})   
    )
    postal_code = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'maxlength': '10'})   
    )

    # We validate the inputs country, state and postal code
    def clean(self):
        country = self.cleaned_data['country']
        if not Country.objects.filter(name=country):
            self.add_error('country', 'Por favor elija un país dentro de la lista.')

        if country == "Estados Unidos":
            if not State.objects.filter(name=self.cleaned_data['state']):
                self.add_error('state', f'Este campo es obligatorio para {country}.')
        # If Puerto Rico is selected, it is saved in None
        if country == "Puerto Rico":
            self.cleaned_data['state'] = None

        postal_code = self.cleaned_data["postal_code"]
        if postal_code:
            if not validate_postal_code(postal_code):
                self.add_error('postal_code', 'Por favor ingrese un código postal válido.')


# Register Form of User
class UserRegisterForm(forms.ModelForm):
    # Campos de las contraseña para el formulario de registro de usuario
    password = forms.CharField(required = True,
    	widget = forms.PasswordInput(
            attrs= {
                'class': 'form-register__input', 
                'placeholder': 'Contraseña'})
    )

    repeat_password = forms.CharField(required = True,
    	widget = forms.PasswordInput(
            attrs= {
                'class': 'form-register__input', 
                'placeholder': 'Repetir Contraseña'})
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
            attrs = {'class': 'form-register__input', 'placeholder': 'Nombre'}
        ),
        'last_name': forms.TextInput(
            attrs = {'class': 'form-register__input', 'placeholder': 'Apellido'}
        ),
        'email': forms.EmailInput(
            attrs = {'class': 'form-register__input', 'placeholder': 'Correo Electronico'}
        )}
    
    # Validation of passwords when creating user
    def validate_password(self, new_password: str, repeat_password: str):

        espacio = False
        minuscula = False
        mayuscula = False
        numeros = False

        for c in new_password:
            if c.isspace():
                espacio = True
            if c.islower():
                minuscula = True
            if c.isupper():
                mayuscula = True
            if c.isnumeric():
                numeros = True

        if new_password != repeat_password:
            self.add_error('repeat_password', 'Las contraseñas no coinciden.')
        if len(new_password) < 8:
            self.add_error('repeat_password', 'La contraseña debe contener al menos 8 caracteres.')
        if espacio == True:
            self.add_error('repeat_password', 'La contraseña no debe contener espacios.')
        if minuscula == False:
            self.add_error('repeat_password', 'La contraseña debe contener al menos una letra minúscula.')
        if mayuscula == False:
            self.add_error('repeat_password', 'La contraseña debe contener al menos una letra mayúscula.')
        if numeros == False:
            self.add_error('repeat_password', 'La contraseña debe contener al menos un numero.')
    
    def clean(self):
        # Validating if the email already exists in the database
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        repeat_password = self.cleaned_data['repeat_password']
        email_exists = User.objects.email_exists(email)
        if email_exists:
            self.add_error('email', 'Ya existe una cuenta con este correo electrónico.')

        UserRegisterForm.validate_password(self, password, repeat_password)


# Login form of User
class UserLoginForm(forms.Form):

    email = forms.CharField(required = True,
        widget = forms.EmailInput(
            attrs= {
                'class': 'form-register__input', 
                'placeholder': 'Correo Electronico'})
    )

    password = forms.CharField(required = True,
        widget = forms.PasswordInput(
            attrs= {
                'class': 'form-register__input', 
                'placeholder': 'Contraseña'})
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
            raise forms.ValidationError('Los datos de ususario no son correctos.')

        if not authenticate(email=email, password=password):
            raise forms.ValidationError('Los datos de ususario no son correctos.')

        return self.cleaned_data


class UserVerificationResendForm(forms.Form):
    email = forms.CharField( required=True,
        widget= forms.EmailInput(
            attrs={'class': 'form-register__input', 'placeholder': 'Correo Electrónico'})
    )

    def clean(self):
        email = self.cleaned_data['email']
        user = User.objects.email_exists(email)

        if not user:
            raise forms.ValidationError('Ningún usuario está ligado a este correo.')


class EmailPasswordForm(forms.Form):
    email = forms.CharField( required=True,
        widget= forms.EmailInput(
            attrs={'class': 'form-register__input', 'placeholder': 'Correo Electrónico'})
    )

    def clean(self):
        email = self.cleaned_data['email']
        user = User.objects.email_exists(email)

        if not user:
            raise forms.ValidationError('Ningún usuario está ligado a este correo.')


class ChangePasswordForm(forms.Form):
    new_password = forms.CharField( required=True,
        widget= forms.PasswordInput(
            attrs={'class': 'form-register__input', 'placeholder': 'Contraseña nueva'}
        )
    )
    repeat_password = forms.CharField( required=True,
        widget= forms.PasswordInput(
            attrs={'class': 'form-register__input', 'placeholder': 'Repetir nueva contraseña'}
        )
    )

    def clean(self):
        new_password = self.cleaned_data['new_password']
        repeat_password = self.cleaned_data['repeat_password']
        UserRegisterForm.validate_password(self, new_password, repeat_password)
