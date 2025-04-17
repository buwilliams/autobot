# Autobot

**Progressively build frameworks and applications with external AI code agents.**

![Autobot Logo](images/autobot.png)

## Overview
Autobot is a Python-based CLI tool for generating, listing, and running code templates using external AI code agents (like Codex or Claude). It helps you scaffold and evolve applications and frameworks in a modular, repeatable way. The AI agent command is externalized and configurable via the `ai-tools` directory.

## Prerequisites
- [Python 3.7+](https://www.python.org/downloads/)
- [Node.js (for some agents)](https://nodejs.org/en/download/)
- At least one supported AI agent CLI:
  - [Claude Code (Anthropic)](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview)
  - [OpenAI Codex](https://github.com/openai/codex)

> Note: Each agent may have its own installation and authentication requirements. See the linked documentation for setup instructions.

## Features
- List available template types and templates
- Show template contents
- Run templates through a configurable AI agent (Codex, Claude, or others)
- Dry-run to preview the command
- Easily add support for new AI agents via the `ai-tools` directory

## Usage

```sh
# Show help
./autobot.sh

# List available types
./autobot.sh list

# List templates for a type
./autobot.sh list <type>

# Show a template's contents
./autobot.sh show <type>:<template_name>

# Run a template through the default agent (Codex)
./autobot.sh run <type>:<template_name>

# Run a template through Claude
./autobot.sh run <type>:<template_name> --ai-tool claude

# Preview the command that would be run (dryrun)
./autobot.sh dryrun <type>:<template_name>
./autobot.sh dryrun <type>:<template_name> --ai-tool claude
```

## Example
```sh
./autobot.sh list backend
./autobot.sh show backend:python
./autobot.sh run backend:python
./autobot.sh run backend:python --ai-tool claude
./autobot.sh dryrun backend:python --ai-tool codex
```

## AI Agent Configuration

Autobot supports multiple AI code agents. The available agents are defined in the `ai-tools/` directory as Python files. Each file must define an `execute(template_path)` function that returns the shell command to run for that agent.

- `ai-tools/codex.py` (default):
  ```python
  def execute(template_path):
      with open(template_path, 'r') as file:
          template = file.read()
      return f"codex --quiet --approval-mode full-auto '{template}'"
  ```
- `ai-tools/claude.py`:
  ```python
  def execute(template_path):
      with open(template_path, 'r') as file:
          template = file.read()
      return f"echo '{template}' | claude -p --allowedTools 'Bash,Edit,Write'"
  ```

To add a new agent, create a new `.py` file in `ai-tools/` with the required `execute(template_path)` function.

Choose an agent at runtime with `--ai-tool <agent>`. If not specified, `codex` is used by default.

## License
MIT
