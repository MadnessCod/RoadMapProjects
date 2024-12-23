import unittest

from unittest.mock import patch
from app.main import ExpenseTracker


class ExpenseTrackerTest(unittest.TestCase):
    def setUp(self):
        self.expense = ExpenseTracker()

    @patch('sys.argv', ['app.main.ExpenseTracker', '-a', '-d', 'book', '-am', 15])
    def test_arguments(self):
        args = self.expense.parser.parse_args()
        self.assertEqual(len(vars(args)), 8)
        self.assertEqual(args.add, 'books')

    @patch('sys.argv', ['app.main.ExpenseTracker', '-u', '1', '-d', 'buying coffee'])
    def test_update_description(self):
        args = self.expense.parser.parse_args()
        self.assertEqual(args.description, 'buying coffee')

    def tearDown(self):
        self.expense = None


if __name__ == '__main__':
    unittest.main()
