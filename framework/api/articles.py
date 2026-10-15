import httpx


class ArticlesApi:
    def __init__(self, http: httpx.Client) -> None:
        self._http = http

    def create(self, article: dict) -> httpx.Response:
        return self._http.post("/articles", json={"article": article})

    def get(self, slug: str) -> httpx.Response:
        return self._http.get(f"/articles/{slug}")

    def update(self, slug: str, changes: dict) -> httpx.Response:
        return self._http.put(f"/articles/{slug}", json={"article": changes})

    def delete(self, slug: str) -> httpx.Response:
        return self._http.delete(f"/articles/{slug}")
