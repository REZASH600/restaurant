from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

@shared_task(queue="tasks")
def send_verification_email(email, token):
    subject = 'Verify Your Email'
    message = f'Your verification token is: {token}'

    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
        logger.info(f"Verification email sent to {email}")
    except Exception as e:
        logger.error(f"Failed to send verification email to {email}: {e}")