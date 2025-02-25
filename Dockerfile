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
    cp ExpenseTrackerAPI/sample_settings.py ExpenseTrackerAPI/local_settings.py && \
    sed -i "s/SECRET_KEY = ''/SECRET_KEY = '$(cat secret_key.txt)'/" ExpenseTrackerAPI/local_settings.py && \
    sed -i "s/DEBUG = False/DEBUG = True/" ExpenseTrackerAPI/local_settings.py && \
    rm secret_key.txt
RUN poetry run python manage.py makemigrations && \
    poetry run python manage.py migrate
RUN useradd --create-home --shell /bin/bash app
USER app
EXPOSE 8000
CMD ["poetry", "run", "python", "manage.py", "runserver"]
