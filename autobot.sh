#!/bin/bash
# autobot.sh - Progressively build frameworks and applications with Claude Code.
# Pass-through script to run autobot.py with all arguments

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$SCRIPT_DIR/autobot.py" "$@"
