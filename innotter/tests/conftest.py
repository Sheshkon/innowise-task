import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

from dataclasses import dataclass


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
