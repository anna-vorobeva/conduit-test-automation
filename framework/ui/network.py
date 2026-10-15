from urllib.parse import urlparse

from playwright.sync_api import BrowserContext


def block_third_party_requests(context: BrowserContext, allowed_host: str) -> None:
    """Abort requests to any host but the stand (icon CDN, Google fonts).

    Tests must not depend on the internet, and page.goto must not wait for it.
    """
    context.route(
        lambda url: urlparse(url).hostname != allowed_host,
        lambda route: route.abort(),
    )
