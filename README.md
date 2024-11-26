## Expense Tracker CLI 
#### This project is created for roadmap.sh backend Expense Tracker [project](https://roadmap.sh/projects/expense-tracker)

## Table of contents
 - [Features](#features)
 - [Requirements](#requirements)
 - [Installation](#installation)
 - [Usage](#usage)

## Features
- **Add, Update and Delete Expenses**
- **List all expenses**
- **Get the summary of expenses**
- **Get summary for a specific month**

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
    git clone https://github.com/MadnessCod/ExpenseTrackerCLI.git
    ```          
3. **install requirements using poetry**
    ```
   poetry install
   ```
   <span style="color: #33ffd7;">***this project doesn't need any external library, so you can use it with plain python***</span>

## Usage
```
cd app
```
1. **Add an Expense**
   - commands: 
      - <span style="color: #2ecc71;">--add</span> or <span style="color: #2ecc71;">-a</span>
      - <span style="color: #2ecc71;">--description</span> or <span style="color: #2ecc71;">-d</span>
      - <span style="color: #2ecc71;">--amount</span> or <span style="color: #2ecc71;">-am</span>
       ```
      python main.py -a -d "Expense description" -am amount
       ```
     - example: 
      ```
      python main.py -a -d "Lunch" -am 20 
      ```
2. **List all Expenses**
   - commands
     - <span style="color: #2ecc71;">--list</span> or <span style="color: #2ecc71;">-l</span>
     ```
     python main.py -l
     ```

3. **Update a Expense description**
   - commands: 
     - <span style="color: #2ecc71;">--update</span> or <span style="color: #2ecc71;">-u</span>
     - <span style="color: #2ecc71;">--description</span> or <span style="color: #2ecc71;">-d</span>
       ```
       python main.py -u expense id -d "new description"
       ```
       - example: 
      ```
      python main.py -u 1 -d "Books"
      ```

4. **Update a Expense amount**
    - commands:
      - <span style="color: #2ecc71;">--update</span> or <span style="color: #2ecc71;">-u</span>
      - <span style="color: #2ecc71;">--amount</span> or <span style="color: #2ecc71;">-am</span>
      ```
      python main.py -u expense id -am new amount
      ```
      - example: 
      ```
      python main.py -u 1 am 30
      ```

5. **Delete a task**
    - commands: 
      - <span style="color: #2ecc71;">--delete</span> or <span style="color: #2ecc71;">-de</span>
      ```
      python main.py -de expense id
      ```
      - example: Delete second task
      ```
      python main.py -de 1
      ```

6. **Get the summary of expenses**
    - commands:
      - <span style="color: #2ecc71;">--summary</span> or <span style="color: #2ecc71;">-s</span>
      ```
      python main.py -s
      ```

7. **Get the summary of a specific month**
    - commands: 
      - <span style="color: #2ecc71;">--month</span> or <span style="color: #2ecc71;">-m</span>
      ```
      python main.py -m month number
      ```
      - example: get the summary for november
      ```
      python main.py -m 11
      ```