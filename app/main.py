import argparse
import json

import urllib.request
import urllib.error


class GithubUserActivity:
    def __init__(self):

        self.url = 'https://api.github.com/'
        self.headers = {'Accept': 'application/vnd.github+json'}
        self.parser = argparse.ArgumentParser(description='Github User Activity CLI')
        self.add_argument()

    def add_argument(self):
        self.parser.add_argument('-u', '--username', help='Github username')

    def run(self):
        args = self.parser.parse_args()
        file = f'{args.username}.json'
        req = urllib.request.Request(f'{self.url}users/{args.username}/events', headers=self.headers)
        if args.username:
            try:
                with urllib.request.urlopen(req) as request:
                    user_events = json.loads(request.read().decode())
            except urllib.error.URLError as error:
                print(f'Error: {error}')
            else:
                with open(file, 'w') as file:
                    json.dump(user_events, file)


if __name__ == '__main__':
    github = GithubUserActivity()
    github.run()
