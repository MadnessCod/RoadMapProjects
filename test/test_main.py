import unittest

from app.main import GithubUserActivity


class GithubUserActivityTests(unittest.TestCase):
    def setUp(self):
        self.github_user = GithubUserActivity()

    def tearDown(self):
        GithubUserActivity.github_user = None