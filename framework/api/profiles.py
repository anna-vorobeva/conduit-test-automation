import httpx


class ProfilesApi:
    def __init__(self, http: httpx.Client) -> None:
        self._http = http

    def get(self, username: str) -> httpx.Response:
        return self._http.get(f"/profiles/{username}")

    def follow(self, username: str) -> httpx.Response:
        return self._http.post(f"/profiles/{username}/follow")

    def unfollow(self, username: str) -> httpx.Response:
        return self._http.delete(f"/profiles/{username}/follow")
