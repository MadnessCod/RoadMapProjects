## Number Guessing Game 
#### This project is created for roadmap.sh backend Number Guessing Game [project](https://roadmap.sh/projects/number-guessing-game)

## Table of contents
 - [Features](#features)
 - [Requirements](#requirements)
 - [Installation](#installation)
 - [Usage](#usage)

## Features
- **Play guessing game in three modes (easy, medium, hard)**
- **Save plays in a csv file**
- **List all previous runs**
- **See best score for each mode for specific username**

## Requirements
- **python 3.x**

## Installation
1. **Create a venv**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
   for more information visit [python virtual environments](https://docs.python.org/3/tutorial/venv.html)
2. **Clone the repository**
   ```bash
   git clone https://github.com/MadnessCod/NumberGuessingGame.git
   ```
3. **Install requirements using poetry**
   ```bash
   poetry install
   ```
   <span style="color: #33ffd7;">***this project doesn't need any external library, so you can use it with plain python***</span>

## Usage
```bash
cd app
```
1. **Start a game**
   - commands
     - --username or -u
     - --mode or -m, available modes are(easy, medium, hard)
     ```
     python main.py -u "Your username" -m "mode"
     ```
2. **List all previous runs**
    - commands 
      - --list or -l
      ```
      python main.py -l
      ```
3. **See the best score for each mode for each username**
    - commands
      - --best or -b 
      ```
      python main.py -b "Your username"
      ```
