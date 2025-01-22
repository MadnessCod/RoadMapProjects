from django.test import TestCase
from django.contrib.auth.models import User

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Expense


# Create your tests here.

class ExpenseTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='<NAME>',
            email='<EMAIL>',
            password='<PASSWORD>'
        )

    def test_create_expense(self):
        expense = Expense.objects.create(
            name='<NAME>',
            description='<DESCRIPTION>',
            amount=10,
            category='UTILITIES',
            user=self.user,
        )

        self.assertEqual(Expense.objects.all().count(), 1)
        self.assertEqual(expense.name, '<NAME>')
        self.assertEqual(expense.description, '<DESCRIPTION>')
        self.assertEqual(expense.amount, 10)
        self.assertEqual(expense.category, 'UTILITIES')
        self.assertEqual(expense.user.username, self.user.username)


class RegisterViewTestCase(APITestCase):
    def setUp(self):
        self.register_url = '/register/'
        self.valid_payload = {
            'username': 'USERNAME',
            'email': 'example@example.com',
            'password': '<PASSWORD>',
        }

        self.invalid_payload = {
            'username': '',
            'email': 'invalid email',
            'password': '',
        }

    def test_successful_registration(self):
        response = self.client.post(self.register_url, data=self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_unsuccessful_registration(self):
        response = self.client.post(self.register_url, data=self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
        self.assertIn('email', response.data)
        self.assertIn('password', response.data)

    def test_duplicate_username(self):
        User.objects.create(
            username='USERNAME',
            email='<EMAIL>',
            password='<PASSWORD>'
        )

        data = {
            'username': 'USERNAME',
            'email': 'different@email.com',
            'password': '<PASSWORD>',
        }
        response = self.client.post(self.register_url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)

    def test_duplicate_email(self):
        User.objects.create(
            username='USERNAME',
            email='example@example.com',
            password='<PASSWORD>'
        )

        data = {
            'username': 'DifferentUsername',
            'email': 'example@example.com',
            'password': '<PASSWORD>',
        }

        response = self.client.post(self.register_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)


class LoginViewTestCase(APITestCase):
    def setUp(self):
        self.login_url = '/login/'
        self.user = User.objects.create_user(
            username='USERNAME',
            email='example@example.com',
            password='<PASSWORD>'
        )
        self.valid_payload = {
            'username': 'USERNAME',
            'password': '<PASSWORD>',
        }
        self.invalid_payload = {
            'username': 'USERNAME',
            'password': 'wrong password'
        }

    def test_successful_login(self):
        response = self.client.post(self.login_url, data=self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_unsuccessful_login(self):
        response = self.client.post(self.login_url, data=self.invalid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertIn(response.data['detail'], 'No active account found with the given credentials')

    def test_unregistered_user(self):
        data = {
            'username': 'UnregisteredUsername',
            'password': 'WrongPassword'
        }

        response = self.client.post(self.login_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertIn(response.data['detail'], 'No active account found with the given credentials')


class ExpenseViewTestCase(APITestCase):
    def setUp(self):
        self.expense_url = '/expenses/'
        self.user = User.objects.create_user(
            username='<USERNAME>',
            email='example@example.com',
            password='<PASSWORD>'
        )
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.valid_payload = {
            'name': '<NAME>',
            'description': '<DESCRIPTION>',
            'amount': 10.0,
            'category': 'UTILITIES',
        }

    def authenticate_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

    def test_successful_post_expense(self):
        self.authenticate_user()
        response = self.client.post(self.expense_url, data=self.valid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], self.valid_payload['name'])
        self.assertEqual(response.data['description'], self.valid_payload['description'])
        self.assertEqual(response.data['amount'], self.valid_payload['amount'])
