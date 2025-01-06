from celery import shared_task
from .models import Reminder
from django.utils.timezone import now
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils import timezone
from .models import Lead


@shared_task
def check_pending_reminders():
    # Get all pending reminders where remind_at time has passed
    pending_reminders = Reminder.objects.filter(
        status='Pending',
        remind_at__lte=timezone.now()
    ).select_related('lead')
    
    for reminder in pending_reminders:
        # Send email
        subject = f'Reminder: Task for {reminder.lead.name}'
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
                to=[reminder.lead.email],
            )
            email.send()
            print(f"Successfully sent reminder email to {reminder.lead.email}")
            
            # Update reminder status
            reminder.status = 'Complete'
            reminder.save()
            
        except Exception as e:
            print(f"Failed to send reminder email: {str(e)}")