import random
import string
from django.core.mail import send_mail
from django.conf import settings


def generate_verification_code(length=6):
    return ''.join(random.choices(string.digits, k=length))


def send_verification_email(email, code):
    subject = "Email tasdiqlash kodi"
    message = f"Sizning tasdiqlash kodingiz: {code}"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)
