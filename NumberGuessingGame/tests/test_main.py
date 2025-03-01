import unittest


from unittest.mock import patch

from app.main import RandomNumberGenerator


class RandomNumberGeneratorTest(unittest.TestCase):
    def setUp(self):
        self.game = RandomNumberGenerator()

    @patch('sys.argv', ['app.main.RandomNumberGenerator', '-m', 'easy', '-u', 'SomeUserName'])
    def test_easy_mode(self):
        args = self.game.parser.parse_args()
        self.assertEqual(len(vars(args)), 4)

    @patch('sys.argv', ['app.main.RandomNumberGenerator', '-m', 'medium', '-u', 'SomeUserName'])
    def test_medium_mode(self):
        args = self.game.parser.parse_args()
        self.assertEqual(len(vars(args)), 4)

    @patch('sys.argv', ['app.main.RandomNumberGenerator', '-m', 'hard', '-u', 'SomeUserName'])
    def test_hard_mode(self):
        args = self.game.parser.parse_args()
        self.assertEqual(len(vars(args)), 4)

    def tearDown(self):
        self.game = None


if __name__ == '__main__':
    unittest.main()
