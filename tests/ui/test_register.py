from playwright.sync_api import Page, expect

from framework.factories import new_user
from framework.ui.register_page import RegisterPage


def test_sign_up_is_disabled_until_all_fields_are_filled(page: Page):
    user = new_user()
    register = RegisterPage(page).open()
    expect(register.submit).to_be_disabled()

    register.username.fill(user["username"])
    register.email.fill(user["email"])
    expect(register.submit).to_be_disabled()

    register.password.fill(user["password"])
    expect(register.submit).to_be_enabled()


def test_register_with_taken_email_shows_error(page: Page, registered_user: dict):
    user = new_user()
    register = RegisterPage(page).open()

    register.register(user["username"], registered_user["email"], user["password"])

    expect(register.errors).to_have_text("email has already been taken")
