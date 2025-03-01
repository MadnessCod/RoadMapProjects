## Blogging API (Django)

#### This project is created for the roadmap.sh [Blogging Platform API project](https://roadmap.sh/projects/blogging-platform-api).

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)

## Features

- Create a post
- Get all posts
- Get a post with a specific ID
- Search posts by term (title, content, or category)
- Update a post
- Delete a post

## Requirements

- **Python 3.x**
- **Django 4.2**

## Installation

### 1. Create a Virtual Environment

```bash
python -m venv .venv
```

For more information, visit [Python virtual environments](https://docs.python.org/3/tutorial/venv.html).

### 2. Clone the Repository

```bash
git clone https://github.com/MadnessCod/PersonalBlog_REST.git
cd PersonalBlog_REST
```

### 3. Install Requirements

Using Poetry:

```bash
pip install poetry
poetry install
```

Alternatively, using pip:

```bash
pip install django==4.2
```

### 4. Configuration

- Create a `local_settings.py` file inside the `RESTBlog` folder.
- Copy the contents of `sample_settings.py` into `local_settings.py`.
- Generate a secret key:
  ```bash
  python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
  ```
- Assign the generated secret key to the `SECRET_KEY` variable in `local_settings.py`.

### 5. Migrations

Run the following commands to prepare the database:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Run the Server

Start the development server:

```bash
python manage.py runserver
```

## Usage

### Create a Post

If in development, replace the `@ensure_csrf_cookie` decorator with `@csrf_exempt`.

#### Example Request:

```http
POST http://localhost:8000/posts/

{
  "title": "Sample Title",
  "content": "Sample Content",
  "tags": ["Tag1", "Tag2"],
  "category": "Sample Category"
}
```

---

### Get All Posts

#### Example Request:

```http
GET http://localhost:8000/posts/
```

---

### Get a Post by ID

#### Example Request:

```http
GET http://localhost:8000/posts/{id_number}/
```

---

### Search Posts by Term

Search for posts with a specific term in their title, content, or category.

#### Example Request:

```http
GET http://localhost:8000/posts?term=search_term
```

---

### Update a Post

You can update any combination of `title`, `content`, `tags`, or `category`.

#### Example Request:

```http
PUT http://localhost:8000/posts/{id_number}/

{
  "title": "Updated Title",
  "category": "Updated Category"
}
```

---

### Delete a Post

#### Example Request:

```http
DELETE http://localhost:8000/posts/{id_number}/
```


