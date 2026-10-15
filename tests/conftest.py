import pytest

from framework.api import ConduitApi
from framework.config import Settings
from framework.factories import new_user


@pytest.fixture(scope="session")
def settings() -> Settings:
    return Settings()


@pytest.fixture(scope="session")
def api(settings: Settings) -> ConduitApi:
    """Anonymous client: no token."""
    client = ConduitApi(settings.api_base_url)
    yield client
    client.close()


@pytest.fixture
def registered_user(api: ConduitApi) -> dict:
    user = new_user()
    response = api.users.register(user)
    response.raise_for_status()
    user["token"] = response.json()["user"]["token"]
    return user


@pytest.fixture
def user_api(settings: Settings, registered_user: dict) -> ConduitApi:
    """Client acting as the freshly registered user."""
    client = ConduitApi(settings.api_base_url, token=registered_user["token"])
    yield client
    client.close()
