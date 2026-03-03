## 1. Project Setup

- [x] 1.1 Initialize project with `uv init`, create `pyproject.toml` with dependencies (`mcp[cli]`, `httpx`) and entry point (`tolgee-mcp`)
- [x] 1.2 Create package structure: `src/tolgee_mcp/` with `__init__.py`, `server.py`, `client.py`, and `tools/` subpackage
- [x] 1.3 Set up `__main__.py` entry point so `uv run tolgee-mcp` starts the server

## 2. Tolgee HTTP Client

- [x] 2.1 Implement `TolgeeClient` class in `client.py` with `httpx.AsyncClient`, reading `TOLGEE_API_URL` and `TOLGEE_API_KEY` from environment variables
- [x] 2.2 Add authenticated request methods (`get`, `post`, `put`, `delete`) with `X-API-Key` header, 30s timeout, and error handling that returns human-readable messages
- [x] 2.3 Add response parsing helpers for paginated Tolgee API responses

## 3. Server Core

- [x] 3.1 Create `FastMCP` instance in `server.py` with name "tolgee" and STDIO transport
- [x] 3.2 Instantiate `TolgeeClient` at module level and wire it into the server lifecycle
- [x] 3.3 Register all tool modules (import and register tools from each tools/ module)

## 4. Project Tools

- [x] 4.1 Implement `list_projects` tool — `GET /v2/projects`
- [x] 4.2 Implement `get_project` tool — `GET /v2/projects/{projectId}`
- [x] 4.3 Implement `create_project` tool — `POST /v2/projects`
- [x] 4.4 Implement `update_project` tool — `PUT /v2/projects/{projectId}`
- [x] 4.5 Implement `delete_project` tool — `DELETE /v2/projects/{projectId}`

## 5. Language Tools

- [x] 5.1 Implement `list_languages` tool — `GET /v2/projects/{projectId}/languages`
- [x] 5.2 Implement `create_language` tool — `POST /v2/projects/{projectId}/languages`
- [x] 5.3 Implement `update_language` tool — `PUT /v2/projects/{projectId}/languages/{languageId}`
- [x] 5.4 Implement `delete_language` tool — `DELETE /v2/projects/{projectId}/languages/{languageId}`

## 6. Key Tools

- [x] 6.1 Implement `list_keys` tool — `GET /v2/projects/{projectId}/keys` with pagination support
- [x] 6.2 Implement `search_keys` tool — `GET /v2/projects/{projectId}/keys/search`
- [x] 6.3 Implement `create_key` tool — `POST /v2/projects/{projectId}/keys/create` with optional translations and namespace
- [x] 6.4 Implement `update_key` tool — `PUT /v2/projects/{projectId}/keys/{keyId}`
- [x] 6.5 Implement `delete_keys` tool — `DELETE /v2/projects/{projectId}/keys` with list of key IDs
- [x] 6.6 Implement `import_keys` tool — `POST /v2/projects/{projectId}/keys/import` for batch key import with translations

## 7. Translation Tools

- [x] 7.1 Implement `get_translations` tool — `GET /v2/projects/{projectId}/translations` with language and pagination filters
- [x] 7.2 Implement `set_translations` tool — `POST /v2/projects/{projectId}/translations` for setting translation values on existing keys
- [x] 7.3 Implement `create_or_update_translations` tool — `POST /v2/projects/{projectId}/translations/createOrUpdate`
- [x] 7.4 Implement `set_translation_state` tool — `PUT /v2/projects/{projectId}/translations/{translationId}/set-state/{state}`
- [x] 7.5 Implement `get_translation_history` tool — `GET /v2/projects/{projectId}/translations/{translationId}/history`

## 8. Export/Import Tools

- [x] 8.1 Implement `export_translations` tool — `POST /v2/projects/{projectId}/export` with format, language, and namespace filters
- [x] 8.2 Implement `import_translations` tool — `POST /v2/projects/{projectId}/single-step-import` for single-step import from structured data

## 9. Tag and Namespace Tools

- [x] 9.1 Implement `list_tags` tool — `GET /v2/projects/{projectId}/tags`
- [x] 9.2 Implement `tag_key` tool — `PUT /v2/projects/{projectId}/keys/{keyId}/tags`
- [x] 9.3 Implement `remove_tag_from_key` tool — `DELETE /v2/projects/{projectId}/keys/{keyId}/tags/{tagId}`
- [x] 9.4 Implement `list_namespaces` tool — `GET /v2/projects/{projectId}/used-namespaces`
- [x] 9.5 Implement `update_namespace` tool — `PUT /v2/projects/{projectId}/namespaces/{namespaceId}`
