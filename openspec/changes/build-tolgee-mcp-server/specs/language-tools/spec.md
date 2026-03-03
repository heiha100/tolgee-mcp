## ADDED Requirements

### Requirement: List languages
The server SHALL provide a `list_languages` tool that lists all languages in a project.

#### Scenario: Successful language listing
- **WHEN** the LLM calls `list_languages` with a `project_id`
- **THEN** the tool SHALL return all languages with their IDs, names, tags, and base language flag

### Requirement: Create language
The server SHALL provide a `create_language` tool that adds a new language to a project.

#### Scenario: Successful language creation
- **WHEN** the LLM calls `create_language` with a `project_id`, `name`, and `tag` (e.g., "fr")
- **THEN** the tool SHALL create the language and return its details

#### Scenario: Duplicate language tag
- **WHEN** the LLM calls `create_language` with a tag that already exists in the project
- **THEN** the tool SHALL return an error message indicating the language already exists

### Requirement: Update language
The server SHALL provide an `update_language` tool that updates a language's properties.

#### Scenario: Update language name
- **WHEN** the LLM calls `update_language` with a `project_id`, `language_id`, and new `name`
- **THEN** the tool SHALL update the language and return the updated details

### Requirement: Delete language
The server SHALL provide a `delete_language` tool that removes a language from a project.

#### Scenario: Successful deletion
- **WHEN** the LLM calls `delete_language` with a `project_id` and `language_id`
- **THEN** the tool SHALL delete the language and return a confirmation message
