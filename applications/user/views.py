from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, TemplateView, ListView, DetailView, FormView
from django.utils.translation import gettext_lazy as _
# import of file functions
from .functions import code_generator, create_html_mail, notification_admin_by_mail
from applications.cart.shopping_cart import ShoppingCartCookies
#import models
from .models import User, Address, Country, State
from applications.order.models import Order
from applications.cart.models import Cart
from applications.points.models import PointsHistory
# import forms
from .forms import (UserLoginForm, UserRegisterForm, EmailPasswordForm, ChangePasswordForm, 
UserVerificationResendForm, UserProfileForm, UserAddressForm
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
        current_password = form.cleaned_data['current_password']
        new_password = form.cleaned_data['new_password']
        repeat_password = form.cleaned_data['repeat_password']
        user = self.request.user

        if current_password and new_password and repeat_password:
            authenticated_user = authenticate(
                email=user.email,
                password=form.cleaned_data['current_password']
            )
            if authenticated_user:
                user.name = form.cleaned_data['name']
                user.last_name = form.cleaned_data['last_name']
                user.phone_number = form.cleaned_data['phone_number']
                user.set_password(new_password)
                user.save()

                messages.add_message(request=self.request, level=messages.SUCCESS, message=_('The data has been saved successfully.'))
                messages.add_message(request=self.request, level=messages.SUCCESS, message=_('Password has been changed, please log in.'))

                # Enviamos un correo notificando al email del administrador que se ha creado una cuenta de usuario.
                affair_admin = "USUARIO HA CAMBIADO SU CONTRASEÑA."
                message_admin = f"Un usuario ha cambiado su contraseña y actualizado sus datos. \n\n ID: {user.id} \n Name: {user.name} {user.last_name} \n Email: {user.email}"
                notification_admin_by_mail(affair_admin, message_admin)

                logout(self.request)
                return super(UserProfileView, self).form_valid(form)
            else:
                messages.add_message(request=self.request, level=messages.ERROR, message=_('Password authentication failed. Sign in again.'))
                logout(self.request)
                return super(UserProfileView, self).form_valid(form)

        user.name = form.cleaned_data['name']
        user.last_name = form.cleaned_data['last_name']
        user.phone_number = form.cleaned_data['phone_number']
        user.save()
        messages.add_message(request=self.request, level=messages.SUCCESS, message=_('The data has been saved successfully.'))
        return super(UserProfileView, self).form_valid(form)


class UserAddressView(LoginRequiredMixin, FormView):
    template_name = 'user/user-address.html'
    form_class = UserAddressForm
    login_url = reverse_lazy('user_app:user_login')
    success_url = reverse_lazy('user_app:user_address')

    def get_initial(self):
        initial = super().get_initial()
        address = Address.objects.filter(id_user=self.request.user.id).first()
        if address:
            initial['country'] = address.country.name
            initial['state'] = address.state
            initial['city'] = address.city
            initial['address_1'] = address.address_1
            initial['address_2'] = address.address_2
            initial['postal_code'] = address.postal_code
        
        return initial  

    def form_valid(self, form):
        country = Country.objects.get(name=form.cleaned_data['country'])
        state = form.cleaned_data['state']
        if state:
            if not country == "Puerto Rico":
                state = State.objects.get(name=state)

        if not Address.objects.filter(id_user=self.request.user.id):
            Address.objects.create_address_user(self.request.user, country, state, form.cleaned_data['city'], 
            form.cleaned_data['address_1'], form.cleaned_data['address_2'], form.cleaned_data['postal_code']
        )
        else:
            Address.objects.update_address_user(self.request.user.id, country, state, form.cleaned_data['city'], 
                form.cleaned_data['address_1'], form.cleaned_data['address_2'], form.cleaned_data['postal_code']
            )

        messages.add_message(request=self.request, level=messages.SUCCESS, message=_('The data has been saved successfully.'))
        return super(UserAddressView, self).form_valid(form)


class UserOrderView(ListView):
    template_name = 'order/orders.html'
    model = Order
    paginate_by = 20
    ordering = '-created'

    def get_queryset(self):
        queryset = Order.objects.filter(id_user=self.request.user.id).order_by('-created')
        return queryset


class OrderDetailsView(DetailView):
    template_name = 'order/order_details.html'
    model = Order


class UserPointView(ListView):
    template_name = 'points/points.html'
    model = PointsHistory
    paginate_by = 20
    ordering = '-date'

    def get_queryset(self):
        queryset = PointsHistory.objects.filter(user_points__id_user=self.request.user.id).order_by('-date')
        return queryset


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
            form.cleaned_data['password'],
            validation_code=validation_code
        )
        
        # user cart is created
        Cart.objects.create_cart(subtotal=0.00, total=0.00, user=user)

        # We send the account verification code to the user's email
        mail = create_html_mail(
            user_email=user.email, 
            subject="VERIFICATION CODE", 
            template_name="send_email/email-verification-user.html", 
            context={
                "path_url": f"/verification-code/{user.id}/{validation_code}/",
                "message_context": _("You need to confirm your email to be able to log in."), 
                "btn_text": _("Verify Email")
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
    success_url = reverse_lazy('user_app:user_orders')

    def get(self, request, *args, **kwargs):
        if "page" in self.kwargs:
            if self.kwargs["page"] == "checkout":
                messages.add_message(request, messages.SUCCESS, message=_("Please log in."))
        return super().get(request, *args, **kwargs)
    

    def form_valid(self, form):
        user = authenticate(
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password']
        )

        # we check and update the cart
        cart = ShoppingCartCookies(self.request)
        cart.cookie_cart_to_database(user.id)

        if "page" in self.kwargs:
            if self.kwargs["page"] == "checkout":
                login(self.request, user)
                response = redirect("order_app:checkout")
                response.delete_cookie("cart")
                return response
            
        login(self.request, user)
        response = super(UserLoginView, self).form_valid(form)
        response.delete_cookie("cart")
        return response


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

            if not user:
                messages.add_message(request=self.request, level=messages.ERROR, message=_('The account activation link is invalid.'))
                return HttpResponseRedirect(
                    reverse('user_app:user_login')
                )

            id_user = user[0].id
            name = user[0].name
            last_name = user[0].last_name
            email = user[0].email
            validation_code = code_generator()
            user = user.update(is_active=True, validation_code=validation_code)
            messages.add_message(request=self.request, level=messages.SUCCESS, message=_('The account has been activated successfully, you can now login.'))

            # We send an email notifying the administrator's email that a user account has been verified.
            affair_admin = "SE HA VERIFICADO UNA CUENTA DE USUARIO"
            message_admin = f"Se verificó la cuenta del usuario. \n\n ID: {id_user} \n Name: {name} {last_name} \n Email: {email}"
            notification_admin_by_mail(affair_admin, message_admin)
        
        except Exception as err:
            print("Failed to get user in CodeVerificationView the error is: ", err)
            messages.add_message(request=self.request, level=messages.ERROR, message=_('The account activation link is invalid.'))

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
        mail = create_html_mail(
            user_email=email_user, 
            subject=_("VERIFICATION CODE"), 
            template_name="send_email/email-verification-user.html", 
            context={
                "path_url": f"/verification-code/{id_user}/{validation_code}/",
                "message_context": _("You need to confirm your email to be able to log in."), 
                "btn_text": _("Verify Email")
            }
        )
        mail.send(fail_silently=False)
        messages.add_message(request=self.request, level=messages.SUCCESS, message=_('A new account activation link has been sent to the email "%(email_user)s".') % {'email_user': email_user})

        # We redirect the user to the verification screen to change the password
        return HttpResponseRedirect(self.get_success_url())


class RecoverAccountView(FormView):
    template_name = 'user/forgot-password.html'
    form_class = EmailPasswordForm
    success_url = reverse_lazy('user_app:user_change_password')

    def get_queryset(self):
        queryset = super(RecoverAccountView, self).get_queryset()
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
        mail = create_html_mail(
            user_email=email_user, 
            subject="ACCOUNT RECOVERY", 
            template_name="send_email/email-verification-user.html", 
            context={
                "path_url": f"/change-password/{id_user}/{validation_code}/",
                "message_context": _("You need this link to change your password."),
                "btn_text": _("Change Password")
            }
        )
        mail.send(fail_silently=False)
        messages.add_message(request=self.request, level=messages.SUCCESS, message=_('The link to change the password has been sent to the email "%(email_user)s".') % {'email_user': email_user})

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
            messages.add_message(request=self.request, level=messages.ERROR, message=_('The link is invalid.'))
            return HttpResponseRedirect(
                reverse('user_app:user_login')
            )

        user = User.objects.cod_validation(id_user=id, validation_code=validation_code)
        if not user:
            messages.add_message(request=self.request, level=messages.ERROR, message=_('The link is invalid.'))
            return HttpResponseRedirect(
                reverse('user_app:user_login')
            )
        return self.render_to_response(self.get_context_data())

    def form_valid(self, form):
        id_user = self.kwargs['id']
        user = User.objects.get(id=id_user)
        new_validation_code = code_generator()

        user.validation_code = new_validation_code
        new_password = form.cleaned_data['new_password']
        user.set_password(new_password)
        user.save()
        messages.add_message(request=self.request, level=messages.SUCCESS, message=_('The password has been changed successfully. Sign in.'))

        # We send an email notifying the administrator's email that a user account has been created.
        affair_admin = "USUARIO HA CAMBIADO SU CONTRASEÑA."
        message_admin = f"Un usuario ha cambiado su contraseña. \n\n ID: {user.id} \n Name: {user.name} {user.last_name} \n Email: {user.email}"
        notification_admin_by_mail(affair_admin, message_admin)

        return super(ChangePasswordView, self).form_valid(form)
