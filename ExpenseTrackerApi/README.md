# ExpenseTracker API (DJANGO) 

This project is created for the [roadmap.sh Expense Tracker API](https://roadmap.sh/projects/expense-tracker-api).

---

## Table of Content

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
  - [1. Create a Virtual Environment](#1-create-a-virtual-environment)
  - [2. Clone the Repository](#2-clone-the-repository)
  - [3. Install Requirements](#3-install-requirements)
  - [4. Configuration](#4-configuration)
  - [5. Migrations](#5-migrations)
  - [6. Run the Server](#6-run-the-server)
- [Usage](#usage)
  - [Authentication](#authentication)
    - [Register](#register)
    - [Login](#login)
  - [Expense Management](#expense-management)
  - [Get/Create Expenses](#listcreate-expenses)
  - [Update Expense](#update-expense)
  - [Delete expense](#delete-expense)

---

## Features

- **User Registration**: Register users and generate JWT tokens.
- **JWT Authentication**: Secure API endpoints with JWT tokens.
- **Expense Management**:
  - List and create expenses.
  - Filter expenses by date range or predefined periods.
  - Update and delete expenses.

---

## Requirements

- **Python 3.12**
- **Django 4.2**
- **Django Rest Framework 5.4.0**
---

## Installation

### 1. Create a Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # For Linux/macOS
# or
.venv\Scripts\activate     # For Windows
```
### 2. Clone the Repository

```bash
git clone https://github.com/MadnessCod/ExpenseTrackerAPI.git
cd ExpenseTrackerAPI
```

### 3. Install Requirements

#### Using Poetry:

```bash
pip install poetry
poetry install
```

#### Alternatively, using pip:

```bash
pip install -r requirements.txt
```

### 4. Configuration

- Create a `local_settings.py` file in the `ExpenseTrackerAPI` folder.
- Copy the contents of `sample_settings.py` into `local_settings.py`.
- Generate a secret key using the command below:
  ```bash
  python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
  ```
- Set the generated key to the `SECRET_KEY` variable in `local_settings.py`.

### 5. Migrations

Prepare the database with the following commands:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Run the Server

Start the development server:

```bash
python manage.py runserver
```

---

## Usage

### Authentication

#### Register
`POST /register/`

- Registers a new user and returns a refresh token and access token.

**Request Body:**
```json
{
  "username": "<USERNAME>",
  "email": "user@example.com",
  "password": "<PASSWORD>"
}
```

**Response:**
```json
{
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}
```

#### Login
`POST /login/`

- Login with username and password to get refresh token and access token.

**Request Body:**
```json
{
  "username": "<USERNAME>",
  "password": "<PASSWORD>"
}
```

**Response:**
```json
{
  "refresh": "<refresh_token",
  "access": "<access_token>"
}
```

### Expense Management

#### List/Create Expenses
`GET /expenses/`

- Retrieves the list of expenses for the authenticated user. Supports filtering.

**Query Parameters:**
- `date_filter`: Filter expenses based on predefined periods. Options: `last_week`, `last_month`, `last_three_month`.
- `start_date` and `end_date`: Filter expenses within a specific date range.

**Response:**
```json
[
  {
    "id": 1,
    "name": "<NAME>",
    "description": "<DESCRIPTION>",
    "amount": 50.0,
    "category" : "GROCERIES"
  },
  {
    "id": 2,
    "name": "<NAME>",
    "description": "Transport",
    "amount": 25.0,
    "category": "OTHERS"
  }
]
```

`POST /expenses/`

- Creates a new expense for the authenticated user.

**Request Body:**
```json
{
  "name": "Electric bill",
  "description": "<DESCRIPTION>",
  "amount": 100.0,
  "category": "UTILITIES"
}
```

**Response:**
```json
{
  "id": 3,
  "name": "Electric bill",
  "description": "<DESCRIPTION>",
  "amount": 100.0,
  "category": "UTILITIES"
}
```

#### Update Expense
`PUT /expenses/<id>/update/`

- Partially updates an expense by ID.

**Request Body:**
```json
{
  "description": "Updated Description"
}
```

**Response:**
```json
{
  "id": 3,
  "name": "Electric bill",
  "description": "Updated Description",
  "amount": 100.0,
  "category": "UTILITIES"
}
```

#### Delete Expense
`DELETE /expenses/<id>/delete/`

- Deletes an expense by ID.

**Response:**
```
204 No Content
```

---

## Testing
This project includes unit tests to ensure functionality. To run the tests, follow these steps:

1. Make sure you have the required dependencies installed.
2. Run the tests using the following command:

```bash
python manage.py test
```

```markdown
This project has been tested manually for all described functionalities.
```

---

### Contributing

Feel free to open issues or submit pull requests to enhance this project.

---
