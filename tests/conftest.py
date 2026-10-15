import httpx
import pytest

from framework.config import Settings
from framework.factories import new_user


@pytest.fixture(scope="session")
def settings() -> Settings:
    return Settings()


@pytest.fixture
def registered_user(settings: Settings) -> dict:
    user = new_user()
    response = httpx.post(f"{settings.api_base_url}/users", json={"user": user})
    response.raise_for_status()
    user["token"] = response.json()["user"]["token"]
    return user
