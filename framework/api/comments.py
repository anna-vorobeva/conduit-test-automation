import httpx


class CommentsApi:
    def __init__(self, http: httpx.Client) -> None:
        self._http = http

    def add(self, slug: str, comment: dict) -> httpx.Response:
        return self._http.post(f"/articles/{slug}/comments", json={"comment": comment})

    def list(self, slug: str) -> httpx.Response:
        return self._http.get(f"/articles/{slug}/comments")

    def delete(self, slug: str, comment_id: int) -> httpx.Response:
        return self._http.delete(f"/articles/{slug}/comments/{comment_id}")
