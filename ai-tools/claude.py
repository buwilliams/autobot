def execute(template_path):
    # Return the CLI string for Anthropic Claude Code
    with open(template_path, 'r') as file:
        template = file.read()
    return f"echo '{template}' | claude -p --allowedTools 'Bash,Edit,Write'"
