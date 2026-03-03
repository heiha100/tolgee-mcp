## ADDED Requirements

### Requirement: Get translations
The server SHALL provide a `get_translations` tool that retrieves translations for keys in a project.

#### Scenario: Get all translations
- **WHEN** the LLM calls `get_translations` with a `project_id`
- **THEN** the tool SHALL return translations organized by key and language

#### Scenario: Filter by languages
- **WHEN** the LLM calls `get_translations` with a `project_id` and `languages` list (e.g., ["en", "fr"])
- **THEN** the tool SHALL return translations only for the specified languages

#### Scenario: Pagination
- **WHEN** the LLM calls `get_translations` with `page` and `size` parameters
- **THEN** the tool SHALL return the requested page of translations

### Requirement: Set translations
The server SHALL provide a `set_translations` tool that sets translation values for an existing key.

#### Scenario: Set translation for a key
- **WHEN** the LLM calls `set_translations` with a `project_id`, `key_name`, and `translations` dict (mapping language tags to text values)
- **THEN** the tool SHALL update the translations for the specified key

### Requirement: Create or update translations
The server SHALL provide a `create_or_update_translations` tool that creates a key if it doesn't exist and sets its translations.

#### Scenario: Key does not exist
- **WHEN** the LLM calls `create_or_update_translations` with a `project_id`, `key_name`, and `translations`
- **THEN** the tool SHALL create the key and set the translations

#### Scenario: Key already exists
- **WHEN** the LLM calls `create_or_update_translations` for an existing key
- **THEN** the tool SHALL update the translations for that key

### Requirement: Set translation state
The server SHALL provide a `set_translation_state` tool that changes the state of a translation.

#### Scenario: Mark translation as reviewed
- **WHEN** the LLM calls `set_translation_state` with a `project_id`, `translation_id`, and `state` (e.g., "REVIEWED")
- **THEN** the tool SHALL update the translation state and return confirmation

### Requirement: Get translation history
The server SHALL provide a `get_translation_history` tool that retrieves the modification history of a translation.

#### Scenario: View history
- **WHEN** the LLM calls `get_translation_history` with a `project_id` and `translation_id`
- **THEN** the tool SHALL return the history of changes for that translation
