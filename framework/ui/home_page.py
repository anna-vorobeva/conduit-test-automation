from playwright.sync_api import Locator, Page


class HomePage:
    path = "/"

    def __init__(self, page: Page) -> None:
        self.page = page
        self.feed_tabs = page.locator(".feed-toggle .nav-link")
        self.article_previews = page.locator(".article-preview")
        self.sidebar = page.locator(".sidebar")

    def open(self) -> "HomePage":
        self.page.goto(self.path)
        return self

    def article_preview(self, title: str) -> Locator:
        return self.article_previews.filter(has=self.page.get_by_role("heading", name=title))

    def filter_by_tag(self, tag: str) -> None:
        self.sidebar.get_by_role("link", name=tag, exact=True).click()
