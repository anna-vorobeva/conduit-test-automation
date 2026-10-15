import re

from playwright.sync_api import Page, expect

from framework.ui.home_page import HomePage


def test_new_article_appears_in_global_feed(page: Page, article: dict):
    home = HomePage(page).open()

    expect(home.article_preview(article["title"])).to_be_visible()


def test_filter_articles_by_tag(page: Page, article: dict):
    tag = article["tagList"][0]
    home = HomePage(page).open()

    home.filter_by_tag(tag)

    expect(home.feed_tabs.filter(has_text=tag)).to_have_class(re.compile("active"))
    expect(home.article_preview(article["title"])).to_be_visible()
    without_tag = home.article_previews.filter(has_not=page.get_by_text(tag, exact=True))
    expect(without_tag).to_have_count(0)
