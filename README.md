# Github User Activity 

#### This project is created for roadmap.sh backend GitHub User Activity [Project](https://roadmap.sh/projects/github-user-activity)

## Table of contents 
 - [Features](#features)
 - [Requirements](#requirements-)
 - [Installation](#installation)
 - [Usage](#usage-)

## Features
- **See a User's recent activity on github**

## Requirements 
- **python 3.x**

## Installation
1. **Create a venv**
    ```bash
   python -m venv .venv
   .venv\Scripts\Activate
    ```
   for more information visit [python virtual environments guide](https://docs.python.org/3/tutorial/venv.html)
2. **Clone the repository**
    ```bash
   git clone https://github.com/MadnessCod/GihubUserActivity.git
   ```
3. **install requirements using poetry**
   ```bash
   poetry install
   ```
   <span style="color: #33ffd7;">***this project doesn't need any external library, so you can use it with plain python***</span>

## Usage 
```bash
cd app
```
1. **request a user's activity with github username**
   - commands: <span style="color: #2ecc71;">--username</span> or <span style="color: #2ecc71;">-u</span>
   ```bash
   python main.py -u <username>
   ```