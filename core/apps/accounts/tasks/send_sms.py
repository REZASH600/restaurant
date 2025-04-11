
from celery import shared_task
# from kavenegar import KavenegarAPI, KavenegarAPIException
from django.conf import settings
import logging

logger = logging.getLogger(__name__)



@shared_task(queue="tasks")
def send_verification_sms(phone, token):
    if settings.DEBUG:
        print(f"[DEV MODE] Sending SMS to {phone}: {token}")
        return
    
    # try:
    #     api = KavenegarAPI(settings.KAVENEGAR_API_KEY)
    #     message = f"کد تایید شما: {token}"
    #     params = {'receptor': phone, 'message': message}
    #     api.sms_send(params)
    # except Exception as e:
    #     logger.error(f"Error sending SMS: {e}")
