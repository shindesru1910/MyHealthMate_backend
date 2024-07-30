# # user/management/commands/send_reminders.py

# from django.core.management.base import BaseCommand
# from django.utils import timezone
# from user.models import Reminder
# from user.utils import send_reminder_email
# import requests

# class Command(BaseCommand):
#     help = 'Send email reminders to users'

#     def handle(self, *args, **kwargs):
#         current_time = timezone.now().time().replace(second=0, microsecond=0)
#         reminders = Reminder.objects.filter(time=current_time)
        
#         # Fetch all user emails
#         try:
#             response = requests.get('http://127.0.0.1:8000/get-all-emails')
#             response.raise_for_status()  # Check for HTTP errors
#             user_emails = response.json().get('emails', [])
#         except requests.RequestException as e:
#             self.stdout.write(self.style.ERROR(f"Failed to fetch user emails. Error: {e}"))
#             return
        
#         for reminder in reminders:
#             # Sending emails to the specific user
#             if reminder.user.email in user_emails:
#                 send_reminder_email(
#                     reminder.user.email,
#                     reminder.title,
#                     f"Reminder: {reminder.name} at {reminder.time}"
#                 )
                
#         self.stdout.write(self.style.SUCCESS('Successfully sent reminders'))


# management/commands/send_reminders.py

from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import datetime, time as dt_time
from user.models import Reminder

class Command(BaseCommand):
    help = 'Send email reminders for scheduled exercises'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        current_time = now.time()

        # Fetch reminders that are due
        reminders = Reminder.objects.filter(time=current_time)

        for reminder in reminders:
            try:
                send_mail(
                    reminder.title,
                    f"Reminder: {reminder.name} at {reminder.time}",
                    settings.DEFAULT_FROM_EMAIL,
                    [reminder.user.email],
                    fail_silently=False,
                )
                self.stdout.write(self.style.SUCCESS(f'Email sent to {reminder.user.email}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to send email to {reminder.user.email}. Error: {e}'))


# class Command(BaseCommand):
#     help = 'Send exercise reminders to users'

#     def handle(self, *args, **kwargs):
#         now = timezone.now()
#         reminders = Reminder.objects.filter(time__hour=now.hour, time__minute=now.minute)
        
#         for reminder in reminders:
#             send_mail(
#                 subject=f"Exercise Reminder: {reminder.title}",
#                 message=f"Hi {reminder.user.first_name,'',reminder.user.last_name},\n\nIt's time for your exercise: {reminder.name}.\n\nStay fit!",
#                 from_email='myhealthmate2002@gmail.com',
#                 recipient_list=[reminder.user.email],
#                 fail_silently=False,
#             )

#         self.stdout.write(self.style.SUCCESS('Successfully sent reminders'))

