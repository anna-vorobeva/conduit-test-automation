import pytest
from playwright.sync_api import Page, expect

from framework.ui.login_page import LoginPage


@pytest.mark.smoke
def test_login_via_form_shows_username_in_navbar(page: Page, registered_user):
    login_page = LoginPage(page).open()

    login_page.login(registered_user["email"], registered_user["password"])

    expect(page.get_by_role("link", name=registered_user["username"])).to_be_visible()


def test_login_with_wrong_password_shows_error(page: Page, registered_user):
    login_page = LoginPage(page).open()

    login_page.login(registered_user["email"], "wrong-password")

    expect(login_page.errors).to_have_text("credentials invalid")
    expect(page.get_by_role("button", name="Sign in")).to_be_visible()
