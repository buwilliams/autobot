# Autobot

**Progressively build frameworks and applications with Claude Code.**

## Overview
Autobot is a Python-based CLI tool for generating, listing, and running code templates using Claude Code. It helps you scaffold and evolve applications and frameworks in a modular, repeatable way.

## Features
- List available template types and templates
- Show template contents
- Run templates through Claude Code
- Dry-run to preview the command

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

# Run a template through Claude Code
./autobot.sh run <type>:<template_name>

# Preview the command that would be run
./autobot.sh dryrun <type>:<template_name>
```

## Example
```sh
./autobot.sh list backend
./autobot.sh show backend:python
./autobot.sh run backend:python
```

## Requirements
- Python 3.7+
- Claude CLI (claude)

## Directory Structure
- `autobot.py` — main CLI script
- `autobot.sh` — pass-through shell script
- `templates/` — directory containing template types and files

## License
MIT
