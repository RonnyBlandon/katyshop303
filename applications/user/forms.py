from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3
# Import models from app users
from .models import User

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

    # clases Meta del formulario
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

    # Validation of passwords for changing them
    def clean(self):
        current_password = self.cleaned_data['current_password']
        new_password = self.cleaned_data['new_password']
        repeat_password = self.cleaned_data['repeat_password']
        
        # we recover the old password of the user and we verify his old password is correct
        if current_password:
            user = User.objects.get(id=self.id_user)
            if not check_password(current_password, user.password):
                self.add_error('current_password', 'La contraseña actual no es correcta.')
            UserRegisterForm.validate_password(self)
        else:
            if new_password or repeat_password:
                self.add_error('current_password', 'Debe agregar la contraseña actual.')



# Register Form of User
class UserRegisterForm(forms.ModelForm):
    # Campos de las contraseña para el formulario de registro de usuario
    password1 = forms.CharField(required = True,
    	widget = forms.PasswordInput(
            attrs= {
                'class': 'form-register__input', 
                'placeholder': 'Contraseña'})
    )

    password2 = forms.CharField(required = True,
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
    def validate_password(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        espacio = False
        minuscula = False
        mayuscula = False
        numeros = False

        for c in password1:
            if c.isspace():
                espacio = True
            if c.islower():
                minuscula = True
            if c.isupper():
                mayuscula = True
            if c.isnumeric():
                numeros = True

        if password1 != password2:
            self.add_error('password2', 'Las contraseñas no coinciden.')
        if len(password1) < 8:
            self.add_error('password2', 'La contraseña debe contener al menos 8 caracteres.')
        if espacio == True:
            self.add_error('password2', 'La contraseña no debe contener espacios.')
        if minuscula == False:
            self.add_error('password2', 'La contraseña debe contener al menos una letra minúscula.')
        if mayuscula == False:
            self.add_error('password2', 'La contraseña debe contener al menos una letra mayúscula.')
        if numeros == False:
            self.add_error('password2', 'La contraseña debe contener al menos un numero.')
    
    def clean(self):
        # Validating if the email already exists in the database
        email = self.cleaned_data['email']
        email_exists = User.objects.email_exists(email)
        if email_exists:
            self.add_error('email', 'Ya existe una cuenta con este correo electrónico.')

        UserRegisterForm.validate_password(self)


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
    password1 = forms.CharField( required=True,
        widget= forms.PasswordInput(
            attrs={'class': 'form-register__input', 'placeholder': 'Contraseña nueva'}
        )
    )
    password2 = forms.CharField( required=True,
        widget= forms.PasswordInput(
            attrs={'class': 'form-register__input', 'placeholder': 'Repetir nueva contraseña'}
        )
    )

    def clean(self):
        UserRegisterForm.validate_password(self)
