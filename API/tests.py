from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from .models import Category, User


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
