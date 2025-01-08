from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.hashers import check_password, make_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from .models import Category, User, TodoList


# Create your tests here.


class CategoryTestCase(TestCase):

    def test_category_correct_length_uniqueness(self):
        category = Category.objects.create(name='Category')

        try:
            category.full_clean()
        except ValidationError:
            self.fail('ValidationError raise for a valid category name.')

        with self.assertRaises(IntegrityError):
            Category.objects.create(name='Category')

    def test_category_incorrect_length(self):
        category = Category.objects.create(name='More than twenty length name')

        with self.assertRaises(ValidationError):
            category.full_clean()


class UserTestCase(TestCase):
    def test_duplicate_email(self):
        User.objects.create(email='<EMAIL>')

        with self.assertRaises(IntegrityError):
            User.objects.create(email='<EMAIL>')

    def test_email_valid(self):
        user = User.objects.create(name='<NAME>', email='<EMAIL>', password='<PASSWORD>')
        with self.assertRaises(ValidationError):
            user.full_clean()


class TodoListTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='category1')
        self.user = User.objects.create(name='<NAME>', email='example@example.com', password='<PASSWORD>')

    def test_todolist_creation(self):
        todolist = TodoList.objects.create(title='todolist1',
                                           description='todolist description',
                                           author=self.user,
                                           category=self.category)

        self.assertEqual(todolist.title, 'todolist1')


class RegisterViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('register')

    def test_successful_registration(self):
        data = {
            'name': 'test name',
            'email': 'example@example.com',
            'password': '<PASSWORD>',
        }
        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('token', response.json())
        user = User.objects.get(email=data['email'])
        self.assertEqual(user.name, data['name'])
        self.assertTrue(check_password(data['password'], user.password))

    def test_missing_fields(self):
        data = {
            'name': 'test name',
        }

        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()['error'], 'Missing required field')

    def test_invalid_email(self):
        data = {
            'name': 'test name',
            'email': 'notvalidemail.com',
            'password': '<PASSWORD>',
        }
        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'Invalid email')

    def test_duplicate_email(self):
        User.objects.create(
            name='<NAME>',
            email='example@example.com',
            password='<PASSWORD>'
        )

        duplicate_email = {
            'name': 'duplicate name',
            'email': 'example@example.com',
            'password': '<PASSWORD>',
        }

        response = self.client.post(self.url, duplicate_email, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'email already exists')

    def test_invalid_method(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json()['error'], 'Invalid HTTP method')


class LoginViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('login')
        self.user = User.objects.create(
            name='<NAME>',
            email='<EMAIL>',
            password=make_password('<PASSWORD>')
        )

    def test_correct_info(self):
        data = {
            'email': '<EMAIL>',
            'password': '<PASSWORD>'
        }
        # User.objects.create(name='<NAME>', email='example@example.com', password='<PASSWORD>')
        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json())
        self.assertEqual(response.json()['token'], str(self.user.token))

    def test_missing_password(self):
        data = {
            'email': '<EMAIL>',
        }
        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertIn('error', response.json())
        self.assertEqual(response.json()['error'], 'credential missing')

    def test_missing_email(self):
        data = {
            'password': '<PASSWORD>'
        }

        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertIn('error', response.json())
        self.assertEqual(response.json()['error'], 'credential missing')

    def test_invalid_password(self):
        data ={
            'email': '<EMAIL>',
            'password': 'NotCorrectPassword'
        }
        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertIn('error', response.json())
        self.assertEqual(response.json()['error'], 'invalid credential')

    def test_invalid_user(self):
        data = {
            'email': 'NotExistingEmail',
            'password': '<PASSWORD>'
        }
        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertIn('error', response.json())
        self.assertEqual(response.json()['error'], 'Email does not exist')

    def test_invalid_method(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json()['error'], 'Invalid HTTP method')
