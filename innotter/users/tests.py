from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

User = get_user_model()


class UserBaseTests(APITestCase):

    def setUp(self):
        self.email_user = 'test@mail.com'
        self.username_user = 'tester'
        self.password_user = 'tester1234'

        self.email_admin = 'admin@mail.com'
        self.username_admin = 'admin'
        self.password_admin = 'admin1234'

        self.user = User.objects.create_user(
            username=self.username_user,
            email=self.email_user,
            password=self.password_user,
        )

        self.admin = User.objects.create_superuser(
            username=self.username_admin,
            email=self.email_admin,
            password=self.password_admin,
        )
        self.data_user = {
            'username': self.username_user,
            'password': self.password_user,
        }

        self.data_admin = {
            'username': self.username_admin,
            'password': self.password_admin,
        }

    def login(self, role='user'):
        url = reverse('users-login-user')
        client = APIClient()
        response = client.post(url, eval(f'self.data_{role}'), format='json')
        access_token = response.data.get('access_token', None)
        client.credentials(HTTP_AUTHORIZATION='Token ' + access_token)
        self.client = client
        return response


class UserTests(UserBaseTests):
    
    def setUp(self):
        super().setUp()

    def test_register_user(self):
        url = reverse('users-register')
        client = APIClient()
        response = client.post(url, {'username': 'user', 'email': 'email@mail.com', 'password': 'user1234'},
                               format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.count() == 3)

    def test_login_user(self):
        response = super().login()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data.get('access_token'), None)
        self.assertEqual(response.data['user']['username'], self.username_user)

    def test_refresh_token(self):
        super().login()
        url = reverse('users-refresh-token')
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data['access_token'])

    def test_user_list(self):
        super().login()
        url = reverse('users-list')
        response = self.client.get(url)
        self.assertEqual(len(response.data), User.objects.filter().count())

    def test_user_detail(self):
        super().login()
        url = reverse('users-detail', args=(self.user.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_admin_user_patch(self):
        self.test_login_user()
        url = reverse('users-detail', args=(self.user.pk,))
        response = self.client.patch(url, {'role': 'admin'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_user_patch(self):
        super().login(role='admin')
        url = reverse('users-detail', args=(self.user.pk,))
        response = self.client.patch(url, {'role': 'admin'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['role'], 'admin')

    def test_admin_delete_user(self):
        super().login(role='admin')
        url = reverse('users-detail', args=(self.user.pk,))
        user_amount = User.objects.count()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), user_amount-1)

    def test_not_admin_delete_user(self):
        super().login(role='user')
        url = reverse('users-detail', args=(self.user.pk,))
        user_amount = User.objects.count()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(User.objects.count(), user_amount)
