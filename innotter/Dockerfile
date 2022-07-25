# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION=1.1.13

WORKDIR /code

RUN pip install "poetry==$POETRY_VERSION"

COPY poetry.lock pyproject.toml /code/
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi


COPY . /code/
RUN chmod +x ./entrypoint.sh
RUN chmod +x ./run_celery.sh
