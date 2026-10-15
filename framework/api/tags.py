import httpx


class TagsApi:
    def __init__(self, http: httpx.Client) -> None:
        self._http = http

    def list(self) -> httpx.Response:
        return self._http.get("/tags")
