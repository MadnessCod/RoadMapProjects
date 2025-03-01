FROM python:3.12-slim AS python-base
ENV POETRY_VERSION=1.8.4
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache
FROM python-base as poetry-base
RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==$POETRY_VERSION
FROM python-base as example-app
COPY --from=poetry-base ${POETRY_VENV} ${POETRY_VENV}
ENV PATH="${PATH}:${POETRY_VENV}/bin"
WORKDIR /app
COPY poetry.lock pyproject.toml README.md ./
RUN $POETRY_VENV/bin/poetry check
RUN $POETRY_VENV/bin/poetry install --no-interaction --no-cache
COPY .. /app
RUN poetry run python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())" > secret_key.txt && \
    cp TodoListAPI/sample_settings.py TodoListAPI/local_settings.py && \
    sed -i "s/SECRET_KEY = ''/SECRET_KEY = '$(cat secret_key.txt)'/" TodoListAPI/local_settings.py && \
    sed -i "s/DEBUG = False/DEBUG = True/" TodoListAPI/local_settings.py && \
    rm secret_key.txt
RUN $POETRY_VENV/bin/poetry run python manage.py makemigrations && \
    $POETRY_VENV/bin/poetry run python manage.py migrate
RUN useradd --create-home --shell /bin/bash app
USER app
EXPOSE 8000
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]