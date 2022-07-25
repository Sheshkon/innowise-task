from celery import shared_task
from innotter.aws_services import send_email


@shared_task
def notify_followers(post_owner, followers_emails: list):
    response = send_email(post_owner, followers_emails)
    return response
