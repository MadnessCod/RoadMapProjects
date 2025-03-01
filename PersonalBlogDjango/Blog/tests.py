from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Article
# Create your tests here.


class ArticleTestCase(TestCase):
    def setUp(self):
        self.valid_payload = {
            'title': '<TITLE>',
            'content': '<CONTENT>',
            'author': '<AUTHOR>',
        }

    def test_create_article(self):
        Article.objects.create(
            title=self.valid_payload['title'],
            content=self.valid_payload['content'],
            author=self.valid_payload['author'],
        )

        self.assertEqual(Article.objects.count(), 1)


class SignupViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')

    def test_signup_view_get(self):

        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

    def test_signup_view_post_valid_data(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'TestPass123!',
            'password2': 'TestPass123!'
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_signup_view_post_invalid_data(self):
        data = {
            'username': '',
            'email': 'invalidemail',
            'password1': 'TestPass123!',
            'password2': 'MismatchPass123!'
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(email='invalidemail').exists())
        self.assertContains(response, "This field is required.")

    def test_signup_view_duplicate_username(self):
        User.objects.create_user(username='testuser', email='testuser@example.com', password='TestPass123!')
        data = {
            'username': 'testuser',
            'email': 'newemail@example.com',
            'password1': 'TestPass123!',
            'password2': 'TestPass123!'
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A user with that username already exists.")
