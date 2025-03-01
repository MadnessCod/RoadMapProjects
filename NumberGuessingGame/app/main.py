import argparse
import random
import datetime
import time
import csv


class RandomNumberGenerator:
    """
    A class for guessing game in three different modes (easy, medium, hard)
    """
    def __init__(self) -> None:
        """
        Creates a random number between 1 and 100
        Creates a parser (argparse.ArgumentParser)
        calls add_argument()
        """
        self.number = random.randint(1, 100)
        self.file = 'Users.csv'
        self.users = list()
        self.parser = argparse.ArgumentParser(prog='Number Guessing Game')
        self.add_argument()

    def add_argument(self) -> None:
        """
        Adds Argument to self.parser
            -m, --mode for choosing game mode
            -u, --user for choosing username
            -l, --list for getting list of games a user done
            -b, --best to see best scores in each mode
        :return: None
        """
        self.parser.add_argument(
            '-m',
            '--mode',
            choices=['easy', 'medium', 'hard'],
            help='Mode of the game, choices are easy, medium, hard')
        self.parser.add_argument('-u', '--username', help='Users name')
        self.parser.add_argument('-l', '--list', action='store_true', help='List all user\'s game')
        self.parser.add_argument('-b', '--best', help='Get the lowest attempt of a users for different modes')

    def save(self, attempt=None, elapsed=0.) -> None:
        """
        Saves user attempt in guessing the random number in selected mode
        :param attempt: number of attempts to guess the random number or -1
        :param elapsed: time took to guess the number or 0 if user couldn't guess the number
        :return: None
        """
        args = self.parser.parse_args()
        user = {
            'User': args.username,
            'Date': datetime.date.today().strftime('%Y-%m-%d'),
            'Time': datetime.datetime.now().strftime('%H:%M:%S'),
            'Mode': args.mode,
            'Number': self.number,
            'Guesses': -1 if attempt is None else attempt,
            'Elapsed': f'{elapsed}s',
        }
        self.users = self.load()
        self.users.append(user)
        with open(self.file, 'w', newline='') as csvfile:
            writer = csv.DictWriter(
                csvfile,
                fieldnames=['User', 'Date', 'Time', 'Mode', 'Number', 'Guesses', 'Elapsed'])
            writer.writeheader()
            writer.writerows(self.users)

    def load(self) -> list:
        """
        Loads users data from csv file into a list
        :return: list of users data
        """
        try:
            with open(self.file, 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    self.users.append(row)
        except FileNotFoundError:
            print('File not found')
        return self.users

    def game(self, number: int) -> None:
        """
        Function to guess the number in given attempt, calls save function if you guess wrong or right
        :param number: maximum number of attempts to guess the random number or -1
        :return: None
        """
        print('Great! Let\'s start the game\n')
        start_time = time.time()
        for attempt in range(number):
            try:
                guess = int(input('Enter your guess: '))
            except ValueError:
                print('Enter a valid number ')
                attempt -= 1
            else:
                if guess in range(1, 101):
                    if guess > self.number:
                        print('Too high')
                    elif guess < self.number:
                        print('Too low')
                    elif guess == self.number:
                        end_time = time.time()
                        elapsed_time = end_time - start_time
                        self.save(attempt, round(elapsed_time, 2))
                        print(
                            f'Congratulations! You guessed the correct number in {attempt} attempts in {round(elapsed_time, 2)} seconds. ')
                        return
                else:
                    print(f'Hey enter a number between 1 and 100')
                    print('Don\'t worry I won\'t deduct a point for that')
                    attempt -= 1
        print(f'The game has finished, you could\'t guess the number, the number was {self.number}')
        self.save()

    def best_score(self, entries: list) -> None:
        """
        prints Best score for each mode for specific user
        :param entries: list of users previous game data from csv file
        """
        for type_ in ['easy', 'medium', 'hard']:
            filtered = list(filter(lambda entry: entry['Mode'] == type_, entries))
            try:
                print(
                    f'the lowest attempt for {type_} is: ',
                    min([int(i['Guesses']) for i in filtered if int(i['Guesses']) > 0])
                )
            except ValueError:
                print(f'There is no best score for {type_} mode')

    def run(self) -> None:
        """
        calls game function to start playing game
        prints list of games done before for all users
        calls best_score function to print best score for each mode for specific user
        """
        args = self.parser.parse_args()
        if args.username and args.mode:
            if args.mode == 'easy':
                print('You have chosen Easy Mode you have 10 chances to guess the correct number')
                self.game(10)
            elif args.mode == 'medium':
                print('You have chosen Medium Mode you have 5 chances to guess the correct number')
                self.game(5)
            elif args.mode == 'hard':
                print('You have chosen Hard Mode you have 3 chances to guess the correct number')
                self.game(3)
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
