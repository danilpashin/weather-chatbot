FROM python:3.12-alpine AS builder
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app
WORKDIR /app

RUN python -m venv /app/venv

COPY requirements.txt .
RUN /app/venv/bin/pip install --no-cache-dir -r requirements.txt

FROM python:3.12-alpine

WORKDIR /app

RUN apk add --no-cache \
    postgresql-client \
    bash

COPY --from=builder /app/venv /app/venv
COPY . .

ENV PATH="/app/venv/bin:$PATH"