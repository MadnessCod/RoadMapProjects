## Task Tracker CLI (Python)
#### This project is created for roadmap.sh backend tasktracker cli [project](https://roadmap.sh/projects/task-tracker)

## Table of contents
 - [Features](#features-)
 - [Requirements](#requirements-)
 - [Installation](#installation)
 - [Usage](#usage)


## Features 
- **Add, Update and Delete Tasks**
- **Mark a task as in progress or done**
- **List all tasks**
- **List all tasks that are done**
- **List all tasks that are not done**
- **List all tasks that are in progress**

## Requirements 
- **python 3.x**

## Installation
1. **Create a venv**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
   for more information visit [python virtual environments](https://docs.python.org/3/tutorial/venv.html)
2. **Clone the repository:**
    ```bash
    git clone https://github.com/MadnessCod/TaskTrackerCLI
    ```          
3. **install requirements using poetry**
    ```
   poetry install
   ```
   <span style="color: #33ffd7;">***this project doesn't need any external library, so you can use it with plain python***</span>

## Usage
   ```bash
   cd app
   ```
1. **Create a task**
   - commands: <span style="color: #2ecc71;">--add</span> or <span style="color: #2ecc71;">-a</span> 
   ```bash
   python main.py --add "your task"
   ```
2. **list all task**
   - commands: <span style="color: #2ecc71;">--list</span> or <span style="color: #2ecc71;">-l</span> 
   ```bash
   pyton -m main.py --list
   ```
3. **Update a tasks status**
   - commands: <span style="color: #2ecc71;">--update</span> or <span style="color: #2ecc71;">-u</span> 
   - commands: <span style="color: #2ecc71;">--status</span> or <span style="color: #2ecc71;">-s</span> 
   - can only use <span style="color: #fa6756;">done</span> or <span style="color: #fa6756;">in progress</span>
   ```bash
   python main.py --update task_id --status "done"
   ```
   ```bash
   python main.py --update task_id --status "in progress"
   ```
4. **Update a task Description**
   - commands: <span style="color: #2ecc71;">--update</span> or <span style="color: #2ecc71;">-u</span> 
   - commands: <span style="color: #2ecc71;">--description</span>
   ```bash
   pyton main.py --update task_id --description "your description"
   ```
5. **list tasks that are done**
   - commands: <span style="color: #2ecc71;">--list_done</span> or <span style="color: #2ecc71;">-l_d</span>
   ```bash
   python main.py --list_done
   ```
6. **list tasks that are in progress**
   - commands: <span style="color: #2ecc71;">--list_progress</span> or <span style="color: #2ecc71;">-l_p</span>
   ```bash
   python main.py --list_progress
   ```
7. **list todo tasks**
   - commands: <span style="color: #2ecc71;">--list_todo</span> or <span style="color: #2ecc71;">-l_t</span>
   ```bash
   python main.py --list_todo
   ```
8. **delete a task**
   - commands: <span style="color: #2ecc71;">--delete</span> or <span style="color: #2ecc71;">-d</span>
   ```bash
   python main.py --delete task_id
   ```