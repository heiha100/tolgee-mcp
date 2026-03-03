"""Translation management tools."""

from __future__ import annotations

import json

from tolgee_mcp.server import mcp
from tolgee_mcp.client import tolgee_client


@mcp.tool()
async def get_translations(
    project_id: int,
    languages: list[str] | None = None,
    page: int = 0,
    size: int = 20,
) -> str:
    """Get translations for keys in a Tolgee project.

    Args:
        project_id: The numeric ID of the project.
        languages: Optional list of language tags to filter by (e.g., ["en", "fr"]). If not specified, all languages are returned.
        page: Page number (0-indexed, default 0).
        size: Number of items per page (default 20).
    """
    params: dict[str, object] = {"page": page, "size": size}
    if languages:
        params["languages"] = ",".join(languages)

    result = await tolgee_client.get(
        f"/v2/projects/{project_id}/translations", params=params
    )
    if isinstance(result, str):
        return result

    keys = tolgee_client.get_embedded(result, "keys")
    if not keys:
        return "No translations found."

    lines = []
    for entry in keys:
        key_name = entry.get("keyName", entry.get("name", "?"))
        key_id = entry.get("keyId", entry.get("id", "?"))
        translations = entry.get("translations", {})
        trans_parts = []
        for lang_tag, trans_data in translations.items():
            if isinstance(trans_data, dict):
                text = trans_data.get("text", "")
                state = trans_data.get("state", "")
                trans_id = trans_data.get("id", "")
                trans_parts.append(
                    f"  - {lang_tag}: \"{text}\" [{state}] (translation ID: {trans_id})"
                )
            else:
                trans_parts.append(f"  - {lang_tag}: \"{trans_data}\"")
        trans_str = "\n".join(trans_parts) if trans_parts else "  (no translations)"
        lines.append(f"- `{key_name}` (key ID: {key_id}):\n{trans_str}")

    page_info = tolgee_client.format_page_info(result)
    return f"Translations ({page_info}):\n" + "\n".join(lines)


@mcp.tool()
async def set_translations(
    project_id: int,
    key_name: str,
    translations: dict[str, str],
) -> str:
    """Set translation values for an existing key in a Tolgee project.

    Args:
        project_id: The numeric ID of the project.
        key_name: The name of the existing key.
        translations: Dict mapping language tags to translation text values (e.g., {"en": "Hello", "fr": "Bonjour"}).
    """
    body = {
        "key": key_name,
        "translations": translations,
    }
    result = await tolgee_client.post(
        f"/v2/projects/{project_id}/translations", body=body
    )
    if isinstance(result, str):
        return result

    return f"Translations set successfully.\n{json.dumps(result, indent=2)}"


@mcp.tool()
async def create_or_update_translations(
    project_id: int,
    key_name: str,
    translations: dict[str, str],
    namespace: str | None = None,
) -> str:
    """Create a key if it doesn't exist and set its translations. If the key already exists, update its translations.

    Args:
        project_id: The numeric ID of the project.
        key_name: The key name.
        translations: Dict mapping language tags to translation text values.
        namespace: Optional namespace for the key.
    """
    body: dict[str, object] = {
        "key": key_name,
        "translations": translations,
    }
    if namespace:
        body["namespace"] = namespace

    result = await tolgee_client.post(
        f"/v2/projects/{project_id}/translations/createOrUpdate", body=body
    )
    if isinstance(result, str):
        return result

    return f"Translations created/updated successfully.\n{json.dumps(result, indent=2)}"


@mcp.tool()
async def set_translation_state(
    project_id: int,
    translation_id: int,
    state: str,
) -> str:
    """Set the state of a specific translation.

    Args:
        project_id: The numeric ID of the project.
        translation_id: The numeric ID of the translation (not the key ID).
        state: The new state. Valid values: "UNTRANSLATED", "TRANSLATED", "REVIEWED".
    """
    result = await tolgee_client.put(
        f"/v2/projects/{project_id}/translations/{translation_id}/set-state/{state}"
    )
    if isinstance(result, str):
        return result

    return f"Translation state set to {state}.\n{json.dumps(result, indent=2)}"


@mcp.tool()
async def get_translation_history(
    project_id: int, translation_id: int
) -> str:
    """Get the modification history of a specific translation.

    Args:
        project_id: The numeric ID of the project.
        translation_id: The numeric ID of the translation.
    """
    result = await tolgee_client.get(
        f"/v2/projects/{project_id}/translations/{translation_id}/history"
    )
    if isinstance(result, str):
        return result

    return json.dumps(result, indent=2)
