import datetime
import argparse
import json


class TaskTracker:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self._add_arguments()
        self.tasks = dict()

    def _add_arguments(self):
        self.parser.add_argument('-a', '--add')
        self.parser.add_argument('-u', '--update')
        self.parser.add_argument('-d', '--delete')

    def run(self):
        args = self.parser.parse_args()

        if args.add:
            self.tasks[args.add] = {'id': '',
                                    'description': '',
                                    'createdAt': datetime.datetime.now(),
                                    'updatedAt': datetime.datetime.now()
                                    }


if __name__ == '__main__':
    tasks = TaskTracker()
    tasks.run()

