#!/usr/bin/env python3
import sys
import os
import subprocess
import json

import importlib.util

SPECS_DIR = os.path.join(os.path.dirname(__file__), 'specs')
AI_TOOLS_DIR = os.path.join(os.path.dirname(__file__), 'ai-tools')
CONFIG_FILE = os.path.join(os.path.dirname(__file__), '.autobot-config.json')
DEFAULT_AI_TOOL = 'claude'

def get_ai_tools():
    try:
        return [f[:-3] for f in os.listdir(AI_TOOLS_DIR) if f.endswith('.py')]
    except Exception:
        return []

def load_config():
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
    except Exception:
        pass
    return {}

def save_config(config):
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
        return True
    except Exception:
        return False

def get_default_ai_tool():
    config = load_config()
    return config.get('default_ai_tool', DEFAULT_AI_TOOL)

def set_default_ai_tool(ai_tool):
    available_tools = get_ai_tools()
    if ai_tool not in available_tools:
        raise ValueError(f"AI tool '{ai_tool}' not found. Available: {', '.join(available_tools)}")
    
    config = load_config()
    config['default_ai_tool'] = ai_tool
    if save_config(config):
        return True
    else:
        raise Exception("Failed to save configuration")

def get_ai_tool_module(ai_tool):
    tool_file = os.path.join(AI_TOOLS_DIR, f"{ai_tool}.py")
    if not os.path.isfile(tool_file):
        raise ValueError(f"AI tool '{ai_tool}' not found. Available: {', '.join(get_ai_tools())}")
    spec = importlib.util.spec_from_file_location(f"ai_tools.{ai_tool}", tool_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def get_spec_types():
    try:
        return [d for d in os.listdir(SPECS_DIR)
                if os.path.isdir(os.path.join(SPECS_DIR, d))]
    except Exception:
        return []

def get_help_text():
    script_name = "autobot"  # Always show "autobot" regardless of how script is called
    pad = ' ' * (len(script_name) + 1)
    spec_types = get_spec_types()
    ai_tools = get_ai_tools()
    current_default = get_default_ai_tool()
    purpose = "Save, refine, and leverage application specs for AI-driven development."
    return f"""
{purpose}

Usage:
  {script_name}                                                Show this help message
  {script_name} help                                           Show this help message
  {script_name} generate <type>:<spec_name> [--ai-tool <tool>] Generate application from spec
  {script_name} dryrun <type>:<spec_name> [--ai-tool <tool>]   Preview generation command
  {script_name} show <type>:<spec_name>                        Display spec content
  {script_name} ls                                             List available spec types
  {script_name} ls <type>                                      List specs for a type
  {script_name} create <type>:<spec_name>                      Create new spec from template
  {script_name} refine <type>:<spec_name>                      Refine existing spec
  {script_name} config default-ai-tool <tool>                  Set default AI tool
  {script_name} config show                                    Show current configuration

Spec Types: {', '.join(spec_types)}
AI Tools: {', '.join(ai_tools)} (default: {current_default})
"""

def show_help():
    print(get_help_text())

def list_spec_types():
    spec_types = get_spec_types()
    if spec_types:
        print("Available spec types:")
        for t in spec_types:
            print(f"  {t}")
    else:
        print("No spec types found.")

def list_specs(t):
    dir_path = os.path.join(SPECS_DIR, t)
    if not os.path.isdir(dir_path):
        print(f"Spec type '{t}' does not exist.")
        return
    files = [f[:-3] for f in os.listdir(dir_path)
             if f.endswith('.md') and os.path.isfile(os.path.join(dir_path, f))]
    if not files:
        print(f"No specs found for type '{t}'.")
    else:
        print(f"Available specs for '{t}':")
        for f in files:
            print(f"  {f}")

def parse_ai_tool(args):
    if '--ai-tool' in args:
        idx = args.index('--ai-tool')
        if idx+1 < len(args):
            return args[idx+1]
        else:
            print("Missing value for --ai-tool. Using default.")
    return get_default_ai_tool()

def build_generation_command(arg, ai_tool=None):
    if ai_tool is None:
        ai_tool = get_default_ai_tool()
    if ':' not in arg:
        raise ValueError("Invalid format. Use <type>:<spec_name>")
    t, name = arg.split(':', 1)
    file_path = os.path.join(SPECS_DIR, t, f"{name}.md")
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Spec '{name}' not found for type '{t}'.")
    module = get_ai_tool_module(ai_tool)
    if not hasattr(module, 'execute'):
        raise AttributeError(f"AI tool module '{ai_tool}' does not have an 'execute' method.")
    cmd = module.execute(file_path)
    return cmd

def generate_from_spec(arg, ai_tool=None):
    if ai_tool is None:
        ai_tool = get_default_ai_tool()
    try:
        cmd = build_generation_command(arg, ai_tool)
    except Exception as e:
        print(f"Error: {e}")
        return
    try:
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running generation command: {e}")

def show_spec(arg):
    if ':' not in arg:
        print("Invalid format. Use <type>:<spec_name>")
        return
    t, name = arg.split(':', 1)
    file_path = os.path.join(SPECS_DIR, t, f"{name}.md")
    if not os.path.isfile(file_path):
        print(f"Spec '{name}' not found for type '{t}'.")
        return
    with open(file_path, 'r') as f:
        print(f.read())

def dryrun_generation(arg, ai_tool=None):
    if ai_tool is None:
        ai_tool = get_default_ai_tool()
    try:
        cmd = build_generation_command(arg, ai_tool)
    except Exception as e:
        print(f"Error: {e}")
        return
    print("[DRYRUN] Command that would be executed:")
    print(cmd)

def create_spec(arg):
    if ':' not in arg:
        print("Invalid format. Use <type>:<spec_name>")
        return
    t, name = arg.split(':', 1)
    
    spec_type_dir = os.path.join(SPECS_DIR, t)
    if not os.path.isdir(spec_type_dir):
        os.makedirs(spec_type_dir)
    
    file_path = os.path.join(spec_type_dir, f"{name}.md")
    if os.path.isfile(file_path):
        print(f"Spec '{name}' already exists for type '{t}'.")
        return
    
    # Create a default spec template
    default_spec = f"""# {name.title()} Specification

## Purpose
Brief description of what this application does and why it exists.

## Goals
- Primary objective 1
- Primary objective 2
- Primary objective 3

## Use Cases
1. **Use Case 1**: Description of primary user interaction
2. **Use Case 2**: Description of secondary user interaction
3. **Use Case 3**: Description of edge case or special scenario

## Usage Rules
- Rule about how the application should behave
- Constraint or limitation to consider
- Performance or security requirement

## Database Schema
```sql
-- Define your database tables here
-- Example:
-- CREATE TABLE users (
--     id SERIAL PRIMARY KEY,
--     email VARCHAR(255) UNIQUE NOT NULL,
--     created_at TIMESTAMP DEFAULT NOW()
-- );
```

## Services
- **Service 1**: Description of core service functionality
- **Service 2**: Description of supporting service
- **Service 3**: Description of integration service

## Endpoints
### REST API Endpoints
- `GET /api/resource` - Description
- `POST /api/resource` - Description
- `PUT /api/resource/:id` - Description
- `DELETE /api/resource/:id` - Description

## UI Layout
### Main Components
- **Header**: Navigation and user controls
- **Sidebar**: Secondary navigation or filters
- **Main Content**: Primary application interface
- **Footer**: Additional links and information

## Pages
1. **Home Page** (`/`): Landing page with overview
2. **Dashboard** (`/dashboard`): Main application interface
3. **Settings** (`/settings`): User configuration
4. **About** (`/about`): Application information

## Technical Requirements
- Framework preferences
- Database requirements
- Authentication needs
- Deployment considerations
"""
    
    with open(file_path, 'w') as f:
        f.write(default_spec)
    
    print(f"Created new spec: {file_path}")

def refine_spec(arg):
    if ':' not in arg:
        print("Invalid format. Use <type>:<spec_name>")
        return
    t, name = arg.split(':', 1)
    file_path = os.path.join(SPECS_DIR, t, f"{name}.md")
    if not os.path.isfile(file_path):
        print(f"Spec '{name}' not found for type '{t}'. Use 'create' to make a new spec.")
        return
    
    print(f"Opening spec for refinement: {file_path}")
    print("Use your preferred editor to refine the spec, or use AI tools to help improve it.")
    
    # Could integrate with AI tools here to help refine specs
    try:
        subprocess.run(['nano', file_path], check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        try:
            subprocess.run(['vim', file_path], check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"Could not open editor. Please manually edit: {file_path}")

def show_config():
    config = load_config()
    current_default = get_default_ai_tool()
    available_tools = get_ai_tools()
    
    print("Current Configuration:")
    print(f"  Default AI Tool: {current_default}")
    print(f"  Available AI Tools: {', '.join(available_tools)}")
    print(f"  Config File: {CONFIG_FILE}")

def set_config_default_ai_tool(ai_tool):
    try:
        set_default_ai_tool(ai_tool)
        print(f"Default AI tool set to: {ai_tool}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error saving configuration: {e}")

def main():
    args = sys.argv[1:]
    if len(args) == 0 or (len(args) == 1 and args[0] == 'help'):
        show_help()
        return
    if args[0] == 'ls' and len(args) == 1:
        list_spec_types()
        return
    if args[0] == 'ls' and len(args) == 2:
        t = args[1]
        list_specs(t)
        return
    if args[0] == 'generate' and len(args) >= 2:
        ai_tool = parse_ai_tool(args)
        arg = args[1]
        generate_from_spec(arg, ai_tool)
        return
    if args[0] == 'dryrun' and len(args) >= 2:
        ai_tool = parse_ai_tool(args)
        arg = args[1]
        dryrun_generation(arg, ai_tool)
        return
    if args[0] == 'show' and len(args) == 2:
        show_spec(args[1])
        return
    if args[0] == 'create' and len(args) == 2:
        create_spec(args[1])
        return
    if args[0] == 'refine' and len(args) == 2:
        refine_spec(args[1])
        return
    if args[0] == 'config' and len(args) >= 2:
        if args[1] == 'show':
            show_config()
            return
        elif args[1] == 'default-ai-tool' and len(args) == 3:
            set_config_default_ai_tool(args[2])
            return
        else:
            print("Invalid config command. Use 'config show' or 'config default-ai-tool <tool>'")
            return
    show_help()

if __name__ == '__main__':
    main()
