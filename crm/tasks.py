from celery import shared_task
from .models import Reminder
from django.utils.timezone import now
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils import timezone
from .models import Lead

@shared_task
def send_manual_reminder(reminder_id):
    try:
        reminder = Reminder.objects.get(id=reminder_id)

        # Create the email message
        email = EmailMessage(
            subject='Manual Reminder Notification',
            body=reminder.message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[reminder.lead.email],
        )

        # Send the email
        email.send()

        print(f"Manual reminder sent to {reminder.lead.email}")

    except Reminder.DoesNotExist:
        print(f"Reminder with ID {reminder_id} does not exist")
    except Exception as e:
        print(f"Failed to send manual reminder: {e}")

@shared_task
def send_reminder_to_all_active_leads():
    active_leads = Lead.objects.filter(status='Active')
    sent_reminders = []

    for lead in active_leads:
        if not lead.email: 
            continue

        # Create a reminder message
        message = f"Hello {lead.name}, this is your scheduled reminder."

        # Send the email reminder
        try:
            email = EmailMessage(
                subject='Scheduled Reminder',
                body=message,
                to=[lead.email],
            )
            email.send()
            print(f"Successfully sent reminder email to {lead.email}")

            # Create a record in the Reminder model
            Reminder.objects.create(
                lead=lead,
                user=lead.user,
                message=message,
                remind_at=timezone.now(),
            )
            sent_reminders.append(f"Sent reminder to {lead.name} at {timezone.now()}")

        except Exception as e:
            print(f"Failed to send email to {lead.email}: {e}")

    return sent_reminders