import pytest
from playwright.sync_api import Page, expect


@pytest.mark.smoke
def test_home_page_shows_global_feed(page: Page):
    page.goto("/")

    expect(page).to_have_title("Conduit")
    expect(page.get_by_text("Global Feed")).to_be_visible()
