from django.contrib.auth import get_user_model

from celery import shared_task
from innotter.publisher import publish
from innotter.aws_services import send_email
from innotter.services import get_stats

User = get_user_model()


@shared_task
def notify_followers(post_owner, followers_emails: list):
    response = send_email(post_owner, followers_emails)
    return response


@shared_task
def send_stats():
    users = User.objects.all()
    for user in users:
        publish(body=get_stats(user))
