# # user/tasks.py
import logging
from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.conf import settings

# logger=logging.getLogger(__name__)

# @shared_task(bind=True)
# def send_mail_func(self):
#     logger.info("send_mail_func started")
#     users = get_user_model().objects.all()
#     for user in users:
#         # mail_subject = 'Health-Mate Exercise Reminder'
#         mail_subject = 'Testing Exercise Reminder'
#         message = 'hii! Testing.'
#         # message = 'TIME TO STAY HEALTHY ! This is your daily reminder to complete your exercise routine!'
#         to_email = user.email
#         # to_email = 'shaguftasaiyed25@gmail.com'
#         logger.info(f"Sending email to {to_email}")
#         send_mail(
#             subject = mail_subject,
#             message = message,
#             from_email = settings.DEFAULT_FROM_EMAIL,
#             recipient_list = [to_email],
#             #if TRUE no mail, when FALSE mail. 
#             fail_silently = False 
#         )
#         logger.info("send_mail_func completed")
#         return "Done"



logger = logging.getLogger(__name__)

@shared_task(bind=True)
def send_mail_func(self):
    logger.info("send_mail_func started")
    users = get_user_model().objects.all()
    for user in users:
        mail_subject = 'Testing Exercise Reminder'
        message = 'hii! Testing.'
        to_email = user.email
        
        logger.info(f"Attempting to send email to {to_email}")
        try:
            send_mail(
                subject=mail_subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[to_email],
                fail_silently=False
            )
            logger.info(f"Email successfully sent to {to_email}")
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {e}")
    logger.info("send_mail_func completed")
    return "Done"




