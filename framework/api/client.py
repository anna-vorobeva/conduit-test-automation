import httpx

from framework.api.articles import ArticlesApi
from framework.api.comments import CommentsApi
from framework.api.profiles import ProfilesApi
from framework.api.reporting import attach_to_allure
from framework.api.tags import TagsApi
from framework.api.users import UsersApi


class ConduitApi:
    """HTTP client for the Conduit API. Knows the base URL and, if given, the user's token."""

    def __init__(self, base_url: str, token: str | None = None) -> None:
        headers = {"Authorization": f"Token {token}"} if token else {}
        self._http = httpx.Client(
            base_url=base_url, headers=headers, event_hooks={"response": [attach_to_allure]}
        )
        self.users = UsersApi(self._http)
        self.articles = ArticlesApi(self._http)
        self.comments = CommentsApi(self._http)
        self.profiles = ProfilesApi(self._http)
        self.tags = TagsApi(self._http)

    def close(self) -> None:
        self._http.close()
