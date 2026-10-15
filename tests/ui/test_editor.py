import re

from playwright.sync_api import Page, expect

from framework.factories import new_article
from framework.ui.article_page import ArticlePage
from framework.ui.editor_page import EditorPage


def test_create_article_via_editor(user_page: Page):
    article = new_article()
    editor = EditorPage(user_page).open()

    editor.publish_article(article)

    expect(user_page).to_have_url(re.compile(r"/article/"))
    article_page = ArticlePage(user_page)
    expect(article_page.title).to_have_text(article["title"])
    expect(article_page.tags).to_have_text(sorted(article["tagList"]))
