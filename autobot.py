#!/usr/bin/env python3
import sys
import os
import subprocess

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), 'templates')

def get_types():
    try:
        return [d for d in os.listdir(TEMPLATES_DIR)
                if os.path.isdir(os.path.join(TEMPLATES_DIR, d))]
    except Exception:
        return []

def get_help_text():
    script_name = os.path.basename(sys.argv[0])
    pad = ' ' * (len(script_name) + 1)
    types = get_types()
    purpose = "Progressively build frameworks and applications with Claude Code."
    return f"""
{purpose}

Usage:
  {script_name}                                Show this help message
  {script_name} help                           Show this help message
  {script_name} run <type>:<template_name>     Run the template command
  {script_name} dryrun <type>:<template_name>  Show the command that would be run
  {script_name} show <type>:<template_name>    Print the template to STDOUT
  {script_name} list                           List available types
  {script_name} list <type>                    List available templates for a type

Types: {', '.join(types)}
"""

def show_help():
    print(get_help_text())

def list_types():
    types = get_types()
    if types:
        print("Available types:")
        for t in types:
            print(f"  {t}")
    else:
        print("No types found.")

def list_templates(t):
    dir_path = os.path.join(TEMPLATES_DIR, t)
    if not os.path.isdir(dir_path):
        print(f"Type '{t}' does not exist.")
        return
    files = [f[:-3] for f in os.listdir(dir_path)
             if f.endswith('.md') and os.path.isfile(os.path.join(dir_path, f))]
    if not files:
        print(f"No templates found for type '{t}'.")
    else:
        print(f"Available templates for '{t}':")
        for f in files:
            print(f"  {f}")

def run_template(arg):
    if ':' not in arg:
        print("Invalid format. Use <type>:<template_name>")
        return
    t, name = arg.split(':', 1)
    file_path = os.path.join(TEMPLATES_DIR, t, f"{name}.md")
    if not os.path.isfile(file_path):
        print(f"Template '{name}' not found for type '{t}'.")
        return
    cmd = f"python -c \"with open(\'{file_path}\', \'r\') as file: print(file.read())\" | claude -p --allowedTools \"Bash,Edit,Write\""
    try:
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running template command: {e}")

def show_template(arg):
    if ':' not in arg:
        print("Invalid format. Use <type>:<template_name>")
        return
    t, name = arg.split(':', 1)
    file_path = os.path.join(TEMPLATES_DIR, t, f"{name}.md")
    if not os.path.isfile(file_path):
        print(f"Template '{name}' not found for type '{t}'.")
        return
    with open(file_path, 'r') as f:
        print(f.read())

def dryrun_template(arg):
    if ':' not in arg:
        print("Invalid format. Use <type>:<template_name>")
        return
    t, name = arg.split(':', 1)
    file_path = os.path.join(TEMPLATES_DIR, t, f"{name}.md")
    if not os.path.isfile(file_path):
        print(f"Template '{name}' not found for type '{t}'.")
        return
    cmd = f"python -c \"with open(\'{file_path}\', \'r\') as file: print(file.read())\" | claude -p --allowedTools \"Bash,Edit,Write\""
    print("[DRYRUN] Command that would be executed:")
    print(cmd)

def main():
    if len(sys.argv) == 1 or (len(sys.argv) == 2 and sys.argv[1] == 'help'):
        show_help()
        return
    if sys.argv[1] == 'list' and len(sys.argv) == 2:
        list_types()
        return
    if sys.argv[1] == 'list' and len(sys.argv) == 3:
        t = sys.argv[2]
        list_templates(t)
        return
    if sys.argv[1] == 'run' and len(sys.argv) == 3:
        run_template(sys.argv[2])
        return
    if sys.argv[1] == 'dryrun' and len(sys.argv) == 3:
        dryrun_template(sys.argv[2])
        return
    if sys.argv[1] == 'show' and len(sys.argv) == 3:
        show_template(sys.argv[2])
        return
    show_help()

if __name__ == '__main__':
    main()
