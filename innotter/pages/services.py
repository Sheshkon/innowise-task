from datetime import datetime, timedelta
from innotter.settings import BLOCK_DAYS
from .models import Page, Like, Post
from users.models import User


def is_not_blocked(unblock_date):
    not unblock_date or unblock_date < datetime.now()


def block_page(page: Page, is_to_permanent=False):
    if is_to_permanent:
        page.is_permanent_blocked = True
    else:
        page.unblock_date = datetime.now() + timedelta(days=BLOCK_DAYS)

    page.save()

    return page


def create_like(user: User, post: Post):
    if not Like.objects.filter(owner=user, post__id=post.id).exists() and \
            not post.page.is_permanent_blocked and is_not_blocked(post.page.unblock_date):
        Like.objects.create(owner=user, post=post)


def create_post(user: User, serialized_post):
    reply_to = serialized_post.get('reply_to')
    page = serialized_post.get('page')
    content = serialized_post.get('content')

    if not page and page.owner != user and is_not_blocked(page.unblock_date):
        return

    if not reply_to and is_not_blocked(reply_to.page.unblock_date):
        Post.objects.create(page=page, content=content, reply_to=reply_to)
    else:
        Post.objects.create(page=page, content=content)

