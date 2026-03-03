## ADDED Requirements

### Requirement: Export translations
The server SHALL provide an `export_translations` tool that exports project translations.

#### Scenario: Export as JSON
- **WHEN** the LLM calls `export_translations` with a `project_id` and `format` set to "JSON"
- **THEN** the tool SHALL return the exported translation data as JSON content

#### Scenario: Export with language filter
- **WHEN** the LLM calls `export_translations` with `languages` parameter
- **THEN** the tool SHALL export only translations for the specified languages

#### Scenario: Export with namespace filter
- **WHEN** the LLM calls `export_translations` with `filter_namespace` parameter
- **THEN** the tool SHALL export only translations in the specified namespace

### Requirement: Import translation files
The server SHALL provide an `import_translations` tool that imports translations from structured data.

#### Scenario: Single-step import
- **WHEN** the LLM calls `import_translations` with a `project_id` and translation data containing keys and their translations per language
- **THEN** the tool SHALL import the translations into the project using the single-step import endpoint
