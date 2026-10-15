import httpx


class ArticlesApi:
    def __init__(self, http: httpx.Client) -> None:
        self._http = http

    def create(self, article: dict) -> httpx.Response:
        return self._http.post("/articles", json={"article": article})
