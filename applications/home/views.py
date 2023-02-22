from django.views.generic import TemplateView, FormView
from django.urls import reverse
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.contrib import messages
# imports form
from .forms import ContactForm
#
from katyshop303.settings.base import get_secret

# Create your views here.

class HomeView(TemplateView):
    template_name = 'home/home.html'


class ContactView(FormView):
    template_name = 'home/contact.html'
    form_class = ContactForm
    success_url = '.'

    def form_valid(self, form):
        try:
            # We send the message to the email for support
            name = form.cleaned_data['name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            affair = form.cleaned_data['affair']
            mensaje = 'PAGINA DE CONTACTO' + '\n\n' + 'Mi nombre es: ' + name + ' ' + last_name + '\n' + 'Mi correo es: ' + email + '\n\n' +form.cleaned_data['message']
            email_remitente = get_secret('EMAIL')
            send_mail(affair, mensaje, email_remitente, [email_remitente,])

            messages.add_message(request=self.request, level=messages.WARNING, message='Su mensaje fue enviado con exito. Muy pronto recibira una respuesta en su correo.')
        except Exception as err:
            print("Error on the contact page the error is: ", err)
            messages.add_message(request=self.request, level=messages.ERROR, message='Error en el envío, inténtelo más tarde.')
        # Redirigimos a la misma pagina de contacto
        
        return HttpResponseRedirect(
            reverse('home_app:contact')
        )


class PointsRulesView(TemplateView):
    template_name = 'home/points-rules.html'


class TermsView(TemplateView):
    template_name = 'home/terms.html'


class PrivacyPolicyView(TemplateView):
    template_name = 'home/privacy-policy.html'
