from django.test import TestCase


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