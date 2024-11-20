import json
import sys
import os
import io
import unittest


from app.main import TaskTracker


class TaskTrackerTest(unittest.TestCase):
    def setUp(self):
        self.test_file = 'tasks.json'
        self.tasktracker = TaskTracker()

        self.sample_tasks = {
            '1': {
                'id': 1,
                'title': 'doing homeworks',
                'description': 'math and physics homework',
                'status': '',
                'createdAt': '2024-11-20T18:57:22.781752',
                'updatedAt': '2024-11-20T18:57:22.781752',
            },
            '2': {
                'id': 2,
                'title': 'vising parents',
                'description': '',
                'status': 'done',
                'createdAt': '2024-11-20T18:56:50.209456',
                'updatedAt': '2024-11-20T18:56:50.209456',
            },
            '3': {
                'id': 3,
                'title': 'reading books',
                'description': '',
                'status': 'in progress',
                'createdAt': '2024-12-20T18:57:50.123456',
                'updatedAt': '2024-12-20T18:57:50.123456',
            }
        }
        with open(self.test_file, 'w') as f:
            json.dump(self.sample_tasks, f)
        print('creating a new tasks files')

    def test_add_task(self):
        self.tasktracker.add_task('calling mom')
        tasks = self.tasktracker.load()
        self.assertEqual(len(tasks), 4)
        self.assertTrue(any(task['title'] == 'calling mom' for task in tasks.values()))

    def test_list(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.tasktracker.list_tasks()
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue()
        self.assertIn('doing homeworks', output)
        self.assertIn('vising parents', output)

    def test_delete_task(self):
        self.tasktracker.delete_task('calling mom')
        tasks = self.tasktracker.load()
        self.assertFalse(any(task['title'] == 'calling mom' for task in tasks.values()))

    def test_update_status(self):
        self.tasktracker.update_status('1', 'done')
        tasks = self.tasktracker.load()
        self.assertTrue(tasks['1']['status'] == 'done')

    def test_update_description(self):
        self.tasktracker.update_description('3', 'read math books')
        tasks = self.tasktracker.load()
        self.assertTrue(tasks['3']['description'] == 'read math books')

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        self.taskTracker = None


if __name__ == '__main__':
    unittest.main()
