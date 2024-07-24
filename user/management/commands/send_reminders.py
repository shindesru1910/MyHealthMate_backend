# user/management/commands/send_reminders.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from user.models import Reminder
from user.utils import send_reminder_email
import requests

class Command(BaseCommand):
    help = 'Send email reminders to users'

    def handle(self, *args, **kwargs):
        current_time = timezone.now().time().replace(second=0, microsecond=0)
        reminders = Reminder.objects.filter(time=current_time)
        
        # Fetch all user emails
        try:
            response = requests.get('http://127.0.0.1:8000/get-all-emails')
            response.raise_for_status()  # Check for HTTP errors
            user_emails = response.json().get('emails', [])
        except requests.RequestException as e:
            self.stdout.write(self.style.ERROR(f"Failed to fetch user emails. Error: {e}"))
            return
        
        for reminder in reminders:
            # Sending emails to the specific user
            if reminder.user.email in user_emails:
                send_reminder_email(
                    reminder.user.email,
                    reminder.title,
                    f"Reminder: {reminder.name} at {reminder.time}"
                )
                
        self.stdout.write(self.style.SUCCESS('Successfully sent reminders'))
