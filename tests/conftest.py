import pytest

from framework.api import ConduitApi
from framework.config import Settings
from framework.db import ConduitDb
from framework.factories import new_article, new_user


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Every test gets its layer marker (api/ui) from its folder; non-smoke tests are regression."""
    for item in items:
        layer = item.path.parent.name
        if layer in ("api", "ui"):
            item.add_marker(layer)
        if "smoke" not in item.keywords:
            item.add_marker("regression")


@pytest.fixture(scope="session")
def settings() -> Settings:
    return Settings()


@pytest.fixture(scope="session")
def db(settings: Settings) -> ConduitDb:
    database = ConduitDb(settings.database_dsn)
    yield database
    database.close()


@pytest.fixture(scope="session")
def api(settings: Settings) -> ConduitApi:
    """Anonymous client: no token."""
    client = ConduitApi(settings.api_base_url)
    yield client
    client.close()


def register(api: ConduitApi) -> dict:
    """Register a brand-new user and return their credentials together with the token."""
    user = new_user()
    response = api.users.register(user)
    response.raise_for_status()
    user["token"] = response.json()["user"]["token"]
    return user


@pytest.fixture
def registered_user(api: ConduitApi) -> dict:
    return register(api)


@pytest.fixture
def another_user(api: ConduitApi) -> dict:
    """A second user, for scenarios between two people (follow, someone else's article)."""
    return register(api)


@pytest.fixture
def user_api(settings: Settings, registered_user: dict) -> ConduitApi:
    """Client acting as the freshly registered user."""
    client = ConduitApi(settings.api_base_url, token=registered_user["token"])
    yield client
    client.close()


@pytest.fixture
def article(user_api: ConduitApi) -> dict:
    """An article freshly created by the registered user."""
    response = user_api.articles.create(new_article())
    response.raise_for_status()
    return response.json()["article"]


@pytest.fixture(scope="session")
def base_url(settings: Settings) -> str:
    """Tells pytest-playwright where the UI lives, so tests can call page.goto("/")."""
    return settings.ui_base_url
