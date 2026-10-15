from playwright.sync_api import Page


class LoginPage:
    path = "/login"

    def __init__(self, page: Page) -> None:
        self.page = page
        self.email = page.get_by_placeholder("Email")
        self.password = page.get_by_placeholder("Password")
        self.submit = page.get_by_role("button", name="Sign in")
        self.errors = page.locator(".error-messages")

    def open(self) -> "LoginPage":
        self.page.goto(self.path)
        return self

    def login(self, email: str, password: str) -> None:
        self.email.fill(email)
        self.password.fill(password)
        self.submit.click()
