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
        self.parser.add_argument('-m', '--mode', choices=['easy', 'medium', 'hard'])
        self.parser.add_argument('-u', '--username', help='Users name')

    def save(self, attempt):
        args = self.parser.parse_args()
        user = {
            'User': args.username,
            'Date': datetime.date.today().strftime('%Y-%m-%d'),
            'Time': datetime.datetime.now().strftime('%H:%M:%S'),
            'Mode': args.mode,
            'Number': self.number,
            'Guesses': 'failed' if attempt is None else attempt,
        }
        self.load()
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

    def game(self, username, mode, number):
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
                        print(f'Correct the number was {self.number}')
                        self.save(attempt)
                        break
                else:
                    print(f'Hey enter a number between 1 and 100')
                    print('Don\'t worry I won\'t deduct a point for that')
                    attempt -= 1
        print(f'The game has finished, you could\'t guess the number, the number was {self.number}')
        self.save(attempt=None)

    def run(self):
        args = self.parser.parse_args()
        if args.username:
            if args.mode == 'easy':
                print('You have chosen Easy Mode you have 10 chances ')
                self.game(args.username, args.mode, 10)
            elif args.mode == 'medium':
                print('You have chosen Medium Mode you have 5 chances')
                self.game(args.username, args.mode, 5)
            elif args.mode == 'hard':
                print('You have chosen Hard Mode you have 3 chances')
                self.game(args.username, args.mode, 3)
            else:
                print('you haven\'t chosen any mode')


if __name__ == '__main__':
    game = RandomNumberGenerator()
    game.run()
