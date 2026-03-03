"""Localization key management tools."""

from __future__ import annotations

import json
from typing import Any

from tolgee_mcp.server import mcp
from tolgee_mcp.client import tolgee_client


@mcp.tool()
async def list_keys(
    project_id: int, page: int = 0, size: int = 20
) -> str:
    """List localization keys in a Tolgee project.

    Args:
        project_id: The numeric ID of the project.
        page: Page number (0-indexed, default 0).
        size: Number of keys per page (default 20).
    """
    params = {"page": page, "size": size}
    result = await tolgee_client.get(
        f"/v2/projects/{project_id}/keys", params=params
    )
    if isinstance(result, str):
        return result

    keys = tolgee_client.get_embedded(result, "keys")
    if not keys:
        return "No keys found in this project."

    lines = []
    for k in keys:
        ns = k.get("namespace", "")
        ns_str = f" [ns: {ns}]" if ns else ""
        tags = k.get("tags", [])
        tag_names = [t.get("name", "") for t in tags] if tags else []
        tag_str = f" tags: {', '.join(tag_names)}" if tag_names else ""
        lines.append(
            f"- `{k.get('name', '')}` (ID: {k.get('id')}){ns_str}{tag_str}"
        )

    page_info = tolgee_client.format_page_info(result)
    return f"Keys ({page_info}):\n" + "\n".join(lines)


@mcp.tool()
async def search_keys(project_id: int, search: str) -> str:
    """Search for localization keys by name in a Tolgee project.

    Args:
        project_id: The numeric ID of the project.
        search: Search query string to match against key names.
    """
    params = {"search": search}
    result = await tolgee_client.get(
        f"/v2/projects/{project_id}/keys/search", params=params
    )
    if isinstance(result, str):
        return result

    # The search endpoint may return different structures
    if isinstance(result, list):
        if not result:
            return f"No keys found matching '{search}'."
        return json.dumps(result, indent=2)

    keys = tolgee_client.get_embedded(result, "keys")
    if not keys:
        return f"No keys found matching '{search}'."

    lines = []
    for k in keys:
        lines.append(f"- `{k.get('name', '')}` (ID: {k.get('id')})")

    return f"Keys matching '{search}':\n" + "\n".join(lines)


@mcp.tool()
async def create_key(
    project_id: int,
    name: str,
    namespace: str | None = None,
    translations: dict[str, str] | None = None,
) -> str:
    """Create a new localization key in a Tolgee project.

    Args:
        project_id: The numeric ID of the project.
        name: The key name (e.g., "button.submit", "greeting.hello").
        namespace: Optional namespace for the key.
        translations: Optional dict mapping language tags to translation values (e.g., {"en": "Hello", "fr": "Bonjour"}).
    """
    body: dict[str, Any] = {"name": name}
    if namespace:
        body["namespace"] = namespace
    if translations:
        body["translations"] = translations

    result = await tolgee_client.post(
        f"/v2/projects/{project_id}/keys/create", body=body
    )
    if isinstance(result, str):
        return result

    return f"Key created successfully.\n{json.dumps(result, indent=2)}"


@mcp.tool()
async def update_key(project_id: int, key_id: int, name: str) -> str:
    """Update a localization key's name.

    Args:
        project_id: The numeric ID of the project.
        key_id: The numeric ID of the key to update.
        name: The new name for the key.
    """
    body = {"name": name}
    result = await tolgee_client.put(
        f"/v2/projects/{project_id}/keys/{key_id}", body=body
    )
    if isinstance(result, str):
        return result

    return f"Key updated successfully.\n{json.dumps(result, indent=2)}"


@mcp.tool()
async def delete_keys(project_id: int, key_ids: list[int]) -> str:
    """Delete one or more localization keys from a Tolgee project.

    Args:
        project_id: The numeric ID of the project.
        key_ids: List of key IDs to delete.
    """
    body = {"ids": key_ids}
    result = await tolgee_client.delete(
        f"/v2/projects/{project_id}/keys", body=body
    )
    if isinstance(result, str):
        return result

    return f"Deleted {len(key_ids)} key(s) successfully."


@mcp.tool()
async def import_keys(
    project_id: int,
    keys: list[dict[str, Any]],
) -> str:
    """Import localization keys with translations into a Tolgee project.

    Each key object should have a "name" field and a "translations" dict mapping language tags to values.

    Args:
        project_id: The numeric ID of the project.
        keys: List of key objects, each with "name" (str) and "translations" (dict of language_tag -> value).

    Example keys format:
        [{"name": "greeting", "translations": {"en": "Hello", "fr": "Bonjour"}}]
    """
    body = {"keys": keys}
    result = await tolgee_client.post(
        f"/v2/projects/{project_id}/keys/import", body=body
    )
    if isinstance(result, str):
        return result

    return f"Imported {len(keys)} key(s) successfully.\n{json.dumps(result, indent=2)}"
