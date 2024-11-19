import argparse
import json

from datetime import datetime


class TaskTracker:
    def __init__(self):
        self.tasks_file = 'tasks.json'
        self.parser = argparse.ArgumentParser(prog='TaskTracker')
        self._add_arguments()
        self.tasks = dict()

    def _add_arguments(self):
        self.parser.add_argument('-a', '--add', nargs='+', type=str, help='Add task')
        self.parser.add_argument('-u', '--update', nargs='+', type=int, help='Update task')
        self.parser.add_argument('-d', '--delete')

    def save(self):
        with open(self.tasks_file, 'w') as f:
            json.dump(self.tasks, f)

    def run(self):
        args = self.parser.parse_args()
        for arg in args.add:
            self.tasks[len(self.tasks) + 1] = {'id': len(self.tasks) + 1,
                                               'title': arg,
                                               'description': '',
                                               'status': '',
                                               'createdAt': datetime.now().isoformat(),
                                               'updatedAt': datetime.now().isoformat(),
                                               }
        self.save()


if __name__ == '__main__':
    tasks = TaskTracker()
    tasks.run()
