import pytest
from playwright.sync_api import Page

from framework.config import Settings


@pytest.fixture
def user_page(new_context, settings: Settings, registered_user: dict) -> Page:
    """A page already signed in as registered_user: the API token is put into localStorage."""
    storage_state = {
        "cookies": [],
        "origins": [
            {
                "origin": settings.ui_base_url,
                "localStorage": [{"name": "jwtToken", "value": registered_user["token"]}],
            }
        ],
    }
    context = new_context(storage_state=storage_state)
    return context.new_page()
