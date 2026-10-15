from uuid import uuid4

import httpx
import pytest

from framework.config import Settings


@pytest.fixture(scope="session")
def settings() -> Settings:
    return Settings()


@pytest.fixture
def registered_user(settings: Settings) -> dict:
    suffix = uuid4().hex[:8]
    user = {
        "username": f"user_{suffix}",
        "email": f"user_{suffix}@example.com",
        "password": "Secret-123",
    }
    response = httpx.post(f"{settings.api_base_url}/users", json={"user": user})
    response.raise_for_status()
    return user
