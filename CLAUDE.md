# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Autobot is a Python CLI tool for creating, managing, and leveraging detailed application specifications (specs) with AI code agents. It helps save technical requirements, refine them over time, and use them to generate applications from scratch using AI agents like Codex and Claude.

## Core Architecture

- **Entry Points**: `autobot.py` (main CLI) and `autobot.sh` (bash wrapper)
- **Specs**: Markdown files in `specs/` directory with standardized structure
- **AI Tools**: Python modules in `ai-tools/` that define how to execute specs with different AI agents
- **Review Directory**: `specs/_review/` contains component-level specs for evaluation

## Key Commands

```bash
# Run autobot (use autobot.sh wrapper or python3 autobot.py)
python3 autobot.py                                    # Show help
python3 autobot.py ls                                 # List available specs
python3 autobot.py show <spec>                       # Show spec content
python3 autobot.py create <spec>                     # Create new spec
python3 autobot.py refine <spec>                     # Refine existing spec
python3 autobot.py infer <spec> [--path <dir>]       # Infer spec from codebase
python3 autobot.py generate <spec>                   # Generate with default AI tool (claude)
python3 autobot.py generate <spec> --ai-tool codex   # Generate with specific AI tool
python3 autobot.py dryrun <spec>                     # Preview generation command
python3 autobot.py config default-ai-tool <tool>     # Set default AI tool
python3 autobot.py config show                       # Show current configuration
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

### Directory Structure
- **specs/**: Complete application specifications (one file per application)
- **specs/meta/**: Internal meta-specifications for system operation
- **specs/_review/**: Component and layer-specific specs for evaluation
  - Moved from old structure: backend/, frontend/, design/, examples/, experimental/, etc.
  - These represent partial specs that focus on technical layers rather than complete applications

## Development Notes

- Specs use markdown format with standardized 9-section structure for clarity and AI disambiguation
- Each spec represents a complete application, not a technical layer or component
- The tool dynamically loads AI modules using importlib for extensibility
- Simplified naming: specs are stored as `<spec_name>.md` in the root specs/ directory
- Shell command construction handles quote escaping for different AI tools
- Specs can be created from existing codebases using the `infer` command
- Refinement workflow allows iterative improvement of specifications
- Structured format reduces ambiguity and improves AI code generation quality
- Component-level specs moved to `_review/` directory for evaluation