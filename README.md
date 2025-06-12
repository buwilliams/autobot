# Autobot

**Save, refine, and leverage application specs for AI-driven development.**

![Autobot Logo](images/autobot.png)

## Overview
Autobot is a Python-based CLI tool for creating, managing, and leveraging detailed application specifications (specs) with AI code agents. It helps you save technical requirements, refine them over time, and use them to generate applications from scratch. Specs contain comprehensive details including purpose, goals, database schema, API endpoints, and UI layouts that AI agents use to create complete applications.

## Prerequisites
- [Python 3.7+](https://www.python.org/downloads/)
- [Node.js (for some agents)](https://nodejs.org/en/download/)
- At least one supported AI agent CLI:
  - [Claude Code (Anthropic)](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview)
  - [OpenAI Codex](https://github.com/openai/codex)

> Note: Each agent may have its own installation and authentication requirements. See the linked documentation for setup instructions.

## Features
- Create new application specs with standardized structure
- Manage and refine existing specs
- Generate applications from specs using AI agents (Codex, Claude, or others)
- List and view spec contents
- Dry-run to preview generation commands
- Support for multiple AI agents via the `ai-tools` directory
- Structured spec format for disambiguation and clarity

## Recommended to add Autobot to your shell

Add the following alias to your shell configuration file (e.g. `~/.bashrc` or `~/.zshrc`):

```sh
alias autobot='<path_to_autobot>/autobot.sh'
```

## Usage

```sh
# Show help
autobot

# List available spec types
autobot ls

# List specs for a type
autobot ls <type>

# Show a spec's contents
autobot show <type>:<spec_name>

# Create a new spec
autobot create <type>:<spec_name>

# Refine an existing spec
autobot refine <type>:<spec_name>

# Generate application from spec using default agent (Claude)
autobot generate <type>:<spec_name>

# Generate application using Codex
autobot generate <type>:<spec_name> --ai-tool codex

# Preview the generation command (dryrun)
autobot dryrun <type>:<spec_name>
autobot dryrun <type>:<spec_name> --ai-tool codex

# Configure default AI tool
autobot config default-ai-tool <tool>
autobot config show
```

## Example
```sh
# Create a new web application spec
autobot create app:my-webapp

# View existing specs
autobot ls backend
autobot show backend:python

# Generate application from spec
autobot generate backend:python
autobot generate backend:python --ai-tool codex

# Preview generation command
autobot dryrun backend:python --ai-tool codex

# Configure AI tools
autobot config show
autobot config default-ai-tool codex
```

## AI Agent Configuration

Autobot supports multiple AI code agents. The available agents are defined in the `ai-tools/` directory as Python files. Each file must define an `execute(spec_path)` function that returns the shell command to run for that agent.

- `ai-tools/codex.py` (default):
  ```python
  def execute(spec_path):
      with open(spec_path, 'r') as file:
          spec = file.read()
      # Escape single quotes for shell: 'abc' -> 'a'"'"'b'"'"'c'
      escaped = spec.replace("'", "'\"'\"'")
      return f"codex --approval-mode full-auto '{escaped}'"
  ```
  **Note:** Codex will automatically escape single quotes in the spec content to ensure the generated shell command runs correctly.
- `ai-tools/claude.py`:
  ```python
  def execute(spec_path):
      with open(spec_path, 'r') as file:
          spec = file.read()
      return f"echo '{spec}' | claude -p --allowedTools 'Bash,Edit,Write'"
  ```

To add a new agent, create a new `.py` file in `ai-tools/` with the required `execute(spec_path)` function.

Choose an agent at runtime with `--ai-tool <agent>`. If not specified, `claude` is used by default. You can change the default with `autobot config default-ai-tool <tool>`.

## Spec Structure

Each spec follows a standardized outline to ensure clarity and completeness:

1. **Purpose**: What the application does and why it exists
2. **Goals**: Primary objectives and success criteria
3. **Use Cases**: Detailed user interaction scenarios
4. **Usage Rules**: Behavioral constraints and requirements
5. **Database Schema**: Data structure and relationships
6. **Services**: Core functionality and business logic
7. **Endpoints**: API design and interface contracts
8. **UI Layout**: User interface structure and components
9. **Pages**: Application flow and navigation

This structure helps AI agents understand both technical requirements and user intent, enabling better code generation and reducing ambiguity.

## Creating Specs from Existing Codebases

Autobot can help you create specs based on existing applications:
1. Analyze your current codebase structure
2. Extract key components, APIs, and data models
3. Document the application's purpose and behavior
4. Create a comprehensive spec for future regeneration or evolution

## License
MIT
