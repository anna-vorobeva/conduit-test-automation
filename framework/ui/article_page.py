from playwright.sync_api import Page


class ArticlePage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.title = page.locator(".banner h1")
        self.tags = page.locator(".article-content .tag-pill")
        # the page renders the same actions twice (banner and footer), so take the first
        self.edit_link = page.get_by_role("link", name="Edit Article").first
        self.comment_field = page.get_by_placeholder("Write a comment...")
        self.post_comment = page.get_by_role("button", name="Post Comment")
        self.comments = page.locator("app-article-comment .card-text")

    def open(self, slug: str) -> "ArticlePage":
        self.page.goto(f"/article/{slug}")
        return self

    def add_comment(self, text: str) -> None:
        self.comment_field.fill(text)
        self.post_comment.click()
