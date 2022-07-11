from datetime import datetime, timedelta
from django.contrib.auth import get_user_model

from innotter.settings import BLOCK_DAYS
from pages.models import Like, Post, Page, Tag

User = get_user_model()


def is_not_blocked(unblock_date):
    return not unblock_date or unblock_date < datetime.now()


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

    if not reply_to or is_not_blocked(reply_to.page.unblock_date):
        Post.objects.create(page=page, content=content, reply_to=reply_to)
    else:
        Post.objects.create(page=page, content=content)


def _is_followed_page(page: Page, follower: User) -> bool:
    if page.owner == follower:
        return False
    if page.is_private:
        return False

    return is_not_blocked(page.unblock_date) and not page.is_permanent_blocked


def add_follower(page_to_follow: Page, follower: User) -> bool:
    if _is_followed_page(page_to_follow, follower):
        page_to_follow.followers.add(follower)
        return True

    return False


def delete_follower(followed_page: Page, follower: User) -> bool:
    if follower in followed_page.followers.all():
        followed_page.followers.remove(follower)
        return True

    return False


def add_follow_request(page_to_follow: Page, follower: User) -> bool:
    if not _is_followed_page(page_to_follow, follower):
        page_to_follow.follow_requests.add(follower)
        return True

    return False


def delete_follow_request(followed_page: Page, follower: User) -> bool:
    if follower in followed_page.follow_requests.all():
        followed_page.follow_requests.remove(follower)
        return True

    return False


def _accept_request(page: Page, user: User):
    page.followers.add(user)
    delete_follow_request(page, user)


def accept_follow_request(page: Page, one=False, user_id=None):
    if not one:
        for request in page.follow_requests.all():
            _accept_request(page=page, user=request)
    else:
        user = User.objects.filter(id=user_id).first()
        if user:
            _accept_request(page=page, user=user)

    page.save()


def reject_follow_request(page: Page, one=False, user_id=None):
    if not one:
        for request in page.follow_requests.all():
            delete_follow_request(followed_page=page, follower=request)
    else:
        user = User.objects.filter(id=user_id).first()
        if user:
            delete_follow_request(followed_page=page, follower=user)
    page.save()


def add_tags_to_page(page: Page, tags_names: set) -> None:
    page.tags.add(*Tag.objects.filter(name__in=tags_names))


def delete_tags_from_page(page: Page, tags_names: set) -> None:
    page.tags.remove(*Tag.objects.filter(name__in=tags_names))

