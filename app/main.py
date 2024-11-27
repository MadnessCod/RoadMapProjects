import argparse
import random
import csv


class RandomNumberGenerator:
    def __init__(self):
        self.number = random.randint(1, 100)
        self.file = 'Users.csv'
        self.parser = argparse.ArgumentParser(prog='Number Guessing Game')
        self.add_argument()

    def add_argument(self):
        self.parser.add_argument('-m', '--mode', choices=['easy', 'medium', 'hard'], default='easy')

    def game(self, number):
        for i in range(number):
            try:
                guess = int(input('Enter your guess: '))
            except ValueError:
                print('Enter a valid number ')
                i -= 1
            else:
                if guess > self.number:
                    print('Too high')
                elif guess < self.number:
                    print('Too low')
                elif guess == self.number:
                    print(f'Correct the number was {self.number}')
                    break

    def run(self):
        args = self.parser.parse_args()
        if args.mode == 'easy':
            print('You have chosen Easy Mode you have 10 chances ')
            self.game(10)
        elif args.mode == 'medium':
            print('You have chosen Medium Mode you have 5 chances')
            self.game(5)
        else:
            print('You have chosen Hard Mode you have 3 chances')
            self.game(3)
