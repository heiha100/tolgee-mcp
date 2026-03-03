## ADDED Requirements

### Requirement: MCP server initialization
The server SHALL initialize a FastMCP instance named "tolgee" using the `mcp` Python SDK's `FastMCP` class with STDIO transport.

#### Scenario: Server starts successfully
- **WHEN** the server process is started via `uv run tolgee-mcp`
- **THEN** the FastMCP server SHALL listen on STDIO for MCP protocol messages

#### Scenario: Server declares its identity
- **WHEN** an MCP client sends an initialize request
- **THEN** the server SHALL respond with name "tolgee" and version from package metadata

### Requirement: Configuration via environment variables
The server SHALL read configuration from environment variables at startup.

#### Scenario: API URL and key configured
- **WHEN** `TOLGEE_API_URL` and `TOLGEE_API_KEY` environment variables are set
- **THEN** the server SHALL use these values for all Tolgee API requests

#### Scenario: Default API URL
- **WHEN** `TOLGEE_API_URL` is not set
- **THEN** the server SHALL default to `https://app.tolgee.io`

#### Scenario: Missing API key
- **WHEN** `TOLGEE_API_KEY` is not set
- **THEN** the server SHALL start but tools SHALL return an error message indicating the API key is not configured

### Requirement: Tolgee HTTP client
The server SHALL provide a shared async HTTP client (`TolgeeClient`) using `httpx.AsyncClient` for all Tolgee API requests.

#### Scenario: Authenticated requests
- **WHEN** any tool makes a request to the Tolgee API
- **THEN** the client SHALL include the API key in the `X-API-Key` header

#### Scenario: HTTP error handling
- **WHEN** the Tolgee API returns an HTTP error (4xx or 5xx)
- **THEN** the client SHALL return a human-readable error message including the status code and response body

#### Scenario: Request timeout
- **WHEN** a request to the Tolgee API does not respond within 30 seconds
- **THEN** the client SHALL return a timeout error message

### Requirement: Project packaging
The project SHALL be packaged with `pyproject.toml` using `uv` for dependency management.

#### Scenario: Project dependencies
- **WHEN** a user runs `uv sync` in the project directory
- **THEN** all dependencies (`mcp[cli]`, `httpx`) SHALL be installed

#### Scenario: Entry point
- **WHEN** a user runs `uv run tolgee-mcp`
- **THEN** the MCP server SHALL start via the configured entry point
