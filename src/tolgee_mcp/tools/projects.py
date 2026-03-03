"""Project management tools."""

from __future__ import annotations

import json
from typing import Any

from tolgee_mcp.server import mcp
from tolgee_mcp.client import tolgee_client


@mcp.tool()
async def list_projects() -> str:
    """List all Tolgee projects accessible to the authenticated user.

    Returns a list of projects with their IDs, names, and base language.
    """
    result = await tolgee_client.get("/v2/projects")
    if isinstance(result, str):
        return result

    projects = tolgee_client.get_embedded(result, "projects")
    if not projects:
        return "No projects found."

    lines = []
    for p in projects:
        base_lang = p.get("baseLanguage", {})
        base_tag = base_lang.get("tag", "N/A") if base_lang else "N/A"
        lines.append(
            f"- **{p.get('name', 'Unnamed')}** (ID: {p.get('id')}) "
            f"[base: {base_tag}]"
        )

    page_info = tolgee_client.format_page_info(result)
    return f"Projects ({page_info}):\n" + "\n".join(lines)


@mcp.tool()
async def get_project(project_id: int) -> str:
    """Get details of a specific Tolgee project.

    Args:
        project_id: The numeric ID of the project.
    """
    result = await tolgee_client.get(f"/v2/projects/{project_id}")
    if isinstance(result, str):
        return result

    return json.dumps(result, indent=2)


@mcp.tool()
async def create_project(name: str, base_language_tag: str = "en") -> str:
    """Create a new Tolgee project.

    Args:
        name: The name for the new project.
        base_language_tag: BCP 47 language tag for the base language (default: "en").
    """
    body: dict[str, Any] = {
        "name": name,
        "languages": [
            {
                "tag": base_language_tag,
                "name": base_language_tag,
                "originalName": base_language_tag,
            }
        ],
    }
    result = await tolgee_client.post("/v2/projects", body=body)
    if isinstance(result, str):
        return result

    return f"Project created successfully.\n{json.dumps(result, indent=2)}"


@mcp.tool()
async def update_project(project_id: int, name: str) -> str:
    """Update an existing Tolgee project's settings.

    Args:
        project_id: The numeric ID of the project to update.
        name: The new name for the project.
    """
    body = {"name": name}
    result = await tolgee_client.put(f"/v2/projects/{project_id}", body=body)
    if isinstance(result, str):
        return result

    return f"Project updated successfully.\n{json.dumps(result, indent=2)}"


@mcp.tool()
async def delete_project(project_id: int) -> str:
    """Delete a Tolgee project. This action is irreversible.

    Args:
        project_id: The numeric ID of the project to delete.
    """
    result = await tolgee_client.delete(f"/v2/projects/{project_id}")
    if isinstance(result, str):
        return result

    return f"Project {project_id} deleted successfully."
