import json

import allure
import httpx

MASKED_FIELDS = {"password", "token"}


def attach_to_allure(response: httpx.Response) -> None:
    """httpx response hook: records every request and response as a step in the Allure report."""
    response.read()
    request = response.request
    with allure.step(f"{request.method} {request.url.path} -> {response.status_code}"):
        if request.content:
            allure.attach(_pretty(request.content), "request", allure.attachment_type.JSON)
        if response.content:
            allure.attach(_pretty(response.content), "response", allure.attachment_type.JSON)


def _pretty(raw: bytes) -> str:
    try:
        return json.dumps(_mask(json.loads(raw)), indent=2, ensure_ascii=False)
    except ValueError:
        return raw.decode(errors="replace")


def _mask(data):
    """Hide secrets so the published report never shows passwords or tokens."""
    if isinstance(data, dict):
        return {k: "***" if k in MASKED_FIELDS else _mask(v) for k, v in data.items()}
    if isinstance(data, list):
        return [_mask(item) for item in data]
    return data
