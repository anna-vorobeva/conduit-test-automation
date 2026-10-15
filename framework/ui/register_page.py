from playwright.sync_api import Page


class RegisterPage:
    path = "/register"

    def __init__(self, page: Page) -> None:
        self.page = page
        self.username = page.get_by_placeholder("Username")
        self.email = page.get_by_placeholder("Email")
        self.password = page.get_by_placeholder("Password")
        self.submit = page.get_by_role("button", name="Sign up")
        self.errors = page.locator(".error-messages")

    def open(self) -> "RegisterPage":
        self.page.goto(self.path)
        return self

    def register(self, username: str, email: str, password: str) -> None:
        self.username.fill(username)
        self.email.fill(email)
        self.password.fill(password)
        self.submit.click()
