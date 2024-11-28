import unittest

from unittest.mock import patch
from app.main import GithubUserActivity


class GithubUserActivityTest(unittest.TestCase):
    def setUp(self):
        self.github_user = GithubUserActivity()

    @patch('sys.argv', ['app.main.GithubUserActivity', '-u', 'Somename'])
    def test_argument_length(self):
        self.github_user.run()
        self.assertEqual(len(vars(self.github_user.parser.parse_args())), 1)

    def tearDown(self):
        GithubUserActivity.github_user = None
