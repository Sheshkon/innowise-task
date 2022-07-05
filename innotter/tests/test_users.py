import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from users import serializers

User = get_user_model()


@pytest.mark.django_db
def test_register_user(client):
    payload = dict(
        first_name='good',
        last_name='guy',
        email='user@mail.com',
        username='someone',
        password='someone1234'

    )
    url = reverse('users-register')
    response = client.post(url, payload)
    expected_data = serializers.RegistrationSerializer(payload).data
    data = response.data

    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.count() == 1
    assert data == expected_data


@pytest.mark.django_db
def test_login_user(client, user):
    url = reverse('users-login-user')
    response = client.post(url, dict(username='user', email='user@mail.com', password='user1234'))

    assert response.status_code == status.HTTP_200_OK
    assert response.data.get('access_token') is not None


@pytest.mark.django_db
def test_refresh_token(auth_user_client):
    url = reverse('users-refresh-token')
    response = auth_user_client.post(url, {}, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert response.data['access_token'] is not None


@pytest.mark.django_db
def test_anonymous_user_list(client):
    url = reverse('users-list')
    response = client.get(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_user_list(auth_user_client, user):
    url = reverse('users-list')
    response = auth_user_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == User.objects.count()


@pytest.mark.django_db
def test_user_detail(auth_user_client, user):
    url = reverse('users-detail', args=(user.pk,))
    response = auth_user_client.get(url)
    expected_data = serializers.RetrieveUserSerializer(user).data

    assert response.data == expected_data
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_not_admin_user_patch(user, auth_user_client):
    url = reverse('users-detail', args=(user.pk,))
    response = auth_user_client.patch(url, {'role': 'admin'}, format='json')

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_admin_user_patch(user, auth_admin_client):
    url = reverse('users-detail', args=(user.pk,))
    response = auth_admin_client.patch(url, {'role': 'admin'}, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert response.data['role'] == 'admin'
    assert response.data['username'] == 'user'


@pytest.mark.django_db
def test_admin_delete_user(user, auth_admin_client):
    url = reverse('users-detail', args=(user.pk,))
    user_amount = User.objects.count()
    response = auth_admin_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert User.objects.count() == user_amount - 1


@pytest.mark.django_db
def test_not_admin_delete_user(user, auth_user_client):
    url = reverse('users-detail', args=(user.pk,))
    user_amount = User.objects.count()
    response = auth_user_client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert User.objects.count(), user_amount


@pytest.mark.django_db
def test_admin_create_user(auth_admin_client):
    payload = dict(
        first_name='bot',
        last_name='bot',
        email='bot@mail.com',
        username='bot',
        password='bot12345',
        title='bot'
    )
    url = reverse('users-list')
    response = auth_admin_client.post(url, payload)

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_not_admin_create_user(auth_user_client):
    payload = dict(
        first_name='bot',
        last_name='bot',
        email='bot@mail.com',
        username='bot',
        password='bot12345',
        title='bot'
    )
    url = reverse('users-list')
    response = auth_user_client.post(url, payload)

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_admin_update_user(user, auth_admin_client):
    payload = dict(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        username='new_username',
        role=user.role
    )
    url = reverse('users-detail', args=(user.pk,))
    prev_username = user.username
    response = auth_admin_client.put(url, payload)

    assert response.status_code == status.HTTP_200_OK
    assert response.data.get('username') != prev_username


@pytest.mark.django_db
def test_not_admin_update_user(user, auth_user_client):
    payload = dict(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        username='new_username',
        role=user.role
    )
    url = reverse('users-detail', args=(user.pk,))
    response = auth_user_client.put(url, payload)

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_not_admin_block_user(user, auth_user_client):
    url = reverse('users-block', args=(user.pk,))
    response = auth_user_client.patch(url, {})

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_admin_block_user(user, auth_admin_client):
    url = reverse('users-block', args=(user.pk,))
    response = auth_admin_client.patch(url, {})

    assert response.status_code == status.HTTP_200_OK
    blocked_user = User.objects.filter(pk=user.pk).first()
    assert blocked_user.is_blocked is True
