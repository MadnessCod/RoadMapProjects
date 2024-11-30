## Unit Converter *django*
#### This project is created for roadmap.sh unit converter backend [project](https://roadmap.sh/projects/unit-converter)
A simple web app to convert units
## Tables of contents 
 - [Features](#features-)
 - [Requirements](#requirements-)
 - [Installation](#installation)
 - [Usage](#usage-)

## Features 
- **Support conversion for length, weight and temperature**
- **Using Django Framework**

## Requirements 
- **python 3.x**
- **django 4.2**

## Installation
1. **Create a venv**
    ```
    python -m venv .venv
    ```
    for more information visit [python virtual environments](https://docs.python.org/3/tutorial/venv.html)
2. **Clone the repository:**
   ```
   git clone https://github.com/MadnessCod/UnitConverter_django.git
   ```
3. **Install requirements using poetry**
   ```
   pip install poetry
   ```
   ```
   poetry install
   ```
4. **create a local_settings.py**
   - create a local_settings.py file inside Units folder
   - copy sample_settings.py file to local_settings.py 
   - create a secret_key 
     ```
     python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
     ```
   - this is your SECRET_KEY inside local_settings.py, put it there 
   

## Usage 
1. **head to http://localhost:8000/**
2. **Select the type of unit**
3. **Select unit to convert and unit convert from**
4. **Enter a value** 
5. **Hit Convert**
   #### Enjoy
