## Why

Tolgee is an open-source localization platform with a comprehensive REST API, but LLMs have no way to interact with it programmatically. Building an MCP (Model Context Protocol) server in Python will allow LLMs to manage translation projects, keys, translations, languages, and related localization workflows through Tolgee's API.

## What Changes

- Create a Python MCP server using the `mcp` SDK (`FastMCP`) with STDIO transport
- Implement tools for core Tolgee API operations:
  - **Project management**: list, create, get, update, delete projects
  - **Language management**: list, create, update, delete languages in a project
  - **Key management**: list, create, update, delete localization keys; search keys; import keys
  - **Translation management**: get, set, update translations; set translation state; get translation history
  - **Export/Import**: export translations in various formats; import translation files
  - **Tag management**: tag/untag keys, list tags
  - **Namespace management**: list and manage namespaces
- Provide a configurable authentication mechanism supporting both PAT (Personal Access Token) and project-scoped API keys
- Package with `pyproject.toml` using `uv` for dependency management

## Capabilities

### New Capabilities
- `server-core`: MCP server initialization, configuration, authentication, and HTTP client setup for the Tolgee API
- `project-tools`: Tools for managing Tolgee projects (list, create, get, update, delete)
- `language-tools`: Tools for managing languages within a project
- `key-tools`: Tools for managing localization keys (CRUD, search, import)
- `translation-tools`: Tools for managing translations (get, set, update state, history)
- `export-import-tools`: Tools for exporting and importing translation data
- `tag-namespace-tools`: Tools for managing tags and namespaces

### Modified Capabilities

## Impact

- New Python project with `pyproject.toml`, dependencies: `mcp[cli]`, `httpx`
- No existing code is affected (greenfield project)
- Requires network access to a Tolgee instance (cloud or self-hosted)
- Authentication via environment variables (`TOLGEE_API_KEY`, `TOLGEE_API_URL`)
