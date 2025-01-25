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
        tag2 = Tag.objects.create(name='<TAG1>')

        self.post = Post.objects.create(
            title='<TITLE>',
            content='<CONTENT>',
            category=category,
        )
        self.post.tags.add(tag1, tag2)

    def test_successful_get(self):
        response = self.client.get(self.url, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['title'], '<TITLE>')
