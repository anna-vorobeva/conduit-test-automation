import re

from playwright.sync_api import Page, expect

from framework.factories import new_article, new_comment
from framework.ui.article_page import ArticlePage
from framework.ui.editor_page import EditorPage


def test_edit_article_title(user_page: Page, article: dict):
    new_title = new_article()["title"]
    article_page = ArticlePage(user_page).open(article["slug"])
    article_page.edit_link.click()
    expect(user_page).to_have_url(re.compile(r"/editor/"))

    editor = EditorPage(user_page)
    expect(editor.title).to_have_value(article["title"])
    editor.title.fill(new_title)
    editor.publish.click()

    expect(user_page).to_have_url(re.compile(r"/article/"))
    expect(article_page.title).to_have_text(new_title)


def test_add_comment(user_page: Page, article: dict):
    comment = new_comment()
    article_page = ArticlePage(user_page).open(article["slug"])

    article_page.add_comment(comment["body"])

    expect(article_page.comments).to_have_count(1)
    expect(article_page.comments.first).to_have_text(comment["body"])
