"""Tag and namespace management tools."""

from __future__ import annotations

import json

from tolgee_mcp.server import mcp
from tolgee_mcp.client import tolgee_client


@mcp.tool()
async def list_tags(project_id: int, page: int = 0, size: int = 20) -> str:
    """List all tags in a Tolgee project.

    Args:
        project_id: The numeric ID of the project.
        page: Page number (0-indexed, default 0).
        size: Number of tags per page (default 20).
    """
    params = {"page": page, "size": size}
    result = await tolgee_client.get(
        f"/v2/projects/{project_id}/tags", params=params
    )
    if isinstance(result, str):
        return result

    tags = tolgee_client.get_embedded(result, "tags")
    if not tags:
        return "No tags found in this project."

    lines = []
    for t in tags:
        lines.append(f"- **{t.get('name', '')}** (ID: {t.get('id')})")

    page_info = tolgee_client.format_page_info(result)
    return f"Tags ({page_info}):\n" + "\n".join(lines)


@mcp.tool()
async def tag_key(project_id: int, key_id: int, tag_name: str) -> str:
    """Add a tag to a localization key. Creates the tag if it doesn't exist.

    Args:
        project_id: The numeric ID of the project.
        key_id: The numeric ID of the key to tag.
        tag_name: The name of the tag to add.
    """
    body = {"name": tag_name}
    result = await tolgee_client.put(
        f"/v2/projects/{project_id}/keys/{key_id}/tags", body=body
    )
    if isinstance(result, str):
        return result

    return f"Tag '{tag_name}' added to key {key_id}.\n{json.dumps(result, indent=2)}"


@mcp.tool()
async def remove_tag_from_key(
    project_id: int, key_id: int, tag_id: int
) -> str:
    """Remove a tag from a localization key.

    Args:
        project_id: The numeric ID of the project.
        key_id: The numeric ID of the key.
        tag_id: The numeric ID of the tag to remove.
    """
    result = await tolgee_client.delete(
        f"/v2/projects/{project_id}/keys/{key_id}/tags/{tag_id}"
    )
    if isinstance(result, str):
        return result

    return f"Tag {tag_id} removed from key {key_id}."


@mcp.tool()
async def list_namespaces(project_id: int) -> str:
    """List all used namespaces in a Tolgee project.

    Args:
        project_id: The numeric ID of the project.
    """
    result = await tolgee_client.get(
        f"/v2/projects/{project_id}/used-namespaces"
    )
    if isinstance(result, str):
        return result

    # This endpoint may return a list directly
    if isinstance(result, list):
        if not result:
            return "No namespaces found in this project."
        lines = []
        for ns in result:
            if isinstance(ns, dict):
                lines.append(
                    f"- **{ns.get('name', '(default)')}** (ID: {ns.get('id', 'N/A')})"
                )
            else:
                lines.append(f"- {ns}")
        return "Namespaces:\n" + "\n".join(lines)

    # Paginated response format
    namespaces = tolgee_client.get_embedded(result, "namespaces")
    if not namespaces:
        return "No namespaces found in this project."

    lines = []
    for ns in namespaces:
        lines.append(
            f"- **{ns.get('name', '(default)')}** (ID: {ns.get('id', 'N/A')})"
        )

    return "Namespaces:\n" + "\n".join(lines)


@mcp.tool()
async def update_namespace(
    project_id: int, namespace_id: int, name: str
) -> str:
    """Rename a namespace in a Tolgee project.

    Args:
        project_id: The numeric ID of the project.
        namespace_id: The numeric ID of the namespace to rename.
        name: The new name for the namespace.
    """
    body = {"name": name}
    result = await tolgee_client.put(
        f"/v2/projects/{project_id}/namespaces/{namespace_id}", body=body
    )
    if isinstance(result, str):
        return result

    return f"Namespace renamed to '{name}'.\n{json.dumps(result, indent=2)}"
