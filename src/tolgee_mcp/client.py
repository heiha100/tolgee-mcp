"""Tolgee API HTTP client."""

from __future__ import annotations

import json
import os
from typing import Any

import httpx


DEFAULT_API_URL = "https://app.tolgee.io"
REQUEST_TIMEOUT = 30.0


class TolgeeClient:
    """Async HTTP client for the Tolgee REST API."""

    def __init__(self) -> None:
        self.api_url = os.environ.get("TOLGEE_API_URL", DEFAULT_API_URL).rstrip("/")
        self.api_key = os.environ.get("TOLGEE_API_KEY", "")
        self._client: httpx.AsyncClient | None = None

    @property
    def is_configured(self) -> bool:
        return bool(self.api_key)

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=self.api_url,
                headers={
                    "X-API-Key": self.api_key,
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                },
                timeout=REQUEST_TIMEOUT,
            )
        return self._client

    async def close(self) -> None:
        if self._client and not self._client.is_closed:
            await self._client.aclose()

    # ── Request methods ──────────────────────────────────────────────

    async def get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any] | list[Any] | str:
        """Send a GET request and return parsed JSON or error string."""
        return await self._request("GET", path, params=params)

    async def post(self, path: str, body: Any = None, params: dict[str, Any] | None = None) -> dict[str, Any] | list[Any] | str:
        """Send a POST request and return parsed JSON or error string."""
        return await self._request("POST", path, body=body, params=params)

    async def put(self, path: str, body: Any = None) -> dict[str, Any] | list[Any] | str:
        """Send a PUT request and return parsed JSON or error string."""
        return await self._request("PUT", path, body=body)

    async def delete(self, path: str, body: Any = None) -> dict[str, Any] | list[Any] | str:
        """Send a DELETE request and return parsed JSON or error string."""
        return await self._request("DELETE", path, body=body)

    async def post_raw(self, path: str, body: Any = None, params: dict[str, Any] | None = None) -> httpx.Response | str:
        """Send a POST request and return the raw response (for binary data like exports)."""
        if not self.is_configured:
            return "Error: TOLGEE_API_KEY is not configured. Set the TOLGEE_API_KEY environment variable."
        try:
            client = await self._get_client()
            response = await client.post(path, json=body, params=params)
            response.raise_for_status()
            return response
        except httpx.TimeoutException:
            return f"Error: Request to {path} timed out after {REQUEST_TIMEOUT}s."
        except httpx.HTTPStatusError as exc:
            return _format_http_error(exc)
        except httpx.HTTPError as exc:
            return f"Error: HTTP request failed: {exc}"

    async def _request(
        self,
        method: str,
        path: str,
        body: Any = None,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any] | list[Any] | str:
        if not self.is_configured:
            return "Error: TOLGEE_API_KEY is not configured. Set the TOLGEE_API_KEY environment variable."
        try:
            client = await self._get_client()
            kwargs: dict[str, Any] = {}
            if body is not None:
                kwargs["json"] = body
            if params is not None:
                kwargs["params"] = params
            response = await client.request(method, path, **kwargs)
            response.raise_for_status()
            if not response.content:
                return {"success": True}
            return response.json()
        except httpx.TimeoutException:
            return f"Error: Request to {path} timed out after {REQUEST_TIMEOUT}s."
        except httpx.HTTPStatusError as exc:
            return _format_http_error(exc)
        except httpx.HTTPError as exc:
            return f"Error: HTTP request failed: {exc}"

    # ── Pagination helpers ───────────────────────────────────────────

    @staticmethod
    def format_page_info(data: dict[str, Any] | list[Any] | str) -> str:
        """Extract pagination info from a Tolgee paginated response."""
        if not isinstance(data, dict):
            return ""
        page_info = data.get("page", {})
        total_elements = page_info.get("totalElements", "?")
        total_pages = page_info.get("totalPages", "?")
        current_page = page_info.get("number", "?")
        size = page_info.get("size", "?")
        return f"Page {current_page}/{total_pages} (total: {total_elements}, page size: {size})"

    @staticmethod
    def get_embedded(data: dict[str, Any] | list[Any] | str, key: str) -> list[dict[str, Any]]:
        """Extract items from a Tolgee paginated response's _embedded field."""
        if not isinstance(data, dict):
            return []
        embedded = data.get("_embedded", {})
        return embedded.get(key, [])


def _format_http_error(exc: httpx.HTTPStatusError) -> str:
    """Format an HTTP error into a human-readable string."""
    status = exc.response.status_code
    try:
        body = exc.response.json()
        if isinstance(body, dict):
            message = body.get("message", body.get("error", json.dumps(body)))
        else:
            message = str(body)
    except Exception:
        message = exc.response.text[:500] if exc.response.text else "No response body"
    return f"Error {status}: {message}"


# Module-level singleton
tolgee_client = TolgeeClient()
