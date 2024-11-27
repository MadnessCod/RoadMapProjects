import argparse
import random
import datetime
import csv


class RandomNumberGenerator:
    def __init__(self):
        self.number = random.randint(1, 100)
        self.file = 'Users.csv'
        self.users = list()
        self.parser = argparse.ArgumentParser(prog='Number Guessing Game')
        self.add_argument()

    def add_argument(self):
        self.parser.add_argument(
            '-m',
            '--mode',
            choices=['easy', 'medium', 'hard'],
            help='Mode of the game, choices are easy, medium, hard')
        self.parser.add_argument('-u', '--username', help='Users name')
        self.parser.add_argument('-l', '--list', action='store_true', help='List all user\'s game')
        self.parser.add_argument('-b', '--best', help='Get the lowest attempt of a users for different modes')

    def save(self, attempt=None):
        args = self.parser.parse_args()
        user = {
            'User': args.username,
            'Date': datetime.date.today().strftime('%Y-%m-%d'),
            'Time': datetime.datetime.now().strftime('%H:%M:%S'),
            'Mode': args.mode,
            'Number': self.number,
            'Guesses': -1 if attempt is None else attempt,
        }
        self.users = self.load()
        self.users.append(user)
        with open(self.file, 'w', newline='') as csvfile:
            writer = csv.DictWriter(
                csvfile,
                fieldnames=['User', 'Date', 'Time', 'Mode', 'Number', 'Guesses'])
            writer.writeheader()
            writer.writerows(self.users)

    def load(self):
        try:
            with open(self.file, 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    self.users.append(row)
        except FileNotFoundError:
            print('File not found')
        return self.users

    def game(self, number):
        for attempt in range(number):
            try:
                guess = int(input('Enter your guess: '))
            except ValueError:
                print('Enter a valid number ')
                attempt -= 1
            else:
                if guess in range(1, 100):
                    if guess > self.number:
                        print('Too high')
                    elif guess < self.number:
                        print('Too low')
                    elif guess == self.number:
                        print(f'Correct, the number was {self.number}')
                        self.save(attempt)
                        return
                else:
                    print(f'Hey enter a number between 1 and 100')
                    print('Don\'t worry I won\'t deduct a point for that')
                    attempt -= 1
        print(f'The game has finished, you could\'t guess the number, the number was {self.number}')
        self.save()

    def best_score(self, entries):
        for type_ in ['easy', 'medium', 'hard']:
            filtered = list(filter(lambda entry: entry['Mode'] == type_, entries))
            try:
                print(min([int(i['Guesses']) for i in filtered if int(i['Guesses']) > 0]))
            except ValueError:
                print(f'There is no attempt for {type_} mode')

    def run(self):
        args = self.parser.parse_args()
        if args.username:
            if args.mode == 'easy':
                print('You have chosen Easy Mode you have 10 chances ')
                self.game(10)
            elif args.mode == 'medium':
                print('You have chosen Medium Mode you have 5 chances')
                self.game(5)
            elif args.mode == 'hard':
                print('You have chosen Hard Mode you have 3 chances')
                self.game(3)
            else:
                print('you haven\'t chosen any mode')
        if args.list:
            self.users = self.load()
            for user in self.users:
                print(f'User: {user["User"]}, Date: {user["Date"]}, Time: {user["Time"]}, '
                      f'Mode: {user["Mode"]}, Number: {user["Number"]}, Guesses: {user["Guesses"]}')
        if args.best:
            self.users = self.load()
            filtered = list(filter(lambda person: person['User'] == args.best, self.users))
            if filtered:
                self.best_score(filtered)
            else:
                print(f'There is no such user : {args.best}')


if __name__ == '__main__':
    game = RandomNumberGenerator()
    game.run()
