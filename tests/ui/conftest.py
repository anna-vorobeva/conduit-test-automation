from urllib.parse import urlparse

import pytest
from playwright.sync_api import BrowserContext, Page

from framework.config import Settings
from framework.ui.network import block_third_party_requests


@pytest.fixture
def context(context: BrowserContext, settings: Settings) -> BrowserContext:
    """pytest-playwright's default context, restricted to the stand's host."""
    block_third_party_requests(context, urlparse(settings.ui_base_url).hostname)
    return context


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
    block_third_party_requests(context, urlparse(settings.ui_base_url).hostname)
    return context.new_page()
