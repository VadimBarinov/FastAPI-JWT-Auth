FROM python:3

WORKDIR /api

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./app/ ./app/
COPY poetry.lock .
COPY pyproject.toml .
COPY README.md .
COPY .env .

RUN pip install poetry
RUN poetry install

RUN mkdir certs
WORKDIR certs
RUN openssl genrsa -out jwt-private.pem 2048
RUN openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem

WORKDIR /api