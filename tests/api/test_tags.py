import httpx


def test_tags_endpoint_is_reachable(settings):
    response = httpx.get(f"{settings.api_base_url}/tags")

    assert response.status_code == 200
    assert isinstance(response.json()["tags"], list)
