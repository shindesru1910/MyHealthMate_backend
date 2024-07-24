# # user/utils.py utility function to send reminders

# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from django.conf import settings
# from django.core.mail import send_mail
# import requests

# def send_reminder_email(to_email, subject, body):
#     """
#     Sends an email to the specified recipient with the given subject and body.

#     Args:
#         to_email (str): Recipient's email address.
#         subject (str): Subject of the email.
#         body (str): Body of the email.

#     Returns:
#         None
#     """
#     msg = MIMEMultipart()
#     msg['From'] = settings.DEFAULT_FROM_EMAIL
#     msg['To'] = to_email
#     msg['Subject'] = subject

#     msg.attach(MIMEText(body, 'plain'))

#     try:
#         with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
#             server.starttls()
#             server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
#             server.send_message(msg)
#         print(f"Email sent to {to_email}")
#     except Exception as e:
#         print(f"Failed to send email to {to_email}. Error: {e}")


# user/utils.py
# from django.core.mail import send_mail

# def send_reminder_email(to_email, subject, message):
#     send_mail(
#         subject,
#         message,
#         'myhealthmate2002@gmail.com',
#         [to_email],
#         fail_silently=False,
#     )

# user/utils.py

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.conf import settings

def send_reminder_email(to_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = settings.DEFAULT_FROM_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            server.starttls()
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.send_message(msg)
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}. Error: {e}")

