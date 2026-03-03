## Context

This is a greenfield Python project. There is no existing codebase. The goal is to create an MCP server that wraps the Tolgee REST API, enabling LLMs to manage localization workflows. The Tolgee API is documented at `https://docs.tolgee.io/api` and uses Bearer token (PAT) or API Key authentication. All project-scoped endpoints follow the pattern `/v2/projects/{projectId}/...`.

## Goals / Non-Goals

**Goals:**
- Build a working MCP server in Python using the `mcp` SDK's `FastMCP` class with STDIO transport
- Cover the most commonly used Tolgee API operations (projects, languages, keys, translations, export/import, tags, namespaces)
- Provide clear tool descriptions and parameter documentation so LLMs can use them effectively
- Support both Tolgee Cloud and self-hosted instances via configurable base URL
- Use `httpx` for async HTTP requests to the Tolgee API
- Package with `pyproject.toml` and `uv` for dependency management

**Non-Goals:**
- Building a web UI or HTTP-based MCP transport (STDIO only for v1)
- Implementing every Tolgee API endpoint (batch operations, webhooks, billing, SSO, glossary, AI features are out of scope)
- MCP Resources or Prompts (tools only for v1)
- Automated testing infrastructure (manual testing against a Tolgee instance)
- Publishing to PyPI

## Decisions

### 1. Python with FastMCP

**Choice**: Use Python 3.10+ with the `mcp` SDK's `FastMCP` class.
**Rationale**: FastMCP uses Python type hints and docstrings to auto-generate tool definitions, minimizing boilerplate. Python is the most common language for MCP servers. The user requested Python.
**Alternatives**: TypeScript SDK — rejected because user specified Python.

### 2. STDIO Transport

**Choice**: Use STDIO transport exclusively.
**Rationale**: STDIO is the standard for local MCP servers. It's simpler to configure and works with all MCP clients (Claude Desktop, OpenCode, etc.). HTTP/SSE transport can be added later.
**Alternatives**: HTTP+SSE transport — out of scope for v1, can be added without breaking changes.

### 3. httpx for HTTP Client

**Choice**: Use `httpx.AsyncClient` for all Tolgee API calls.
**Rationale**: `httpx` is the standard async HTTP client in Python. It supports connection pooling, timeouts, and async/await natively. The MCP SDK already uses async patterns.
**Alternatives**: `aiohttp` — heavier dependency, `httpx` is more Pythonic; `requests` — synchronous only.

### 4. Configuration via Environment Variables

**Choice**: Read `TOLGEE_API_KEY` and `TOLGEE_API_URL` from environment variables.
**Rationale**: Environment variables are the standard way to configure MCP servers (set in the MCP client config JSON). No need for config files.
**Alternatives**: Config file — adds complexity without benefit for an MCP server.

### 5. Module Structure

**Choice**: Single-package structure with separate modules per tool group:
```
src/tolgee_mcp/
  __init__.py
  server.py          # FastMCP instance, main entry point
  client.py          # Tolgee API HTTP client wrapper
  tools/
    __init__.py
    projects.py       # Project management tools
    languages.py      # Language management tools
    keys.py           # Key management tools
    translations.py   # Translation management tools
    export_import.py  # Export/import tools
    tags.py           # Tag and namespace tools
```
**Rationale**: Separating tools by domain keeps each module focused and maintainable. A shared HTTP client in `client.py` avoids duplication of auth/request logic.
**Alternatives**: Single file — would work but becomes unwieldy with 20+ tools.

### 6. Shared Tolgee HTTP Client

**Choice**: Create a `TolgeeClient` class that encapsulates authentication, base URL, error handling, and common request patterns.
**Rationale**: Every tool needs authenticated HTTP requests. Centralizing this avoids duplication and ensures consistent error handling. The client will be instantiated once at server startup and passed to tool functions.

### 7. Error Handling Strategy

**Choice**: Tools return descriptive error messages as text rather than raising exceptions. HTTP errors from Tolgee are caught and returned as human-readable strings.
**Rationale**: MCP tools should return useful text that LLMs can understand and relay to users. Unhandled exceptions in MCP tools break the protocol.

## Risks / Trade-offs

- **[API surface breadth vs. depth]** → We cover core operations but skip advanced features (batch ops, webhooks, glossary). Users needing those will have to extend the server. Mitigation: modular design makes adding tools straightforward.
- **[Tolgee API versioning]** → The API may change. Mitigation: pin to v2 endpoints, which are the current stable API.
- **[Rate limiting]** → Tolgee Cloud may rate-limit requests. Mitigation: tools execute one at a time through MCP, which inherently throttles usage. Add retry with backoff in the HTTP client.
- **[Large response payloads]** → Some endpoints (e.g., get all translations) can return large datasets. Mitigation: support pagination parameters in tools and default to reasonable page sizes.
