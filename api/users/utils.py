from django.conf import settings
from django.core.mail import get_connection, EmailMultiAlternatives, BadHeaderError
from django.http import HttpResponse

from django.template.loader import get_template


def send_email_validation(subject, email, message):
    try:
        mail = EmailMultiAlternatives(
            subject,
            'HUX_GYM',
            settings.EMAIL_HOST_USER,
            [email],
        )
        mail.attach_alternative(message, 'text/html')
        mail.send(fail_silently=True)
    except BadHeaderError:
        return HttpResponse('Error al enviar el correo')
    return True
