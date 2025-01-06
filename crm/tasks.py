from celery import shared_task
from django.core.mail import EmailMessage
from django.utils import timezone
from .models import Reminder
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

@shared_task
def check_pending_reminders():
    """
    Celery task to check for pending reminders and send reminder emails.
    """
    try:
        # Get all pending reminders where remind_at time has passed
        pending_reminders = Reminder.objects.filter(
            status='Pending',
            remind_at__lte=timezone.now()
        ).select_related('lead')

        if not pending_reminders.exists():
            logger.info("No pending reminders found.")
            return

        for reminder in pending_reminders:
            if not reminder.lead.email:
                logger.warning(f"Skipping reminder for lead {reminder.lead.name} (ID: {reminder.lead.id}) as no email is provided.")
                continue

            # Email details
            subject = f"Reminder: Task for {reminder.lead.name}"
            message = f"""
            Dear {reminder.lead.name},

            This is a reminder about your task:
            {reminder.message}

            Lead: {reminder.lead.name}
            Due time: {reminder.remind_at}

            Best regards,
            Your Application Team
            """

            try:
                email = EmailMessage(
                    subject=subject,
                    body=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[reminder.lead.email],
                )
                email.send()
                logger.info(f"Successfully sent reminder email to {reminder.lead.email}")

                # Update reminder status
                reminder.status = 'Complete'
                reminder.save()

            except Exception as e:
                logger.error(f"Failed to send reminder email to {reminder.lead.email}: {str(e)}")

    except Exception as e:
        logger.critical(f"Critical error in check_pending_reminders task: {str(e)}")
