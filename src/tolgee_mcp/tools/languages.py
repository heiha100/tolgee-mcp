"""Language management tools."""

from __future__ import annotations

import json

from tolgee_mcp.server import mcp
from tolgee_mcp.client import tolgee_client


@mcp.tool()
async def list_languages(project_id: int) -> str:
    """List all languages configured in a Tolgee project.

    Args:
        project_id: The numeric ID of the project.
    """
    result = await tolgee_client.get(f"/v2/projects/{project_id}/languages")
    if isinstance(result, str):
        return result

    languages = tolgee_client.get_embedded(result, "languages")
    if not languages:
        return "No languages found in this project."

    lines = []
    for lang in languages:
        base = " (base)" if lang.get("base", False) else ""
        lines.append(
            f"- **{lang.get('name', 'Unknown')}** "
            f"[tag: {lang.get('tag', '?')}] "
            f"(ID: {lang.get('id')}){base}"
        )

    page_info = tolgee_client.format_page_info(result)
    return f"Languages ({page_info}):\n" + "\n".join(lines)


@mcp.tool()
async def create_language(project_id: int, name: str, tag: str) -> str:
    """Add a new language to a Tolgee project.

    Args:
        project_id: The numeric ID of the project.
        name: Display name of the language (e.g., "French").
        tag: BCP 47 language tag (e.g., "fr", "de", "ja").
    """
    body = {
        "name": name,
        "tag": tag,
        "originalName": name,
    }
    result = await tolgee_client.post(
        f"/v2/projects/{project_id}/languages", body=body
    )
    if isinstance(result, str):
        return result

    return f"Language created successfully.\n{json.dumps(result, indent=2)}"


@mcp.tool()
async def update_language(
    project_id: int, language_id: int, name: str
) -> str:
    """Update a language's properties in a Tolgee project.

    Args:
        project_id: The numeric ID of the project.
        language_id: The numeric ID of the language to update.
        name: The new display name for the language.
    """
    body = {"name": name}
    result = await tolgee_client.put(
        f"/v2/projects/{project_id}/languages/{language_id}", body=body
    )
    if isinstance(result, str):
        return result

    return f"Language updated successfully.\n{json.dumps(result, indent=2)}"


@mcp.tool()
async def delete_language(project_id: int, language_id: int) -> str:
    """Delete a language from a Tolgee project. This removes all translations for this language.

    Args:
        project_id: The numeric ID of the project.
        language_id: The numeric ID of the language to delete.
    """
    result = await tolgee_client.delete(
        f"/v2/projects/{project_id}/languages/{language_id}"
    )
    if isinstance(result, str):
        return result

    return f"Language {language_id} deleted successfully."
