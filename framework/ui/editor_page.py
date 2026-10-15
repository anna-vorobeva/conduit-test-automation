from playwright.sync_api import Page


class EditorPage:
    path = "/editor"

    def __init__(self, page: Page) -> None:
        self.page = page
        self.title = page.get_by_placeholder("Article Title")
        self.description = page.get_by_placeholder("What's this article about?")
        self.body = page.get_by_placeholder("Write your article (in markdown)")
        self.tags = page.get_by_placeholder("Enter tags")
        self.publish = page.get_by_role("button", name="Publish Article")

    def open(self) -> "EditorPage":
        self.page.goto(self.path)
        return self

    def publish_article(self, article: dict) -> None:
        self.title.fill(article["title"])
        self.description.fill(article["description"])
        self.body.fill(article["body"])
        for tag in article["tagList"]:
            self.tags.fill(tag)
            self.tags.press("Enter")
        self.publish.click()
