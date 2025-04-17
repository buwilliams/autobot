#!/usr/bin/env python3
import sys
import os
import subprocess

import importlib.util

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), 'templates')
AI_TOOLS_DIR = os.path.join(os.path.dirname(__file__), 'ai-tools')
DEFAULT_AI_TOOL = 'codex'

def get_ai_tools():
    try:
        return [f[:-3] for f in os.listdir(AI_TOOLS_DIR) if f.endswith('.py')]
    except Exception:
        return []

def get_ai_tool_module(ai_tool):
    tool_file = os.path.join(AI_TOOLS_DIR, f"{ai_tool}.py")
    if not os.path.isfile(tool_file):
        raise ValueError(f"AI tool '{ai_tool}' not found. Available: {', '.join(get_ai_tools())}")
    spec = importlib.util.spec_from_file_location(f"ai_tools.{ai_tool}", tool_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

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
    ai_tools = get_ai_tools()
    purpose = "Progressively build frameworks and applications with Claude Code."
    return f"""
{purpose}

Usage:
  {script_name}                                                     Show this help message
  {script_name} help                                                Show this help message
  {script_name} run <type>:<template_name> [--ai-tool <engine>]     Run the template command
  {script_name} dryrun <type>:<template_name> [--ai-tool <engine>]  Show the command that would be run
  {script_name} show <type>:<template_name>                         Print the template to STDOUT
  {script_name} ls                                                  List available types
  {script_name} ls <type>                                           List available templates for a type

Types: {', '.join(types)}
AI Tools: {', '.join(ai_tools)} (default: {DEFAULT_AI_TOOL})
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

def parse_ai_tool(args):
    if '--ai-tool' in args:
        idx = args.index('--ai-tool')
        if idx+1 < len(args):
            return args[idx+1]
        else:
            print("Missing value for --ai-tool. Using default.")
    return DEFAULT_AI_TOOL

def build_template_command(arg, ai_tool=DEFAULT_AI_TOOL):
    if ':' not in arg:
        raise ValueError("Invalid format. Use <type>:<template_name>")
    t, name = arg.split(':', 1)
    file_path = os.path.join(TEMPLATES_DIR, t, f"{name}.md")
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Template '{name}' not found for type '{t}'.")
    module = get_ai_tool_module(ai_tool)
    if not hasattr(module, 'execute'):
        raise AttributeError(f"AI tool module '{ai_tool}' does not have an 'execute' method.")
    cmd = module.execute(file_path)
    return cmd

def run_template(arg, ai_tool=DEFAULT_AI_TOOL):
    try:
        cmd = build_template_command(arg, ai_tool)
    except Exception as e:
        print(f"Error: {e}")
        return
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

def dryrun_template(arg, ai_tool=DEFAULT_AI_TOOL):
    try:
        cmd = build_template_command(arg, ai_tool)
    except Exception as e:
        print(f"Error: {e}")
        return
    print("[DRYRUN] Command that would be executed:")
    print(cmd)

def main():
    args = sys.argv[1:]
    if len(args) == 0 or (len(args) == 1 and args[0] == 'help'):
        show_help()
        return
    if args[0] == 'ls' and len(args) == 1:
        list_types()
        return
    if args[0] == 'ls' and len(args) == 2:
        t = args[1]
        list_templates(t)
        return
    if args[0] == 'run' and len(args) >= 2:
        ai_tool = parse_ai_tool(args)
        arg = args[1]
        run_template(arg, ai_tool)
        return
    if args[0] == 'dryrun' and len(args) >= 2:
        ai_tool = parse_ai_tool(args)
        arg = args[1]
        dryrun_template(arg, ai_tool)
        return
    if args[0] == 'show' and len(args) == 2:
        show_template(args[1])
        return
    show_help()

if __name__ == '__main__':
    main()
