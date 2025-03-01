import argparse
import json

import urllib.request
import urllib.error


from collections import defaultdict


class GithubUserActivity:
    """
    Attributes:
        url : str
            url of GitHub user activity api
        headers : dict
            Dictionary of HTTP Headers to send with the Request.
        event_types : list(str)
            List of different Event Types returned by the API.
        parser : argparse.ArgumentParser
    """
    def __init__(self) -> None:
        self.url = 'https://api.github.com/'
        self.headers = {'Accept': 'application/vnd.github+json'}
        self.event_types = [
            'CommitComment', 'Create', 'Delete', 'Fork',
            'Gollum', 'IssueComment', 'Issue', 'Member',
            'Public', 'PullRequest', 'PullRequestReview', 'PullRequestReviewComment',
            'PullRequestReviewThread', 'Push', 'Release', 'Sponsorship', 'Watch'
        ]
        self.parser = argparse.ArgumentParser(description='Github User Activity CLI')
        self.add_argument()

    def add_argument(self) -> None:
        """adds arguments to the parser"""
        self.parser.add_argument('-u', '--username', help='Github username')

    def count_type_to_repo(self, events: list, type_: str) -> None:
        """Counts the number of types of each event type and prints it to the console"""
        repo_event = defaultdict(list)
        for event in events:
            repo_name = event['repo']['name']
            repo_event[repo_name].append(event)

        if type_ == 'Push':
            for repo_name, event in repo_event.items():
                print(f'Pushed {len(event)} commits to {repo_name} ')
        elif type_ == 'CommitComment':
            for repo_name, event in repo_event.items():
                print(f'Made {len(event)} comments to {repo_name} ')
        elif type_ == 'Delete':
            for repo_name, event in repo_event.items():
                print(f'Deleted {len(event)} commits from {repo_name}')
        elif type_ == 'Create':
            for repo_name, event in repo_event.items():
                print(f'Created {repo_name}')
        elif type_ == 'Watch':
            for repo_name, event in repo_event.items():
                print(f'Started Watching {repo_name}')
        elif type_ == 'Member':
            for repo_name, event in repo_event.items():
                print(f'Membered to  {repo_name}: {len(event)}')
        elif type_ == 'Fork':
            for repo_name, event in repo_event.items():
                print(f'Forked {repo_name}')
        elif type_ == 'Gollum':
            for repo_name, event in repo_event.items():
                print(f'Gollum for {repo_name}')
        elif type_ == 'IssueComment':
            for repo_name, event in repo_event.items():
                print(f'IssueComment for {repo_name}')
        elif type_ == 'Issue':
            for repo_name, event in repo_event.items():
                print(f'Opened a issue on {repo_name}')
        elif type_ == 'Public':
            for repo_name, event in repo_event.items():
                print(f'Opened a public repo on {repo_name}')
        elif type_ == 'PullRequest':
            for repo_name, event in repo_event.items():
                print(f'Opened a pull request on {repo_name}')
        elif type_ == 'PullRequestReview':
            for repo_name, event in repo_event.items():
                print(f'Opened a pull request review on {repo_name}')
        elif type_ == 'PullRequestReviewComment':
            for repo_name, event in repo_event.items():
                print(f'Opened a pull request review comment on {repo_name}')
        elif type_ == 'PullRequestReviewThread':
            for repo_name, event in repo_event.items():
                print(f'Opened a pull request review thread on {repo_name}')
        elif type_ == 'Release':
            for repo_name, event in repo_event.items():
                print(f'Opened a release on {repo_name}')
        elif type_ == 'Sponsorship':
            for repo_name, event in repo_event.items():
                print(f'Started sponsoring {repo_name}')
        else:
            for repo_name, event in repo_event.items():
                print(f'Unknown type {repo_name}: {len(event)}')

    def run(self):
        """"Runs different arguments
        :raises urllib.error.URLError
        """
        args = self.parser.parse_args()
        req = urllib.request.Request(f'{self.url}users/{args.username}/events', headers=self.headers)
        if args.username:
            try:
                with urllib.request.urlopen(req) as request:
                    user_events = json.loads(request.read().decode())
            except urllib.error.URLError as error:
                print(f'Error: {error}')
            else:
                for event_type in self.event_types:
                    self.count_type_to_repo(
                        list(filter(lambda event: event['type'] == f'{event_type}Event', user_events)),
                        event_type
                    )


if __name__ == '__main__':
    github = GithubUserActivity()
    github.run()
