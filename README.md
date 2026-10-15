# Conduit Test Automation

[![CI](https://github.com/anna-vorobeva/conduit-test-automation/actions/workflows/ci.yml/badge.svg)](https://github.com/anna-vorobeva/conduit-test-automation/actions/workflows/ci.yml)
[![Allure report](https://img.shields.io/badge/Allure-live%20report-orange)](https://anna-vorobeva.github.io/conduit-test-automation/)

API and UI test automation framework for [Conduit](https://realworld-docs.netlify.app/), the RealWorld "Medium clone", written in Python.
Every push runs the suite in GitHub Actions against a stand built with Docker Compose and publishes an [Allure report](https://anna-vorobeva.github.io/conduit-test-automation/) with run history.

**Stack:** Python 3.12 · Pytest · httpx · Pydantic · Playwright · PostgreSQL (psycopg) · Allure · pytest-xdist · uv · ruff · pre-commit · Docker Compose · GitHub Actions

## What is tested

The system under test is a pinned build of the official RealWorld stack: the Angular frontend served by nginx and the Django Ninja backend on PostgreSQL (see [`docker/`](docker/) and [`docker-compose.yml`](docker-compose.yml)).

| Layer | Tests | Covers |
| --- | --- | --- |
| API, [`tests/api`](tests/api) | 16 | registration, login, article CRUD, comments, follow/unfollow, negative cases with exact error bodies, response contracts validated with Pydantic, 3 checks that read PostgreSQL directly after API calls |
| UI, [`tests/ui`](tests/ui) | 10 | login form, registration form validation, article editor (create and edit), comments, global feed, tag filter |

Markers: `smoke` (8 critical-path tests), `regression` (everything else), `api`, `ui`.

## Quick start

Requirements: Docker Desktop, Python 3.12, [uv](https://docs.astral.sh/uv/).

```bash
cp .env.example .env                           # addresses and database credentials of the local stand
docker compose up -d --build --wait            # PostgreSQL + backend + frontend; the first build takes a few minutes
uv sync && uv run playwright install chromium  # dependencies and the browser
uv run pytest -n auto                          # the whole suite in parallel, about 15 seconds
```

Useful variations:

```bash
uv run pytest -m smoke             # critical path only
uv run pytest -m ui --headed       # watch the browser
allure serve allure-results        # open the report locally (needs Allure CLI and Java)
docker compose down                # stop the stand; the next `up` starts with an empty database
```

## Framework layout

```text
framework/                  shared toolbox, no test logic inside
├── config.py               Settings: reads .env (pydantic-settings); the only source of URLs and credentials
├── factories.py            new_user(), new_article(), new_comment(): unique, realistic data (Faker + uuid)
├── models.py               Pydantic models of API responses; strict, an unknown field fails the test
├── db.py                   read-only PostgreSQL access to verify what the API actually persisted
├── api/                    httpx client: ConduitApi with users, articles, comments, profiles, tags
│   └── reporting.py        httpx hook: every request and response goes to Allure, secrets masked
└── ui/                     Playwright page objects: LoginPage, RegisterPage, HomePage, EditorPage, ArticlePage
    └── network.py          blocks third-party requests (icon CDN, Google fonts) in every browser context

tests/
├── conftest.py             fixtures: settings, api, user_api, registered_user, another_user, article, db
├── api/                    one file per API resource
└── ui/                     one file per page; conftest.py adds user_page, a browser signed in via API token

docker/                     Dockerfiles of the stand: backend (Django Ninja), frontend (Angular + nginx)
.github/workflows/ci.yml    lint → tests on the compose stand → Allure report to GitHub Pages
```

### How a test goes through the layers

`test_create_article` asks for `user_api`, and pytest builds the chain: `settings` reads `.env`,
`api` creates an anonymous client, `registered_user` takes `new_user()` and registers it through the API,
`user_api` is a client that carries this user's token. The test then calls `user_api.articles.create(new_article())`,
validates the response with `Article.model_validate(...)` and asserts on typed fields.

UI tests follow the same idea: `user_page` puts the API token into the browser's localStorage,
so the browser starts already signed in and the test exercises only the page under test.
