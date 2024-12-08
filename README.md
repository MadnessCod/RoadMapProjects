## Personal Blog *django*
#### This project is created for roadmap.sh unit converter backend [project](https://roadmap.sh/projects/personal-blog)
A simple personal blog webapp

## Tables of contents 
 - [Features](#features-)
 - [Requirements](#requirements-)
 - [Installation](#installation)
 - [Usage](#usage-)

## Features 
- **add, update, delete articles**
- **user Dashboard**
- **Using Django Framework**

## Requirements 
- **python 3.x**
- **django 4.2**

## Installation
1. **Create a venv**
    ```bash
    python -m venv .venv
    ```
    for more information visit [python virtual environments](https://docs.python.org/3/tutorial/venv.html)
2. **Clone the repository:**
   ```bash
   git clone https://github.com/MadnessCod/PersonalBlogDjango.git
   ```
3. **Install requirements using poetry**
   ```bash
   pip install poetry
   ```
   ```bash
   poetry install
   ```
4. **create a local_settings.py**
   - create a local_settings.py file inside PersonalBlog1 folder
   - copy sample_settings.py file to local_settings.py 
   - create a secret_key 
     ```bash
     python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
     ```
   - this is your SECRET_KEY inside local_settings.py, put it there 
   

## Usage 
1. **head to http://localhost:8000/articles/**
2. **Sign up**
3. **Login**
4. **Add an article** 
5. **You can also edit, delete and view your dashboard**
   #### Enjoy
