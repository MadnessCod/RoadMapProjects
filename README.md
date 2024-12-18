## Weather API
#### This project is created for roadmap.sh unit converter backend [project](https://roadmap.sh/projects/weather-api-wrapper-service)
A simple personal blog webapp

## Tables of contents 
 - [Features](#features-)
 - [Requirements](#requirements-)
 - [Installation](#installation)
 - [Usage](#usage-)

## Features 
- **Get Weather data by location and by coordination**
- **Caching (Redis)**

## Requirements 
- **python 3.x**
- **requests**
- **Redis**

## Installation
1. **Create a venv**
    ```bash
    python -m venv .venv
    ```
    for more information visit [python virtual environments](https://docs.python.org/3/tutorial/venv.html)
2. **Clone the repository:**
   ```bash
   git clone https://github.com/MadnessCod/WeatherAPI.git
   ```
3. **Install requirements using poetry**
   ```bash
   pip install poetry
   ```
   ```bash
   poetry install
   ```
4. **create a local_settings.py**
   - create a local_settings.py file inside app folder
   - copy sample_settings.py file to local_settings.py 
   - get you API key from [VisualCrossing website](https://www.visualcrossing.com/)
   - paste it in local_settings.py
   

## Usage 
   ```bash
   cd app
   ```
1. **Get Weather Data by location**
   - commands: <span style="color: #2ecc71;">--location</span> or <span style="color: #2ecc71;">-l</span> 
   ```bash
   python main.py --location "City,Country"
   ```
   Example: ```python main.py --location "London,UK"```
2. **Get Weather Data by coordination**
   - commands: <span style="color: #2ecc71;">--latitude</span> or <span style="color: #2ecc71;">-la</span> 
   ```bash
   pyton main.py --latitude "38.9697,-77.385"
   ```
3. **specify date (optional)**
   - commands: <span style="color: #2ecc71;">--start</span> or <span style="color: #2ecc71;">-s</span> 
   - commands: <span style="color: #2ecc71;">--end</span> or <span style="color: #2ecc71;">-e</span>
   ```bash
   python main.py --location "London,UK" --start "2023-01-01" --end "2024-01-01"
   ```
