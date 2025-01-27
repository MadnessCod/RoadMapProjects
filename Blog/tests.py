from django.test import TestCase, Client
from django.urls import reverse

from .models import Tag, Category, Post


# Create your tests here.


class ApiTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('posts')

        category = Category.objects.create(name='<CATEGORY>')

        tag1 = Tag.objects.create(name='<TAG1>')
        tag2 = Tag.objects.create(name='<TAG2>')

        self.post = Post.objects.create(
            title='<TITLE>',
            content='<CONTENT>',
            category=category,
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
