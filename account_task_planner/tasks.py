from celery import shared_task
from django.core.mail import send_mail
from account_task_planner.models import CustomUser

@shared_task
def send_daily_notification():
    users = CustomUser.objects.all()
    for user in users:
        subject = 'Daily Notification'
        message = 'Hello {0}, this is your daily notification.'.format(user.username)
        from_email = 'noreply@example.com'
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list)
