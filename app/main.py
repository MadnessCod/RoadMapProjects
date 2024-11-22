import argparse
import json

import urllib.request
import urllib.error
from collections import defaultdict


class GithubUserActivity:
    def __init__(self):

        self.url = 'https://api.github.com/'
        self.headers = {'Accept': 'application/vnd.github+json'}
        self.parser = argparse.ArgumentParser(description='Github User Activity CLI')
        self.add_argument()

    def add_argument(self):
        self.parser.add_argument('-u', '--username', help='Github username')

    def count_type_to_repo(self, events, type_):
        repo_push_event = defaultdict(list)
        for event in events:
            repo_name = event['repo']['name']
            repo_push_event[repo_name].append(event)

        if type_ == 'Push':
            for repo_name, event in repo_push_event.items():
                print(f'Pushed {len(event)} commits to {repo_name} ')
        elif type_ == 'Delete':
            for repo_name, event in repo_push_event.items():
                print(f'Deleted {len(event)} commits from {repo_name}')
        elif type_ == 'Pull':
            for repo_name, event in repo_push_event.items():
                print(f'Requested {len(event)} Pulls from {repo_name}')
        elif type_ == 'Create':
            for repo_name, event in repo_push_event.items():
                print(f'Created {repo_name}')
        elif type_ == 'Watch':
            for repo_name, event in repo_push_event.items():
                print(f'Started Watching {repo_name}')
        elif type_ == 'Member':
            for repo_name, event in repo_push_event.items():
                print(f'Membered to  {repo_name}: {len(event)}')
        else:
            for repo_name, event in repo_push_event.items():
                print(f'Unknown type {repo_name}: {len(event)}')

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
                self.count_type_to_repo(list(filter(lambda event: event['type'] == 'PushEvent', user_events)), 'Push')
                self.count_type_to_repo(list(filter(lambda event: event['type'] == 'DeleteEvent', user_events)), 'Delete')
                self.count_type_to_repo(list(filter(lambda event: event['type'] == 'PullRequestEvent', user_events)), 'Pull')
                self.count_type_to_repo(list(filter(lambda event: event['type'] == 'CreateEvent', user_events)), 'Create')
                self.count_type_to_repo(list(filter(lambda event: event['type'] == 'WatchEvent', user_events)), 'Watch')
                self.count_type_to_repo(list(filter(lambda event: event['type'] == 'MemberEvent', user_events)), 'Member')


if __name__ == '__main__':
    github = GithubUserActivity()
    github.run()
