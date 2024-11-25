import argparse
import csv
import datetime

from datetime import date


class ExpenseTracker:
    def __init__(self):
        self.parser = argparse.ArgumentParser(prog='Expense Tracker')
        self.file = 'expense.csv'
        self.expense = list()
        self.add_arguments()

    def add_arguments(self):
        self.parser.add_argument('-a', '--add', action='store_true', help='Add an expense')
        self.parser.add_argument('-d', '--description', help='Add a description')
        self.parser.add_argument('-am', '--amount', help='Add an amount')
        self.parser.add_argument('-u', '--update', help='Update an expense')
        self.parser.add_argument('-de', '--delete', help='Delete an expense')
        self.parser.add_argument('-l', '--list', action='store_true', help='List all expenses')
        self.parser.add_argument('-s', '--summery', help='view a specific months expense summery')
        self.parser.add_argument('-m', '--month', help='view a specific month expense summery')

    def load(self):
        try:
            with open(self.file, 'r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.expense.append(row)
        except FileNotFoundError:
            print('File not found')
        return self.expense

    def save(self):
        with open(self.file, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['ID', 'Date', 'Description', 'Amount'])
            writer.writeheader()
            writer.writerows(self.expense)

    def add_expense(self, description, amount):
        self.expense.append({
            'ID': len(self.expense) + 1,
            'Date': date.today().strftime('%Y-%m-%d'),
            'Description': description,
            'Amount': f'{amount}$',
        })
        self.save()

    def update_description(self, task_id, description):
        pass

    def update_amount(self, task_id, amount):
        pass

    def delete_expense(self, task_id):
        pass

    def run(self):
        args = self.parser.parse_args()
        if args.add and args.description and args.amount:
            self.add_expense(args.description, args.amount)

        if args.update and args.description:
            self.update_description(args.update, args.description)
        if args.update and args.amount:
            self.update_amount(args.update, args.amount)
        if args.delete:
            self.delete_expense(args.delete)
        if args.list:
            expenses = self.load()
            print(expenses)


if __name__ == '__main__':
    exp = ExpenseTracker()
    exp.run()
