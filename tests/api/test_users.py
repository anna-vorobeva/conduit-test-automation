from uuid import uuid4

import httpx


def test_register_user(settings):
    suffix = uuid4().hex[:8]
    payload = {
        "user": {
            "username": f"user_{suffix}",
            "email": f"user_{suffix}@example.com",
            "password": "Secret-123",
        }
    }

    response = httpx.post(f"{settings.api_base_url}/users", json=payload)

    assert response.status_code == 201, response.text
    assert response.json()["user"]["email"] == payload["user"]["email"]
