# TodoList API (DJANGO)

This project is created for the [roadmap.sh Todo List API Project](https://roadmap.sh/projects/todo-list-api).

---

## Table of Contents

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
  - [Register](#register)
  - [Login](#login)
  - [Add Todo](#add-todo)
  - [Update Todo](#update-todo)
  - [Get List of Todos](#get-list-of-todos)
    - [Get Todos by Dates](#get-todos-by-dates)
    - [Paginated Todos](#paginated-todos)
    - [Filter Todos by Category](#filter-todos-by-category)
  - [Delete a Todo](#delete-a-todo)
- [Testing](#testing)

---

## Features

- User registration with token generation.
- User login with token authentication.
- CRUD operations for managing todos:
  - Add a todo.
  - Update a todo.
  - Get a list of todos.
  - Delete a todo.
- Search and filter todos by:
  - Category.
  - Date range.
- Pagination for todos.
- Automatic token refresh.

---

## Requirements

- **Python 3.12**
- **Django 4.2**

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
git clone https://github.com/MadnessCod/TodoListAPI.git
cd TodoListAPI
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

- Create a `local_settings.py` file in the `TodoListAPI` folder.
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

### Register

Register a user. Upon success, you will receive a token. Use this token for authenticated endpoints.

#### Example Request

```http
POST http://localhost:8000/register/
Content-Type: application/json

{
    "name": "<NAME>",
    "email": "<EMAIL>",
    "password": "<PASSWORD>"
}
```

---

### Login

Log in to receive a token for accessing authenticated endpoints.

#### Example Request

```http
POST http://localhost:8000/login/
Content-Type: application/json

{
    "email": "<EMAIL>",
    "password": "<PASSWORD>"
}
```

---

### Add Todo

Add a new todo. Token authentication is required.

#### Example Request

```http
POST http://localhost:8000/todos/
Content-Type: application/json
Authorization: Bearer <your_token>

{
  "title": "<TITLE>",
  "description": "<DESCRIPTION>",
  "category": "<CATEGORY>"
}
```

---

### Update Todo

Update a todo. Token authentication is required. You can update any combination of `title`, `description`, or `category`.

#### Example Request

```http
PUT http://localhost:8000/todos/<todo_id>/
Content-Type: application/json
Authorization: Bearer <your_token>

{
  "title": "<TITLE>",
  "description": "<DESCRIPTION>",
  "category": "<CATEGORY>"
}
```

---

### Get List of Todos

Retrieve all todos. Token authentication is required.

#### Example Request

```http
GET http://localhost:8000/todos/
Content-Type: application/json
Authorization: Bearer <your_token>
```

---

#### Get Todos by Dates

Filter todos within a specific date range.

#### Example Request

```http
GET http://localhost:8000/todos/?start=YYYY-MM-DD&end=YYYY-MM-DD
Content-Type: application/json
Authorization: Bearer <your_token>
```

---

#### Paginated Todos

Retrieve todos with pagination.

#### Example Request

```http
GET http://localhost:8000/todos/?page=<page_number>&limit=<limit>
Content-Type: application/json
Authorization: Bearer <your_token>
```

---

#### Filter Todos by Category

Search todos by category.

#### Example Request

```http
GET http://localhost:8000/todos/?category=<category_name>
Content-Type: application/json
Authorization: Bearer <your_token>
```

---

### Delete a Todo

Delete a todo by its ID. Token authentication is required.

#### Example Request

```http
DELETE http://localhost:8000/todos/<todo_id>/
Content-Type: application/json
Authorization: Bearer <your_token>
```

---

### Notes

- For development, replace the `@ensure_csrf_cookie` decorator with `@csrf_exempt` as needed.
- Always ensure the token is included in the `Authorization` header in the format `Bearer <your_token>`.

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
