## ADDED Requirements

### Requirement: List projects
The server SHALL provide a `list_projects` tool that lists all projects accessible to the authenticated user.

#### Scenario: Successful project listing
- **WHEN** the LLM calls the `list_projects` tool
- **THEN** the tool SHALL return a list of projects with their IDs, names, and base language

#### Scenario: No projects available
- **WHEN** the authenticated user has no projects
- **THEN** the tool SHALL return a message indicating no projects were found

### Requirement: Get project details
The server SHALL provide a `get_project` tool that retrieves details of a specific project.

#### Scenario: Valid project ID
- **WHEN** the LLM calls `get_project` with a valid `project_id`
- **THEN** the tool SHALL return the project's name, ID, description, base language, and statistics

#### Scenario: Invalid project ID
- **WHEN** the LLM calls `get_project` with a non-existent `project_id`
- **THEN** the tool SHALL return an error message indicating the project was not found

### Requirement: Create project
The server SHALL provide a `create_project` tool that creates a new Tolgee project.

#### Scenario: Successful project creation
- **WHEN** the LLM calls `create_project` with a `name` and `base_language_tag` (e.g., "en")
- **THEN** the tool SHALL create the project and return the new project's ID and details

### Requirement: Update project
The server SHALL provide an `update_project` tool that updates an existing project's settings.

#### Scenario: Update project name
- **WHEN** the LLM calls `update_project` with a `project_id` and new `name`
- **THEN** the tool SHALL update the project and return the updated details

### Requirement: Delete project
The server SHALL provide a `delete_project` tool that deletes a project.

#### Scenario: Successful deletion
- **WHEN** the LLM calls `delete_project` with a valid `project_id`
- **THEN** the tool SHALL delete the project and return a confirmation message
