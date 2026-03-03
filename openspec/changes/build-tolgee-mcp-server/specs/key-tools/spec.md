## ADDED Requirements

### Requirement: List keys
The server SHALL provide a `list_keys` tool that lists localization keys in a project.

#### Scenario: List all keys
- **WHEN** the LLM calls `list_keys` with a `project_id`
- **THEN** the tool SHALL return keys with their IDs, names, namespaces, and tags

#### Scenario: Pagination
- **WHEN** the LLM calls `list_keys` with a `project_id` and optional `page` and `size` parameters
- **THEN** the tool SHALL return the requested page of keys

### Requirement: Search keys
The server SHALL provide a `search_keys` tool that searches for keys matching a query.

#### Scenario: Search by name
- **WHEN** the LLM calls `search_keys` with a `project_id` and `search` query string
- **THEN** the tool SHALL return keys whose names contain the search string

### Requirement: Create key
The server SHALL provide a `create_key` tool that creates a new localization key.

#### Scenario: Create key with translations
- **WHEN** the LLM calls `create_key` with a `project_id`, `name`, and optional `translations` dict (mapping language tags to values)
- **THEN** the tool SHALL create the key with translations and return the key details

#### Scenario: Create key with namespace
- **WHEN** the LLM calls `create_key` with a `project_id`, `name`, and `namespace`
- **THEN** the tool SHALL create the key in the specified namespace

### Requirement: Update key
The server SHALL provide an `update_key` tool that updates a key's name.

#### Scenario: Rename key
- **WHEN** the LLM calls `update_key` with a `project_id`, `key_id`, and new `name`
- **THEN** the tool SHALL update the key name and return the updated details

### Requirement: Delete keys
The server SHALL provide a `delete_keys` tool that deletes one or more keys.

#### Scenario: Delete multiple keys
- **WHEN** the LLM calls `delete_keys` with a `project_id` and a list of `key_ids`
- **THEN** the tool SHALL delete the specified keys and return a confirmation message

### Requirement: Import keys
The server SHALL provide an `import_keys` tool that imports keys with translations.

#### Scenario: Import keys with translations
- **WHEN** the LLM calls `import_keys` with a `project_id` and a list of key objects containing `name` and `translations`
- **THEN** the tool SHALL create or update the keys with their translations
