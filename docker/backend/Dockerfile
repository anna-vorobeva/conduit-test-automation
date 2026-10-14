# Conduit backend: Django Ninja reference implementation pinned to a known-good commit.
FROM python:3.12-slim-bookworm

ARG BACKEND_REPO=https://github.com/c4ffein/realworld-django-ninja.git
ARG BACKEND_REF=04ef47ced437ee8795a13bdcbc2eff2be19e33bd

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# git: fetch the pinned commit; gcc + libc6-dev + libpq-dev: build psycopg2 from source
RUN apt-get update \
    && apt-get install -y --no-install-recommends git gcc libc6-dev libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN git init -q . \
    && git fetch -q --depth 1 "$BACKEND_REPO" "$BACKEND_REF" \
    && git checkout -q FETCH_HEAD \
    && rm -rf .git

# jwtninja is unpinned upstream; 0.4.0 is the version upstream CI was green with at this commit
RUN pip install --no-cache-dir . "jwtninja==0.4.0"

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate --no-input && python manage.py runserver 0.0.0.0:8000"]
