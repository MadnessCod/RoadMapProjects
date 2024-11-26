import argparse
import calendar
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
        self.parser.add_argument('-am', '--amount', type=int, help='Add an amount')
        self.parser.add_argument('-u', '--update', help='Update an expense')
        self.parser.add_argument('-de', '--delete', help='Delete an expense')
        self.parser.add_argument('-l', '--list', action='store_true', help='List all expenses')
        self.parser.add_argument('-s', '--summery', action='store_true', help='view a specific months expense summery')
        self.parser.add_argument('-m', '--month', type=int, help='view a specific month expense summery')

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
        self.expense = self.load()
        expense = {
            'ID': len(self.expense) + 1,
            'Date': date.today().strftime('%Y-%m-%d'),
            'Description': description,
            'Amount': f'{amount}$',
        }
        self.expense.append(expense)
        self.save()
        print(f'Expense added successfully (ID: {expense["ID"]})')

    def update_description(self, task_id, description):
        expenses = self.load()
        for expense in expenses:
            if expense['ID'] == task_id:
                expense['Description'] = description
                self.save()
                return

        print(f'Task with ID {task_id} not found')

    def update_amount(self, task_id, amount):
        expenses = self.load()
        for expense in expenses:
            if expense['ID'] == task_id:
                expense['Amount'] = f'{amount}$'
                self.save()
                return

        print(f'Task with ID {task_id} not found')

    def delete_expense(self, task_id):
        self.expense = self.load()
        for expense in self.expense:
            if expense['ID'] == task_id:
                self.expense.remove(expense)
                self.save()
                return

        print(f'Task with ID {task_id} not found')

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
            for expense in expenses:
                print(f'ID: {expense["ID"]} '
                      f'Date: {expense["Date"]} '
                      f'Description: {expense["Description"]} '
                      f'Amount: {expense["Amount"]}'
                      )
        if args.summery:
            expenses = self.load()
            mapped = list(map(lambda amount: int(amount['Amount'].split('$')[0]), expenses))
            print(f'Total expense :{sum(mapped)}$')
        if args.month:
            expenses = self.load()
            filtered = list(filter(lambda entry: datetime.date.fromisoformat(entry['Date']).month == args.month, expenses))
            filtered_expenses = sum([int(i['Amount'].split('$')[0]) for i in filtered])
            print(f'Total expenses for {calendar.month_name[args.month]}: {filtered_expenses}$')


if __name__ == '__main__':
    exp = ExpenseTracker()
    exp.run()
