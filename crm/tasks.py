from celery import shared_task
from .models import Reminder
from django.utils.timezone import now
from django.core.mail import send_mail

@shared_task
def send_reminder():
    reminders = Reminder.objects.filter(remind_at__lte=now())
    for reminder in reminders:
        send_mail(
            'Reminder Notification',
            reminder.message,
            'from@example.com',
            [reminder.lead.email],
        )
        reminder.delete()