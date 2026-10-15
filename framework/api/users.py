import httpx


class UsersApi:
    def __init__(self, http: httpx.Client) -> None:
        self._http = http

    def register(self, user: dict) -> httpx.Response:
        return self._http.post("/users", json={"user": user})

    def login(self, email: str, password: str) -> httpx.Response:
        credentials = {"email": email, "password": password}
        return self._http.post("/users/login", json={"user": credentials})
