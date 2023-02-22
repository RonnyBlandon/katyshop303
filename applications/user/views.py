from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, TemplateView, FormView
# import of file functions
from .functions import code_generator, create_mail, notification_admin_by_mail
#import models
from .models import User
# import forms
from .forms import (UserLoginForm, UserRegisterForm, EmailPasswordForm, ChangePasswordForm, 
UserVerificationResendForm, UserProfileForm
)
# Create your views here.

class UserProfileView(LoginRequiredMixin, FormView):
    template_name = 'user/user-profile.html'
    form_class = UserProfileForm
    login_url = reverse_lazy('user_app:user_login')
    success_url = reverse_lazy('user_app:user_profile')

    def get_initial(self):
        initial = super().get_initial()
        initial['name'] = self.request.user.name
        initial['last_name'] = self.request.user.last_name
        initial['phone_number'] = self.request.user.phone_number
        return initial

    def get_form_kwargs(self):
        kwargs = super(UserProfileView, self).get_form_kwargs()
        kwargs.update({
            'id_user': self.request.user.id
        })
        return kwargs

    def form_valid(self, form):
        name = form.cleaned_data['name']
        last_name = form.cleaned_data['last_name']
        phone_number = form.cleaned_data['phone_number']
        current_password = form.cleaned_data['current_password']
        new_password = form.cleaned_data['new_password']
        repeat_password = form.cleaned_data['repeat_password']
        user = self.request.user

        if current_password and new_password and repeat_password:
            print("Parece que si entra con los campos vacios")
            authenticated_user = authenticate(
                id=user.id,
                password=form.cleaned_data['current_password']
            )

            if authenticated_user:
                user.name = name
                user.last_name = last_name
                user.phone_number = phone_number
                user.set_password(new_password)
                user.save()

                messages.add_message(request=self.request, level=messages.SUCCESS, message='Los datos se han guardado con éxito.')
                messages.add_message(request=self.request, level=messages.SUCCESS, message='Se ha cambiado la contraseña, inicie sesión.')

                # Enviamos un correo notificando al email del administrador que se ha creado una cuenta de usuario.
                affair_admin = "USUARIO HA CAMBIADO SU CONTRASEÑA."
                message_admin = f"Un usuario ha cambiado su contraseña y actualizado sus datos. \n\n ID: {user.id} \n Name: {user.name} {user.last_name} \n Email: {user.email}"
                notification_admin_by_mail(affair_admin, message_admin)

                logout(self.request)
                return super(UserProfileView, self).form_valid(form)
            else:
                messages.add_message(request=self.request, level=messages.ERROR, message='Error en la autenticación de la contraseña. Vuelva a iniciar sesión.')
                logout(self.request)
                return super(UserProfileView, self).form_valid(form)

        user.name = name
        user.last_name = last_name
        user.phone_number = phone_number
        user.save()
        messages.add_message(request=self.request, level=messages.SUCCESS, message='Los datos se han guardado con éxito.')
        print("No entra en el if de las contraseñas")
        return super(UserProfileView, self).form_valid(form)


class UserAddressView(LoginRequiredMixin, TemplateView):
    template_name = 'user/user-address.html'
    login_url = reverse_lazy('user_app:user_login')

    def get_context_data(self, **kwargs):
        context = super(UserAddressView, self).get_context_data(**kwargs)
        return context


class UserRegisterView(FormView):
    template_name = 'user/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('users_app:user_login')

    def form_valid(self, form):
        # We generate the email verification code for the newly registered user
        validation_code = code_generator()
        
        name = form.cleaned_data['name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email']
        user = User.objects.create_user(
            name,
            last_name,
            email,
            form.cleaned_data['password1'],
            validation_code=validation_code
        )

        # We send the account verification code to the user's email
        mail = create_mail(
            user_email=user.email, 
            subject="CÓDIGO DE VERIFICACIÓN", 
            template_name="send_email/email-verification-user.html", 
            context={
                "path_url": f"/verification-code/{user.id}/{validation_code}/",
                "message_context": "Necesitas confirmar tu correo para poder iniciar sesión.", 
                "btn_text": "Verificar Correo electrónico"
            }
        )
        mail.send(fail_silently=False)
        # We send an email notifying the administrator's email that a user account has been created.
        affair_admin = "NUEVA CUENTA DE USUARIO."
        message_admin = f"Se ha creado una nueva cuenta de usuario sin verificar. \n\n ID: {user.id} \n Name: {name} {last_name} \n Email: {email}"
        notification_admin_by_mail(affair_admin, message_admin)

        # We will redirect to the login page
        return HttpResponseRedirect(
            reverse('user_app:user_thank_you')
        )


class UserLoginView(FormView):
    template_name = 'user/login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('user_app:user_profile')

    def form_valid(self, form):
        user = authenticate(
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password']
        )
        login(self.request, user)

        return super(UserLoginView, self).form_valid(form)


class LogoutView(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(
            reverse('user_app:user_login')
        )


class CodeVerificationView(View):
    # We rewrite this function to pass the pk to the Form from the View
    def get(self, request, *args, **kwargs):

        try:
            user = User.objects.filter(
                id=self.kwargs['id'],
                validation_code=self.kwargs['code']
            )
        except Exception as err:
            print("Error al obtener el usuario en CodeVerificationView el error es: ", err)
            messages.add_message(request=self.request, level=messages.ERROR, message=f'El enlace de verificación de cuenta no es válido.')
            return HttpResponseRedirect(
                reverse('user_app:user_login')
            )

        if user[0].is_active:
            messages.add_message(request=self.request, level=messages.ERROR, message=f'El enlace de verificación no es válido, además esta cuenta ya está verificada, ya puede iniciar sesión.')
            return HttpResponseRedirect(
                reverse('user_app:user_login')
            )

        id_user = user[0].id
        name = user[0].name
        last_name = user[0].last_name
        email = user[0].email
        validation_code = code_generator()
        user = user.update(is_active=True, validation_code=validation_code)
        messages.add_message(request=self.request, level=messages.SUCCESS, message='La cuenta se ha verificado con éxito, ya puede iniciar sesión.')

        # We send an email notifying the administrator's email that a user account has been verified.
        affair_admin = "SE HA VERIFICADO UNA CUENTA DE USUARIO"
        message_admin = f"Se verificó la cuenta del usuario. \n\n ID: {id_user} \n Name: {name} {last_name} \n Email: {email}"
        notification_admin_by_mail(affair_admin, message_admin)

        return HttpResponseRedirect(
                reverse('user_app:user_login')
            )


class UserThankYouView(TemplateView):
    template_name = 'user/thanks-for-register.html'


class UserVerificationResendView(FormView):
    template_name = 'user/resend-user-verification.html'
    form_class = UserVerificationResendForm
    success_url = reverse_lazy('user_app:user_resend_email')

    def form_valid(self, form):
        # We generate the verification code to the email of the user who forgot his password
        validation_code = code_generator()

        email = form.cleaned_data['email']
        user = User.objects.filter(email=email)
        # We update the new code to the user in the database
        id_user = user[0].id
        email_user = user[0].email
        user.update(validation_code=validation_code)

        # We send the account verification code to the user's email
        mail = create_mail(
            user_email=email_user, 
            subject="CÓDIGO DE VERIFICACIÓN", 
            template_name="send_email/email-verification-user.html", 
            context={
                "path_url": f"/verification-code/{id_user}/{validation_code}/",
                "message_context": "Necesitas confirmar tu correo para poder iniciar sesión.", 
                "btn_text": "Verificar Correo electrónico"
            }
        )
        mail.send(fail_silently=False)
        messages.add_message(request=self.request, level=messages.SUCCESS, message=f'Se ha enviado un nuevo enlace para la activación de cuenta al correo "{email_user}".')

        # We redirect the user to the verification screen to change the password
        return HttpResponseRedirect(self.get_success_url())


class RecoverAccountView(FormView):
    template_name = 'user/forgot-password.html'
    form_class = EmailPasswordForm
    success_url = reverse_lazy('user_app:user_change_password')

    def get_queryset(self):
        queryset = super(RecoverAccountView, self).get_queryset()
        print(queryset)
        queryset = queryset.id
        return queryset

    def form_valid(self, form):
        # We generate the verification code to the email of the user who forgot his password
        validation_code = code_generator()

        email = form.cleaned_data['email']
        user = User.objects.filter(email=email)
        # We update the new code to the user in the database
        id_user = user[0].id
        email_user = user[0].email
        user.update(validation_code=validation_code)

        # We send the verification code to change the password to the user
        mail = create_mail(
            user_email=email_user, 
            subject="RECUPERACIÓN DE CUENTA", 
            template_name="send_email/email-verification-user.html", 
            context={
                "path_url": f"/change-password/{id_user}/{validation_code}/",
                "message_context": "Necesitas este enlace para cambiar la contraseña.",
                "btn_text": "Cambiar Contraseña"
            }
        )
        mail.send(fail_silently=False)
        messages.add_message(request=self.request, level=messages.SUCCESS, message=f'Se ha enviado el enlace para cambiar la contraseña al correo "{email_user}".')

        # We redirect the user to the verification screen to change the password
        return HttpResponseRedirect(
            reverse('user_app:user_login')
        )


# This view is to change the password of users who are not logged in
class ChangePasswordView(FormView):
    template_name = 'user/change-password.html'
    form_class = ChangePasswordForm
    success_url = reverse_lazy('user_app:user_login')

    def get(self, request, *args, **kwargs):
        try:
            id = self.kwargs['id']
            validation_code = self.kwargs['code']

        except:
            messages.add_message(request=self.request, level=messages.ERROR, message='El enlace es inválido.')
            return HttpResponseRedirect(
                reverse('user_app:user_login')
            )

        user = User.objects.cod_validation(id_user=id, validation_code=validation_code)
        if not user:
            messages.add_message(request=self.request, level=messages.ERROR, message='El enlace es inválido.')
            return HttpResponseRedirect(
                reverse('user_app:user_login')
            )
        return self.render_to_response(self.get_context_data())

    def form_valid(self, form):
        id_user = self.kwargs['id']
        user = User.objects.get(id=id_user)
        new_validation_code = code_generator()

        user.validation_code = new_validation_code
        new_password = form.cleaned_data['password2']
        user.set_password(new_password)
        user.save()
        messages.add_message(request=self.request, level=messages.SUCCESS, message='Se ha cambiado la contraseña con éxito. Inicie sesión.')

        # We send an email notifying the administrator's email that a user account has been created.
        affair_admin = "USUARIO HA CAMBIADO SU CONTRASEÑA."
        message_admin = f"Un usuario ha cambiado su contraseña. \n\n ID: {user.id} \n Name: {user.name} {user.last_name} \n Email: {user.email}"
        notification_admin_by_mail(affair_admin, message_admin)

        return super(ChangePasswordView, self).form_valid(form)
