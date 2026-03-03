## ADDED Requirements

### Requirement: List tags
The server SHALL provide a `list_tags` tool that lists all tags in a project.

#### Scenario: Successful tag listing
- **WHEN** the LLM calls `list_tags` with a `project_id`
- **THEN** the tool SHALL return all tags with their IDs and names

### Requirement: Tag keys
The server SHALL provide a `tag_key` tool that adds a tag to a localization key.

#### Scenario: Add tag to key
- **WHEN** the LLM calls `tag_key` with a `project_id`, `key_id`, and `tag_name`
- **THEN** the tool SHALL add the tag to the key (creating the tag if it doesn't exist) and return confirmation

### Requirement: Remove tag from key
The server SHALL provide a `remove_tag_from_key` tool that removes a tag from a key.

#### Scenario: Remove existing tag
- **WHEN** the LLM calls `remove_tag_from_key` with a `project_id`, `key_id`, and `tag_id`
- **THEN** the tool SHALL remove the tag from the key and return confirmation

### Requirement: List namespaces
The server SHALL provide a `list_namespaces` tool that lists all namespaces in a project.

#### Scenario: Successful namespace listing
- **WHEN** the LLM calls `list_namespaces` with a `project_id`
- **THEN** the tool SHALL return all namespaces with their IDs and names

### Requirement: Update namespace
The server SHALL provide an `update_namespace` tool that renames a namespace.

#### Scenario: Rename namespace
- **WHEN** the LLM calls `update_namespace` with a `project_id`, `namespace_id`, and new `name`
- **THEN** the tool SHALL rename the namespace and return the updated details
