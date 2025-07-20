# listings/tasks.py
from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_booking_confirmation_email(email, full_name, destination):
    subject = 'Booking Confirmation'
    message = (
        f"Hello {full_name},\n\n"
        f"Your booking to {destination} is confirmed.\n\n"
        f"Thank you for choosing our service!"
    )
    from_email = None  # uses DEFAULT_FROM_EMAIL
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)
