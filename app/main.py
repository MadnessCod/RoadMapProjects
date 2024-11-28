import argparse
import json
import os

from datetime import datetime
from pprint import pprint
from typing import Dict


class TaskTracker:
    """TaskTracker class
    Attributes:
        tasks : dict
            Dictionary of tasks, keyed by task id
        tasks_file : json file with tasks
        parser : argparse parser
    """
    def __init__(self) -> None:
        self.tasks_file = 'tasks.json'
        self.parser = argparse.ArgumentParser(
            prog='TaskTracker',
            description='Keep track of your tasks, program saves tasks in a json file',
        )
        self.tasks = dict()
        self._add_arguments()

    def _add_arguments(self) -> None:
        """Adds arguments to the parser"""
        self.parser.add_argument('-a', '--add', type=str, help='Add a task')
        self.parser.add_argument('-u', '--update', type=str, help='Update task by it id')
        self.parser.add_argument(
            '-s',
            '--status',
            type=str,
            choices=['in progress', 'done'],
            help='Set status of a task, use it with --update, choices are "in progress", "done"',
        )
        self.parser.add_argument(
            'de',
            '--description',
            type=str,
            help='add description for a task, use it with --update'
        )
        self.parser.add_argument('-d', '--delete', type=int, help='Delete a task by it Id number')
        self.parser.add_argument(
            '-l',
            '--list',
            action='store_true',
            help='List all tasks from json file'
        )
        self.parser.add_argument(
            '-l_d',
            '--list_done',
            action='store_true',
            help='List tasks with done status'
        )
        self.parser.add_argument(
            '-l_p',
            '--list_progress',
            action='store_true',
            help='List tasks with in progress status'
        )
        self.parser.add_argument(
            '-l_t',
            '--list_todo',
            action='store_true',
            help='List todo tasks'
        )

    def save(self) -> None:
        """Saves tasks to json file"""
        with open(self.tasks_file, 'w') as f:
            json.dump(self.tasks, f)

    def load(self) -> Dict:
        """Loads tasks from json file"""
        if os.path.exists(self.tasks_file):
            with open(self.tasks_file, 'r') as f:
                return json.load(f)
        return dict()

    def add_task(self, task) -> None:
        """Adds a tasks from provided commandline arguments"""
        self.tasks = self.load()
        task_id = len(self.tasks) + 1
        self.tasks[task_id] = {'id': task_id,
                               'title': task,
                               'description': '',
                               'status': '',
                               'createdAt': datetime.now().isoformat(),
                               'updatedAt': datetime.now().isoformat(),
                               }
        self.save()

    def list_tasks(self) -> None:
        """reads tasks from json file and prints them on CLI"""
        self.tasks = self.load()
        for task in self.tasks:
            print(
                f'ID: {self.tasks[task]['id']}\n'
                f'Task: {self.tasks[task]['title']}\n'
                f'Description: {self.tasks[task]['description']}\n'
                f'Status: {self.tasks[task]['status']}\n'
                f'Created: {self.tasks[task]['createdAt']}\n'
                f'Updated: {self.tasks[task]['updatedAt']}'
            )

    def delete_task(self, task_id) -> None:
        """Deletes a task by its id
            Raises KeyError if task_id is not found
        """
        self.tasks = self.load()
        try:
            del self.tasks[task_id]
            self.save()
        except KeyError:
            print(f'Task with {task_id} not found')

    def update_status(self, task_id, status) -> None:
        """Update a task status by its id"""
        self.tasks = self.load()
        for task in self.tasks:
            if task == task_id:
                self.tasks[task]['status'] = status
                self.tasks[task]['updatedAt'] = datetime.now().isoformat()
                self.save()
            else:
                print(f'Task with {task_id} not found')

    def update_description(self, task_id, description) -> None:
        """"Updates a task description by its id"""
        self.tasks = self.load()
        for task in self.tasks:
            if task == task_id:
                self.tasks[task]['description'] = description
                self.tasks[task]['updatedAt'] = datetime.now().isoformat()
                self.save()
            else:
                print(f'Task with {task_id} not found')

    def run(self) -> None:
        """"Runs the tasks list"""
        args = self.parser.parse_args()
        if args.add:
            self.add_task(args.add)
        if args.list:
            self.list_tasks()
        if args.list_done:
            saved_tasks = self.load()
            pprint(list(filter(lambda task: task['status'] == 'done', saved_tasks.values())))
        if args.list_progress:
            saved_tasks = self.load()
            pprint(list(filter(lambda task: task['status'] == 'in progress', saved_tasks.values())))
        if args.list_todo:
            saved_tasks = self.load()
            pprint(list(filter(lambda task: task['status'] == '', saved_tasks.values())))
        if args.delete:
            self.delete_task(str(args.delete))
        if args.update and args.status:
            self.update_status(args.update, args.status)
        if args.update and args.description:
            self.update_description(args.update, args.description)


if __name__ == '__main__':
    tasks = TaskTracker()
    tasks.run()
