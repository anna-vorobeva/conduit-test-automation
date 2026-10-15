from playwright.sync_api import Page


class ArticlePage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.title = page.locator(".banner h1")
        self.tags = page.locator(".article-content .tag-pill")
