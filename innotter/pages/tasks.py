from celery import shared_task


@shared_task
def notify_followers(post_owner, followers: list):
    pass
