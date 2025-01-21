from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

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
        self.url = reverse('register')
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
