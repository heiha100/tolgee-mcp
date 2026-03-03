"""Export and import tools."""

from __future__ import annotations

import json
from typing import Any

from tolgee_mcp.server import mcp
from tolgee_mcp.client import tolgee_client


@mcp.tool()
async def export_translations(
    project_id: int,
    format: str = "JSON",
    languages: list[str] | None = None,
    filter_namespace: str | None = None,
) -> str:
    """Export translations from a Tolgee project.

    Args:
        project_id: The numeric ID of the project.
        format: Export format. Supported: "JSON" (default), "XLIFF", "PO", "APPLE_STRINGS_STRINGSDICT", "ANDROID_XML", "FLUTTER_ARB", "PROPERTIES", "YAML_RUBY".
        languages: Optional list of language tags to export (e.g., ["en", "fr"]). Exports all languages if not specified.
        filter_namespace: Optional namespace to filter exported keys.
    """
    body: dict[str, Any] = {"format": format, "zip": False}
    if languages:
        body["languages"] = languages
    if filter_namespace:
        body["filterNamespace"] = [filter_namespace]

    response = await tolgee_client.post_raw(
        f"/v2/projects/{project_id}/export", body=body
    )
    if isinstance(response, str):
        return response

    # For non-zip export, response is the translation content directly
    content_type = response.headers.get("content-type", "")
    if "application/json" in content_type:
        try:
            data = response.json()
            return json.dumps(data, indent=2, ensure_ascii=False)
        except Exception:
            return response.text
    elif "application/zip" in content_type or "application/octet-stream" in content_type:
        return (
            f"Export completed. Response is binary data ({len(response.content)} bytes). "
            f"For file exports, use the Tolgee UI or CLI. "
            f"Set format to JSON for inline results."
        )
    else:
        return response.text


@mcp.tool()
async def import_translations(
    project_id: int,
    keys: list[dict[str, Any]],
) -> str:
    """Import translations into a Tolgee project using single-step import.

    Each key object should have a "name" and "translations" mapping language tags to values.

    Args:
        project_id: The numeric ID of the project.
        keys: List of key objects with "name" (str) and "translations" (dict of language_tag -> value).

    Example:
        [{"name": "hello", "translations": {"en": "Hello", "de": "Hallo"}}]
    """
    body = {"keys": keys}
    result = await tolgee_client.post(
        f"/v2/projects/{project_id}/keys/import-resolvable", body=body
    )
    if isinstance(result, str):
        return result

    return f"Imported {len(keys)} key(s) successfully.\n{json.dumps(result, indent=2)}"
