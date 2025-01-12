import uuid

from datetime import datetime, timedelta

from django.test import TestCase, Client
from django.utils.timezone import now
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
            password=make_password('<PASSWORD>'),
        )

    def test_correct_info(self):
        data = {
            'email': '<EMAIL>',
            'password': '<PASSWORD>'
        }

        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json())
        self.assertEqual(response.json()['token'], str(self.user.token))

    def test_refresh_token(self):
        user = User.objects.create(
            name='<NAME>',
            email='<EMAIL2>',
            password=make_password('<PASSWORD>'),
            last_token_refresh=now() - timedelta(days=31)
        )

        data = {
            'email': '<EMAIL2>',
            'password': '<PASSWORD>',
        }

        old_token = user.token
        response = self.client.post(self.url, data, content_type='application/json')

        user.refresh_from_db()
        new_token = response.json()['token']

        self.assertEqual(str(user.token), new_token)
        self.assertIn('token', response.json())
        self.assertNotEqual(old_token, new_token)
        self.assertEqual(response.status_code, 200)

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
        data = {
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


class AddTodoTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('add')
        self.user = User.objects.create(
            name='<NAME>',
            email='example@example.com',
            password=make_password('<PASSWORD>'))
        self.headers = {'Authorization': f'{self.user.token}'}

    def test_add_todo(self):
        data = {
            'title': 'todolist1',
            'description': 'todolist description',
            'category': 'category1'
        }
        response = self.client.post(self.url, data, content_type='application/json', headers=self.headers)
        todolist1 = TodoList.objects.get(title='todolist1')

        self.assertEqual(todolist1.title, 'todolist1')
        self.assertEqual(todolist1.description, 'todolist description')
        self.assertEqual(todolist1.category.name, 'category1')

        self.assertEqual(response.status_code, 201)
        self.assertIn(response.json()['title'], todolist1.title)
        self.assertIn(response.json()['description'], todolist1.description)
        self.assertEqual(response.json()['category'], 'category1')

    def test_missing_token(self):
        response = self.client.post(self.url, content_type='application/json')

        self.assertEqual(response.status_code, 401)
        self.assertIn('error', response.json())
        self.assertEqual(response.json()['error'], 'Token missing')

    def test_invalid_token(self):
        headers = {'Authorization': f'{uuid.uuid4()}'}

        response = self.client.post(self.url, content_type='application/json', headers=headers)
        self.assertEqual(response.status_code, 401)
        self.assertIn('error', response.json())
        self.assertEqual(response.json()['error'], 'Invalid token')

    def test_missing_fields(self):
        data = {
            'title': 'todolist title',
            'description': 'todolist description',
        }
        data2 = {
            'description': 'todolist description',
            'category': 'category'
        }
        data3 = {
            'title': 'todolist title',
            'category': 'category'
        }

        response = self.client.post(self.url, data, content_type='application/json', headers=self.headers)
        response2 = self.client.post(self.url, data2, content_type='application/json', headers=self.headers)
        response3 = self.client.post(self.url, data3, content_type='application/json', headers=self.headers)

        self.assertEqual(response.status_code, 401)
        self.assertIn('error', response.json())
        self.assertEqual(response.json()['error'], 'Missing required field')

        self.assertEqual(response2.status_code, 401)
        self.assertIn('error', response2.json())
        self.assertEqual(response2.json()['error'], 'Missing required field')

        self.assertEqual(response3.status_code, 401)
        self.assertIn('error', response3.json())
        self.assertEqual(response3.json()['error'], 'Missing required field')

    def test_category_length(self):
        data = {
            'title': 'todolist title',
            'description': 'todolist description',
            'category': 'More than twenty length category'
        }
        response = self.client.post(self.url, data, content_type='application/json', headers=self.headers)

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())
        self.assertEqual(response.json()['error'], 'category length exceeds 20 characters')


class GetTodoTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('add')

        self.user = User.objects.create(
            name='<NAME>',
            email='example@example.com',
            password=make_password('<PASSWORD>'))
        self.headers = {'Authorization': f'{self.user.token}'}

        self.data = [{
            'title': 'todolist1',
            'description': 'todolist description',
            'category': 'test'
        },
            {
                'title': 'todolist2',
                'description': 'todolist description',
                'category': 'category'
            },
            {
                'title': 'todolist3',
                'description': 'todolist description',
                'category': 'test category'
            }]

        for data in self.data:
            category = Category.objects.create(name=data['category'])
            TodoList.objects.create(
                title=data['title'],
                description=data['description'],
                category=category,
                author=self.user,
            )

    def test_get_todo(self):
        response = self.client.get(self.url, content_type='application/json', headers=self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(TodoList.objects.count(), len(response.json()['data']))
        self.assertEqual(response.json()['page'], 1)
        self.assertEqual(response.json()['limit'], 10)
        self.assertEqual(response.json()['total'], TodoList.objects.count())

    def test_get_missing_token(self):
        response = self.client.get(self.url, content_type='application/json')

        self.assertEqual(response.status_code, 401)
        self.assertIn('error', response.json())
        self.assertEqual(response.json()['error'], 'Token missing')

    def test_wrong_token(self):
        headers = {'Authorization': f'{uuid.uuid4()}'}
        response = self.client.get(self.url, content_type='application/json', headers=headers)

        self.assertEqual(response.status_code, 401)
        self.assertIn('error', response.json())
        self.assertEqual(response.json()['error'], 'Invalid token')

    def test_get_with_date(self):
        url = (f'{self.url}?start{(datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")}'
               f'?end={(datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")}')
        response = self.client.get(url, content_type='application/json', headers=self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['data']), TodoList.objects.count())
        self.assertEqual(response.json()['page'], 1)
        self.assertEqual(response.json()['limit'], 10)
        self.assertEqual(response.json()['total'], TodoList.objects.count())

    def test_with_smaller_end_date(self):
        url = f'{self.url}?end={(datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")}'

        response = self.client.get(url, content_type='application/json', headers=self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['data']), 0)
        self.assertEqual(response.json()['page'], 1)
        self.assertEqual(response.json()['limit'], 10)
        self.assertEqual(response.json()['total'], 0)

    def test_with_bigger_start_date(self):
        url = f'{self.url}?start={(datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")}'

        response2 = self.client.get(url, content_type='application/json', headers=self.headers)

        self.assertEqual(response2.status_code, 200)
        self.assertEqual(len(response2.json()['data']), 0)
        self.assertEqual(response2.json()['page'], 1)
        self.assertEqual(response2.json()['limit'], 10)
        self.assertEqual(response2.json()['total'], 0)

    def test_get_wrong_date(self):
        url = f'{self.url}?start=11-2020-01'
        response = self.client.get(url, content_type='application/json', headers=self.headers)

        self.assertEqual(response.status_code, 401)
        self.assertIn('error', response.json())
        self.assertEqual(response.json()['error'], 'invalid date')

    def test_big_page_number(self):
        url = f'{self.url}?page=10'

        response = self.client.get(url, content_type='application/json', headers=self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['data']), 0)
        self.assertEqual(response.json()['page'], 1)
        self.assertEqual(response.json()['limit'], 10)
        self.assertEqual(response.json()['total'], 0)

    def test_small_page_number(self):
        url = f'{self.url}?page=0'

        response = self.client.get(url, content_type='application/json', headers=self.headers)

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())
        self.assertEqual(response.json()['error'], 'Invalid number for page or limit')

    def test_with_category(self):
        url = f'{self.url}?category=test'

        response = self.client.get(url, content_type='application/json', headers=self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['data']), 1)
        self.assertEqual(response.json()['page'], 1)
        self.assertEqual(response.json()['limit'], 10)
        self.assertEqual(response.json()['total'], 1)

    def test_with_invalid_category(self):
        url = f'{self.url}?category=NoSuchCategory'

        response = self.client.get(url, content_type='application/json', headers=self.headers)

        self.assertEqual(response.status_code, 401)
        self.assertIn('error', response.json())
        self.assertEqual(response.json()['error'], 'Category does not exist')

    def test_invalid_method(self):
        response = self.client.put(self.url, content_type='application/json', headers=self.headers)

        self.assertEqual(response.status_code, 405)
        self.assertIn('error', response.json())
        self.assertEqual(response.json()['error'], 'Invalid HTTP method')


class UpdateTodoTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create(
            name='<NAME>',
            email='example@example.com',
            password=make_password('<PASSWORD>'))

        self.headers = {'Authorization': f'{self.user.token}'}

        self.data = [
            {
                'title': 'todolist1',
                'description': 'todolist description',
                'category': 'test'
            },
            {
                'title': 'todolist2',
                'description': 'todolist description',
                'category': 'category'
            },
            {
                'title': 'todolist3',
                'description': 'todolist description',
                'category': 'test category'
            }]

        for data in self.data:
            category = Category.objects.create(name=data['category'])
            TodoList.objects.create(
                title=data['title'],
                description=data['description'],
                category=category,
                author=self.user,
            )

    def test_update_with_correct_data(self):
        url = reverse('update', args=[1])

        data = {
            'title': 'updated title',
            'description': 'updated description',
            'category': 'updated category'
        }
        todo = TodoList.objects.get(id=1)
        self.assertEqual(todo.title, 'todolist1')
        self.assertEqual(todo.description, 'todolist description')
        self.assertEqual(todo.category.name, 'test')

        response = self.client.put(url, data, content_type='application/json', headers=self.headers)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['id'], 1)
        self.assertEqual(response.json()['title'], data['title'])
        self.assertEqual(response.json()['description'], data['description'])
        self.assertEqual(response.json()['category'], data['category'])

        todo = TodoList.objects.get(id=1)
        self.assertEqual(todo.title, data['title'])
        self.assertEqual(todo.description, data['description'])
        self.assertEqual(todo.category.name, data['category'])

    def test_invalid_token(self):
        url = reverse('update', args=[1])

        headers = {'Authorization': f'{uuid.uuid4()}'}

        response = self.client.put(url, content_type='application/json', headers=headers)

        self.assertEqual(response.status_code, 401)
        self.assertIn('error', response.json())
        self.assertEqual(response.json()['error'], 'Invalid token')

    def test_missing_field(self):
        url = reverse('update', args=[1])

        response = self.client.put(url, dict(), content_type='application/json', headers=self.headers)

        self.assertEqual(response.status_code, 401)
        self.assertIn('message', response.json())
        self.assertEqual(response.json()['message'], 'Missing required field')

    def test_invalid_todo_id(self):
        url = reverse('update', args=[4])
        data = {
            'title': 'updated title',
            'description': 'updated description',
            'category': 'updated category'
        }

        response = self.client.put(url, data, content_type='application/json', headers=self.headers)

        self.assertEqual(response.status_code, 401)
        self.assertIn('error', response.json())
        self.assertEqual(response.json()['error'], 'invalid id')

    def test_not_owned_todo(self):
        url = reverse('update', args=[1])
        user = User.objects.create(
            name='SomeOtherGuy',
            email='<EMAIL>',
            password=make_password('<PASSWORD>')
        )
        headers = {'Authorization': f'{user.token}'}

        data = {
            'title': 'updated title',
            'description': 'updated description',
            'category': 'updated category'
        }

        response = self.client.put(url, data, content_type='application/json', headers=headers)

        self.assertEqual(response.status_code, 401)
        self.assertIn('error', response.json())
        self.assertEqual(response.json()['error'], 'Unauthorized: You don\'t own this todo')

    def test_invalid_method(self):
        url = reverse('update', args=[1])

        response = self.client.get(url, content_type='application/json', headers=self.headers)

        self.assertEqual(response.status_code, 405)
        self.assertIn('error', response.json())
        self.assertEqual(response.json()['error'], 'Invalid HTTP method')


class DeleteTodoTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            name='<NAME>',
            email='<EMAIL>',
            password=make_password('<PASSWORD>')
        )
        self.headers = {'Authorization': f'{self.user.token}'}
        self.data = [
            {
                'title': 'todolist1',
                'description': 'todolist description',
                'category': 'test'
            },
            {
                'title': 'todolist2',
                'description': 'todolist description',
                'category': 'category'
            },
            {
                'title': 'todolist3',
                'description': 'todolist description',
                'category': 'test category'
            }]

        for data in self.data:
            category = Category.objects.create(name=data['category'])
            TodoList.objects.create(
                title=data['title'],
                description=data['description'],
                category=category,
                author=self.user,
            )

    def test_delete_with_correct_data(self):
        url = reverse('delete', args=[2])

        response = self.client.delete(url, content_type='application/json', headers=self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json())
        self.assertEqual(response.json()['message'], 'deleted successfully')

        self.assertTrue(not TodoList.objects.filter(title='todolist2').exists())
        self.assertEqual(TodoList.objects.count(), 2)

    def test_invalid_token(self):
        url = reverse('delete', args=[1])
        headers = {'Authorization': f'{uuid.uuid4()}'}

        response = self.client.delete(url, content_type='application/json', headers=headers)

        self.assertEqual(response.status_code, 401)
        self.assertIn('error', response.json())
        self.assertEqual(response.json()['error'], 'Invalid token')

    def test_invalid_todo_id(self):
        url = reverse('delete', args=[4])
        response = self.client.delete(url, content_type='application/json', headers=self.headers)

        self.assertEqual(response.status_code, 401)
        self.assertIn('error', response.json())
        self.assertEqual(response.json()['error'], 'invalid id')

    def test_not_owned_todo(self):
        url = reverse('delete', args=[1])
        user = User.objects.create(
            name='SomeOtherGuy',
            email='example@example.com',
            password=make_password('<PASSWORD>')
        )

        headers = {'Authorization': f'{user.token}'}

        response = self.client.delete(url, content_type='application/json', headers=headers)

        self.assertEqual(response.status_code, 401)
        self.assertIn('error', response.json())
        self.assertEqual(response.json()['error'], 'Unauthorized: You don\'t own this todo')
