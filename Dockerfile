FROM python:3.10-slim AS base

RUN apt-get update && apt-get install -y libpq-dev gcc

WORKDIR /app

COPY pyproject.toml /app/pyproject.toml

RUN pip install --upgrade pip \
  && pip install poetry \
  && poetry config virtualenvs.create false \
  && poetry install

COPY . /app/

ENV PYTHONPATH=/app