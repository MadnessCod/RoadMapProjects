FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.8.4 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"
RUN poetry --version
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --no-dev
COPY . .
RUN poetry run python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())" > secret_key.txt && \
    cp TodoListAPI/sample_settings.py TodoListAPI/local_settings.py && \
    sed -i "s/SECRET_KEY = ''/SECRET_KEY = '$(cat secret_key.txt)'/" TodoListAPI/local_settings.py && \
    sed -i "s/DEBUG = False/DEBUG = True/" TodoListAPI/local_settings.py && \
    rm secret_key.txt
RUN poetry run python manage.py makemigrations && \
    poetry run python manage.py migrate
EXPOSE 8000
CMD ["poetry", "run", "python", "manage.py", "runserver"]