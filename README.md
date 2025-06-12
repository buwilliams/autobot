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
autobot show <spec_name>

# Create a new spec
autobot create <spec_name>

# Refine an existing spec
autobot refine <spec_name>

# Infer spec from existing codebase
autobot infer <spec_name> [--path <directory>]

# Generate application from spec using default agent (Claude)
autobot generate <spec_name>

# Generate application using Codex
autobot generate <spec_name> --ai-tool codex

# Preview the generation command (dryrun)
autobot dryrun <spec_name>
autobot dryrun <spec_name> --ai-tool codex

# Configure default AI tool
autobot config default-ai-tool <tool>
autobot config show
```

## Example
```sh
# Create a new web application spec
autobot create my-webapp

# View existing specs
autobot ls
autobot show estimator

# Generate application from spec
autobot generate estimator
autobot generate estimator --ai-tool codex

# Preview generation command
autobot dryrun estimator --ai-tool codex

# Infer spec from existing project
autobot infer my-legacy-app --path /path/to/existing/project

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

## Specification Philosophy

Autobot treats each specification as a **complete, holistic description of an entire application**. Unlike traditional approaches that fragment requirements by technical layer (frontend, backend, database), Autobot specs capture the full application vision in a single, comprehensive document.

### Standardized Spec Structure

Each spec follows a 9-section outline to ensure clarity and completeness:

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

### Simplified Mental Model

- **One Application = One Spec** - Complete applications deserve complete specifications
- **Technology Agnostic** - Specs focus on WHAT the application does, not HOW
- **AI Ready** - Structured format optimized for AI code generation
- **Human Readable** - Clear documentation that serves both humans and machines

## Creating Specs from Existing Codebases

Autobot can automatically analyze existing codebases and generate comprehensive specifications:

```bash
# Analyze current directory and create spec
autobot infer my-app

# Analyze specific directory
autobot infer legacy-api --path /path/to/legacy/project

# Use specific AI tool for analysis  
autobot infer old-webapp --path ./old-app --ai-tool codex
```

### How Spec Inference Works

1. **Codebase Analysis**: Scans project structure, configuration files, and source code
2. **AI-Powered Analysis**: Uses AI agents to understand functionality and purpose
3. **Technology-Agnostic Output**: Generates specs focused on WHAT the app does, not HOW
4. **Standardized Format**: Creates specifications following the 9-section Autobot format
5. **Regeneration Ready**: Resulting specs can be used to rebuild with different technologies

### What Gets Analyzed

- Project structure and organization patterns
- README files and documentation  
- Configuration files (package.json, requirements.txt, etc.)
- Database schema and model definitions
- API routes and endpoint definitions
- Frontend components and page structures
- Business logic and user workflows

The generated specification captures the essence of your application in a technology-agnostic way, enabling you to regenerate it with completely different tech stacks while preserving all functionality.

## License
MIT
