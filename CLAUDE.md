# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Autobot is a Python CLI tool for creating, managing, and leveraging detailed application specifications (specs) with AI code agents. It helps save technical requirements, refine them over time, and use them to generate applications from scratch using AI agents like Codex and Claude.

## Core Architecture

- **Entry Points**: `autobot.py` (main CLI) and `autobot.sh` (bash wrapper)
- **Specs**: Markdown files in `specs/` organized by type with standardized structure
- **AI Tools**: Python modules in `ai-tools/` that define how to execute specs with different AI agents
- **Spec Types**: backend, frontend, design, applications, components, experimental, examples, db

## Key Commands

```bash
# Run autobot (use autobot.sh wrapper or python3 autobot.py)
python3 autobot.py                                         # Show help
python3 autobot.py ls                                      # List spec types  
python3 autobot.py ls <type>                               # List specs for type
python3 autobot.py show <type>:<spec>                      # Show spec content
python3 autobot.py create <type>:<spec>                    # Create new spec
python3 autobot.py refine <type>:<spec>                    # Refine existing spec
python3 autobot.py generate <type>:<spec>                  # Generate with default AI tool (claude)
python3 autobot.py generate <type>:<spec> --ai-tool codex  # Generate with specific AI tool
python3 autobot.py config default-ai-tool <tool>           # Set default AI tool
python3 autobot.py config show                             # Show current configuration
python3 autobot.py dryrun <type>:<spec>                    # Preview generation command
```

## AI Tool Integration

Each AI tool in `ai-tools/` must implement an `execute(spec_path)` function that returns a shell command string. Available tools:
- `claude.py` (default): Pipes spec to Claude Code with Bash/Edit/Write tools
- `codex.py`: Uses OpenAI Codex with full-auto approval

The default AI tool can be changed using `autobot config default-ai-tool <tool>` and is persisted in `.autobot-config.json`.

## Spec Structure

Specs are markdown files that contain detailed application requirements for AI agents. They follow a standardized outline:

### Standardized Spec Format
Each spec contains these sections:
1. **Purpose**: What the application does and why it exists
2. **Goals**: Primary objectives and success criteria  
3. **Use Cases**: Detailed user interaction scenarios
4. **Usage Rules**: Behavioral constraints and requirements
5. **Database Schema**: Data structure and relationships
6. **Services**: Core functionality and business logic
7. **Endpoints**: API design and interface contracts
8. **UI Layout**: User interface structure and components
9. **Pages**: Application flow and navigation

### Spec Types
- **backend/**: Server-side frameworks (Python/FastAPI, static sites)
- **frontend/**: Client-side frameworks (Next.js, Alpine.js)
- **applications/**: Complete applications (estimator, nevo-ai, tsql-spark)
- **components/**: Reusable components and modules
- **experimental/**: Experimental specs and development phases
- **examples/**: Example specs and test cases
- **design/**: Design-related specifications
- **db/**: Database-specific specifications

## Development Notes

- Specs use markdown format with standardized sections for clarity and AI disambiguation
- The tool dynamically loads AI modules using importlib for extensibility
- Spec naming follows `<type>/<name>.md` convention
- Shell command construction handles quote escaping for different AI tools
- Specs can be created from existing codebases or built from scratch
- Refinement workflow allows iterative improvement of specifications
- Structured format reduces ambiguity and improves AI code generation quality