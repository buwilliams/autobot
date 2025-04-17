def execute(template_path):
    # Return the CLI string for OpenAI Codex
    with open(template_path, 'r') as file:
        template = file.read()
    # Escape single quotes for shell: 'abc' -> 'a'"'"'b'"'"'c'
    escaped = template.replace("'", "'\"'\"'")
    return f"codex --approval-mode full-auto '{escaped}'"