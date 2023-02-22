"""Extra python functions for the users application."""
import random
import string
import re
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import get_template
from katyshop303.settings.base import get_secret

def code_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def notification_admin_by_mail(affair: str, message: str):
    # We send an event notification email
    email_remitente = get_secret("EMAIL")
    send_mail(affair, message, email_remitente, [email_remitente,])


def create_mail(user_email, subject, template_name, context):
    template = get_template(template_name)
    content = template.render(context)

    message = EmailMultiAlternatives(
        subject=subject,
        body='',
        from_email=get_secret("EMAIL"),
        to=[
            user_email
        ],
        cc=[]
    )

    message.attach_alternative(content, 'text/html')
    return message


def validate_phone_number(phone_numer: str):
  
    pattern = re.compile(r'^+?')
    coincidence = re.match(pattern, phone_numer)
    if coincidence:
        return True
    else:
        return False
