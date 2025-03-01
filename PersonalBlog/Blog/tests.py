from django.test import TestCase, Client
from django.urls import reverse

from .models import Tag, Category, Post


# Create your tests here.


class ApiTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('posts')

        self.category = Category.objects.create(name='<CATEGORY>')

        tag1 = Tag.objects.create(name='<TAG1>')
        tag2 = Tag.objects.create(name='<TAG2>')

        self.post = Post.objects.create(
            title='<TITLE>',
            content='<CONTENT>',
            category=self.category,
        )
        self.post.tags.add(tag1, tag2)

        self.valid_payload = {
            'title': '<TITLE>',
            'content': '<CONTENT>',
            'category': '<CATEGORY>',
            'tags': ['<TAG1>', '<TAG2>']
        }
        self.invalid_payload = {
            'title': '<TITLE>',
        }

    def test_successful_get(self):
        response = self.client.get(self.url, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['title'], '<TITLE>')

    def test_successful_id_get(self):
        tag3 = Tag.objects.create(name='<TAG3>')
        post = Post.objects.create(
            title='<TITLE2>',
            content='<CONTENT2>',
            category=self.category,
        )
        post.tags.add(tag3)

        url = f'{self.url}2/'
        response = self.client.get(url, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['title'], '<TITLE2>')

    def test_successful_post(self):
        response = self.client.post(self.url, self.valid_payload, content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['title'], '<TITLE>')
        self.assertEqual(response.json()['tags'], ['<TAG1>', '<TAG2>'])

    def test_unsuccessful_post(self):
        response = self.client.post(self.url, self.invalid_payload, content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_successful_put(self):
        data = {
            'title': '<CHANGED TITLE>'
        }
        url = f'{self.url}1/'
        response = self.client.put(url, data, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['title'], '<CHANGED TITLE>')

    def test_invalid_id_put(self):
        url = f'{self.url}2/'
        response = self.client.put(url, {'title': '<CHANGED TITLE>'}, content_type='application/json')

        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.json())

    def test_successful_delete(self):
        url = f'{self.url}1/'
        response = self.client.delete(url, content_type='application/json')
        self.assertEqual(response.status_code, 204)

    def test_unsuccessful_delete(self):
        url = f'{self.url}2/'
        response = self.client.delete(url, content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_not_allowed_method(self):
        response = self.client.patch(self.url, self.valid_payload, content_type='application/json')
        self.assertEqual(response.status_code, 405)
