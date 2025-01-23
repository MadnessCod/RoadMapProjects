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
        self.invalid_payload = {
            'name': '<NAME>',
            'description': '',
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

    def test_unsuccessful_post_expense(self):
        self.authenticate_user()
        response = self.client.post(self.expense_url, data=self.invalid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('description', response.data)
        self.assertIn('amount', response.data)

    def test_unauthorized_post_expense(self):
        response = self.client.post(self.expense_url, data=self.valid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertIn(response.data['detail'], 'Authentication credentials were not provided.')

    def test_get_expense(self):
        self.authenticate_user()
        self.client.post(self.expense_url, data=self.valid_payload, format='json')
        response = self.client.get(self.expense_url)

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.valid_payload['name'])
        self.assertEqual(response.data[0]['description'], self.valid_payload['description'])
        self.assertEqual(response.data[0]['amount'], self.valid_payload['amount'])
        self.assertEqual(response.data[0]['category'], self.valid_payload['category'])

    def test_unauthorized_get_expense(self):
        response = self.client.get(self.expense_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)


class ExpenseUpdateViewTestCase(APITestCase):
    def setUp(self):
        self.expense_url = '/expenses/1/update'
        user = User.objects.create_user(
            username='USERNAME',
            email='example@example.com',
            password='<PASSWORD>'
        )
        refresh = RefreshToken.for_user(user)
        self.access_token = str(refresh.access_token)

        Expense.objects.create(
            name='<NAME>',
            description='<DESCRIPTION>',
            amount=10.0,
            category='UTILITIES',
            user=user
        )

    def authenticate(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

    def test_successful_update(self):
        self.authenticate()

        data = {
            'name': 'ChangedName',
            'description': '<DESCRIPTION>',
            'amount': 15.0,
            'category': 'ELECTRONICS',
        }

        response = self.client.put(self.expense_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['amount'], data['amount'])
        self.assertEqual(response.data['category'], data['category'])

    def test_unsuccessful_update(self):
        self.authenticate()
        data = {
            'name': 'ChangedName',
        }
        response = self.client.put(self.expense_url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('description', response.data)
        self.assertIn('amount', response.data)

    def test_unauthorized_update(self):
        response = self.client.put(self.expense_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)

    def test_partial_update(self):
        self.authenticate()

        data = {
            'name': 'ChangedName',
        }
        expense = Expense.objects.get(pk=1)

        response = self.client.patch(self.expense_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['description'], expense.description)
        self.assertEqual(response.data['amount'], expense.amount)
        self.assertEqual(response.data['category'], expense.category)

    def test_invalid_pk(self):
        url = '/expenses/2/update/'
        self.authenticate()

        data = {
            'name': 'ChangedName',
        }

        response = self.client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('detail', response.data)

class ExpenseDeleteViewTestCase(APITestCase):
    def setUp(self):
        self.expense_url = '/expenses/1/delete/'
        user = User.objects.create_user(
            username='USERNAME',
            email='example@example.com',
            password='<PASSWORD>'
        )
        refresh = RefreshToken.for_user(user)
        self.access_token = str(refresh.access_token)
        Expense.objects.create(
            name='<NAME>',
            description='<DESCRIPTION>',
            amount=10.0,
            category='ELECTRONICS',
            user=user,
        )

    def authenticate(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

    def test_successful_delete(self):
        self.authenticate()

        response = self.client.delete(self.expense_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthorized_delete(self):
        response = self.client.delete(self.expense_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)

    def test_invalid_pk(self):
        url = '/expenses/2/delete/'

        self.authenticate()
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('detail', response.data)
