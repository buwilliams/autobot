def execute(template_path):
    # Return the CLI string for OpenAI Codex
    with open(template_path, 'r') as file:
        template = file.read()
    return f"codex --quiet --approval-mode full-auto '{template}'"