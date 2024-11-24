import argparse
import csv
import datetime


from datetime import date


class ExpenseTracker:
    def __init__(self):
        self.parser = argparse.ArgumentParser(prog='Expense Tracker')
        self.file = 'expense.csv'
        self.expense = dict()
        self.add_arguments()

    def add_arguments(self):
        self.parser.add_argument('-a', '--add', action='store_true', help='Add an expense')
        self.parser.add_argument('-d', '--description', help='Add a description')
        self.parser.add_argument('-am', '--amount', help='Add an amount')
        self.parser.add_argument('-u', '--update', help='Update an expense')
        self.parser.add_argument('-de', '--delete', help='Delete an expense')
        self.parser.add_argument('-l', '--list', help='List all expenses')
        self.parser.add_argument('-s', '--summery', help='view a specific months expense summery')
        self.parser.add_argument('-m', '--month', help='view a specific month expense summery')

    def add_expense(self, description, amount):
        self.expense[len(self.expense) + 1] = {
            'ID': len(self.expense) + 1,
            'Date': date.today().strftime('%Y-%m-%d'),
            'description': description,
            'amount': f'{amount}$',
        }

    def run(self):
        args = self.parser.parse_args()
        if args.add and args.description and args.amount:
            self.add_expense(args.description, args.amount)


if __name__ == '__main__':
    exp = ExpenseTracker()
    exp.run()
