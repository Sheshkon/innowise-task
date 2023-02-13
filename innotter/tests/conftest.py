from io import BytesIO
from PIL import Image

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

from dataclasses import dataclass

from pages.models import Tag, Post, Page, Like


@dataclass
class Tester:
    first_name: str
    last_name: str
    username: str
    email: str
    password: str


User = get_user_model()

_user = Tester(
    first_name='tester',
    last_name='tester',
    username='user',
    email='user@mail.com',
    password='user1234'
)

_admin = Tester(
    first_name='tester',
    last_name='tester',
    username='admin',
    email='admin@mail.com',
    password='admin1234'
)


@pytest.fixture
def user():
    return User.objects.create_user(
        first_name=_user.first_name,
        last_name=_user.last_name,
        username=_user.username,
        email=_user.email,
        password=_user.password
    )


@pytest.fixture
def admin():
    return User.objects.create_superuser(
        first_name=_admin.first_name,
        last_name=_admin.last_name,
        username=_admin.username,
        email=_admin.email,
        password=_admin.password
    )


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def auth_user_client(client, user):
    url = reverse('users-login-user')
    response = client.post(url, dict(username=_user.username, email=_user.email, password=_user.password))
    access_token = response.data.get('access_token', None)
    client.credentials(HTTP_AUTHORIZATION='Token ' + access_token)
    return client


@pytest.fixture
def auth_admin_client(client, admin):
    url = reverse('users-login-user')
    response = client.post(url, dict(username=_admin.username, email=_admin.email, password=_admin.password))
    access_token = response.data.get('access_token', None)
    client.credentials(HTTP_AUTHORIZATION='Token ' + access_token)
    return client


@pytest.fixture
def user_page(user):
    return Page.objects.create(
        name='user_page',
        uuid='user_tester',
        description='admin user page description',
        owner=user,
        is_private=False,
    )


@pytest.fixture
def admin_page(admin):
    return Page.objects.create(
        name='admin_page',
        uuid='admin_tester',
        description='admin user page description',
        owner=admin,
        is_private=False,
    )


@pytest.fixture
def user_page_with_follower(user_page, admin):
    user_page.followers.add(admin)
    user_page.save()
    return user_page


@pytest.fixture
def admin_page_with_follower(admin_page, user):
    admin_page.followers.add(user)
    admin_page.save()
    return admin_page


@pytest.fixture
def private_user_page(user_page):
    user_page.is_private = True
    user_page.save()
    return user_page


@pytest.fixture
def private_admin_page(admin_page):
    admin_page.is_private = True
    admin_page.save()
    return admin_page


@pytest.fixture
def user_private_page_with_follow_request(private_user_page, admin):
    private_user_page.follow_requests.add(admin)
    private_user_page.save()
    return private_user_page


@pytest.fixture
def admin_private_page_with_follow_request(private_admin_page, user):
    private_admin_page.follow_requests.add(user)
    private_admin_page.save()
    return private_admin_page


@pytest.fixture
def tags_list():
    tags = []
    for i in range(5):
        tags.append(Tag.objects.create(name=str(i)))
    return tags


@pytest.fixture
def user_page_with_tags(user_page, tags_list):
    user_page.tags.add(*Tag.objects.all())
    return user_page


@pytest.fixture
def user_post(user, user_page):
    return Post.objects.create(
        page=user_page,
        content='test user post content'
    )


@pytest.fixture
def admin_post(user, admin_page):
    return Post.objects.create(
        page=admin_page,
        content='test admin post content'
    )


@pytest.fixture
def likes(user, admin, user_post):
    return (Like.objects.create(owner=user, post=user_post),
            Like.objects.create(owner=admin, post=user_post))


@pytest.fixture
def image():
    file = BytesIO()
    image = Image.new('RGBA', size=(1, 1), color=(155, 0, 0))
    image.save(file, 'png')
    file.name = 'test.png'
    file.seek(0)
    return file
