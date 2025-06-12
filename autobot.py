#!/usr/bin/env python3
import sys
import os
import subprocess
import json
import glob
import re

import importlib.util

SPECS_DIR = os.path.join(os.path.dirname(__file__), 'specs')
AI_TOOLS_DIR = os.path.join(os.path.dirname(__file__), 'ai-tools')
META_DIR = os.path.join(os.path.dirname(__file__), 'meta')
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

def get_specs():
    try:
        return [f[:-3] for f in os.listdir(SPECS_DIR) 
                if f.endswith('.md') and os.path.isfile(os.path.join(SPECS_DIR, f))]
    except Exception:
        return []

def get_help_text():
    script_name = "autobot"  # Always show "autobot" regardless of how script is called
    pad = ' ' * (len(script_name) + 1)
    specs = get_specs()
    ai_tools = get_ai_tools()
    current_default = get_default_ai_tool()
    purpose = "Save, refine, and leverage application specs for AI-driven development."
    return f"""
{purpose}

Usage:
  {script_name}                                           Show this help message
  {script_name} help                                      Show this help message
  {script_name} generate <spec_name> [--ai-tool <tool>]   Generate application from spec
  {script_name} dryrun <spec_name> [--ai-tool <tool>]     Preview generation command
  {script_name} show <spec_name>                          Display spec content
  {script_name} ls                                        List available specs
  {script_name} create <spec_name>                        Create new spec from template
  {script_name} refine <spec_name> [--ai-tool <tool>]     Refine existing spec with AI enhancement
  {script_name} update <spec_name> [--path <dir>] [--ai-tool <tool>]  Update spec from current codebase (CAUTION)
  {script_name} infer <spec_name> [--path <dir>]          Infer spec from existing codebase
  {script_name} config default-ai-tool <tool>             Set default AI tool
  {script_name} config show                               Show current configuration

Available Specs: {', '.join(specs) if specs else 'None'}
AI Tools: {', '.join(ai_tools)} (default: {current_default})
"""

def show_help():
    print(get_help_text())

def list_specs():
    specs = get_specs()
    if specs:
        print("Available specs:")
        for spec in sorted(specs):
            print(f"  {spec}")
    else:
        print("No specs found.")

# Function removed - no longer needed with flattened structure

def parse_ai_tool(args):
    if '--ai-tool' in args:
        idx = args.index('--ai-tool')
        if idx+1 < len(args):
            return args[idx+1]
        else:
            print("Missing value for --ai-tool. Using default.")
    return get_default_ai_tool()

def build_generation_command(spec_name, ai_tool=None):
    if ai_tool is None:
        ai_tool = get_default_ai_tool()
    file_path = os.path.join(SPECS_DIR, f"{spec_name}.md")
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Spec '{spec_name}' not found.")
    module = get_ai_tool_module(ai_tool)
    if not hasattr(module, 'execute'):
        raise AttributeError(f"AI tool module '{ai_tool}' does not have an 'execute' method.")
    cmd = module.execute(file_path)
    return cmd

def generate_from_spec(spec_name, ai_tool=None):
    if ai_tool is None:
        ai_tool = get_default_ai_tool()
    try:
        cmd = build_generation_command(spec_name, ai_tool)
    except Exception as e:
        print(f"Error: {e}")
        return
    try:
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running generation command: {e}")

def show_spec(spec_name):
    file_path = os.path.join(SPECS_DIR, f"{spec_name}.md")
    if not os.path.isfile(file_path):
        print(f"Spec '{spec_name}' not found.")
        return
    with open(file_path, 'r') as f:
        print(f.read())

def dryrun_generation(spec_name, ai_tool=None):
    if ai_tool is None:
        ai_tool = get_default_ai_tool()
    try:
        cmd = build_generation_command(spec_name, ai_tool)
    except Exception as e:
        print(f"Error: {e}")
        return
    print("[DRYRUN] Command that would be executed:")
    print(cmd)

def create_spec(spec_name):
    file_path = os.path.join(SPECS_DIR, f"{spec_name}.md")
    if os.path.isfile(file_path):
        print(f"Spec '{spec_name}' already exists.")
        return
    
    # Create a default spec template
    default_spec = f"""# {spec_name.title()} Specification

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

def refine_spec(spec_name, ai_tool=None):
    """Intelligently refine an existing spec using AI analysis and enhancement"""
    file_path = os.path.join(SPECS_DIR, f"{spec_name}.md")
    if not os.path.isfile(file_path):
        print(f"Spec '{spec_name}' not found. Use 'create' to make a new spec.")
        return
    
    if ai_tool is None:
        ai_tool = get_default_ai_tool()
    
    print(f"Refining spec using AI analysis: {spec_name}")
    print(f"Using AI tool: {ai_tool}")
    
    # Check for refinement meta-spec
    meta_spec_path = os.path.join(META_DIR, 'spec-refiner.md')
    if not os.path.exists(meta_spec_path):
        print("Error: Meta-spec for spec refinement not found")
        print("Falling back to manual editing...")
        # Fallback to manual editing
        try:
            subprocess.run(['nano', file_path], check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            try:
                subprocess.run(['vim', file_path], check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                print(f"Could not open editor. Please manually edit: {file_path}")
        return
    
    try:
        # Read the meta-spec for refinement
        with open(meta_spec_path, 'r', encoding='utf-8') as f:
            meta_spec_content = f.read()
        
        # Read the current spec
        with open(file_path, 'r', encoding='utf-8') as f:
            current_spec_content = f.read()
        
        # Create a refinement prompt combining meta-spec with current spec
        refinement_prompt = f"""{meta_spec_content}

===============================================================================

CURRENT SPECIFICATION TO REFINE:

{current_spec_content}

===============================================================================

REFINEMENT INSTRUCTIONS:

Please analyze the above specification and refine it according to the refinement guidelines in the meta-specification. Focus on:

1. Ensuring it follows the standardized Autobot format where applicable
2. Improving clarity and technology-agnostic language
3. Adding missing sections that would be valuable for this application type
4. Omitting sections that are not applicable to this specific application
5. Enhancing content for better AI code generation

The application is named "{spec_name}". Please provide the complete refined specification, maintaining all original functional requirements while improving structure, clarity, and completeness.

Save the refined specification by overwriting the existing file at: {file_path}
"""
        
        # Create temporary file with refinement prompt
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as temp_file:
            temp_file.write(refinement_prompt)
            temp_file_path = temp_file.name
        
        try:
            # Use AI tool to refine the spec
            print("Analyzing and refining specification...")
            
            module = get_ai_tool_module(ai_tool)
            
            # Create appropriate command for refinement
            if ai_tool == 'claude':
                # Use the temp file directly with claude
                cmd = f"claude -p --allowedTools 'Bash,Edit,Write' < {temp_file_path}"
            else:
                # Fall back to the module's execute method for other tools
                cmd = module.execute(temp_file_path)
            
            # Execute the AI tool command
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("Specification refinement completed successfully")
                print(f"Refined spec saved to: {file_path}")
                print("Review the enhanced specification to ensure it meets your requirements.")
                
                # Show a brief summary of what was changed if there's output
                if result.stdout:
                    print("\nRefinement Summary:")
                    # Look for any summary or key changes mentioned in the output
                    lines = result.stdout.split('\n')
                    for line in lines[-10:]:  # Show last 10 lines for summary
                        if line.strip() and not line.startswith('claude'):
                            print(f"  {line}")
            else:
                print(f"Error during AI refinement: {result.stderr}")
                print("Falling back to manual editing...")
                # Fallback to manual editing on AI failure
                try:
                    subprocess.run(['nano', file_path], check=True)
                except (subprocess.CalledProcessError, FileNotFoundError):
                    try:
                        subprocess.run(['vim', file_path], check=True)
                    except (subprocess.CalledProcessError, FileNotFoundError):
                        print(f"Could not open editor. Please manually edit: {file_path}")
                return
                
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_file_path)
            except:
                pass
                
    except Exception as e:
        print(f"Error during spec refinement: {e}")
        print("Falling back to manual editing...")
        # Fallback to manual editing on any error
        try:
            subprocess.run(['nano', file_path], check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            try:
                subprocess.run(['vim', file_path], check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                print(f"Could not open editor. Please manually edit: {file_path}")
        return

def update_spec(spec_name, source_path=None, ai_tool=None):
    """Update an existing spec by analyzing current codebase and merging with existing content"""
    file_path = os.path.join(SPECS_DIR, f"{spec_name}.md")
    if not os.path.isfile(file_path):
        print(f"Spec '{spec_name}' not found. Use 'create' to make a new spec.")
        return
    
    # Use provided path or current directory
    analysis_path = source_path if source_path else "."
    
    if not os.path.exists(analysis_path):
        print(f"Path does not exist: {analysis_path}")
        return
    
    if ai_tool is None:
        ai_tool = get_default_ai_tool()
    
    # Display prominent warning
    print("⚠️  CAUTION: WHOLESALE SPEC UPDATE ⚠️")
    print("")
    print("This command will perform a comprehensive update of your specification")
    print("based on current codebase analysis. This may overwrite manual refinements")
    print("and carefully crafted content.")
    print("")
    print("BEFORE PROCEEDING:")
    print("- Backup your current specification")
    print("- Ensure team awareness of the update")
    print("- Plan time for thorough review of changes")
    print("- Consider using 'refine' command for smaller adjustments")
    print("")
    print("This update will:")
    print("✓ Analyze current codebase state")
    print("✓ Merge findings with existing specification")
    print("✓ Preserve business intent where possible")
    print("⚠️ May overwrite technical sections completely")
    print("⚠️ May modify carefully crafted content")
    print("")
    
    # Require explicit confirmation
    response = input("Continue? (y/N): ").strip().lower()
    if response not in ['y', 'yes']:
        print("Update cancelled.")
        return
    
    # Check for updater meta-spec
    meta_spec_path = os.path.join(META_DIR, 'spec-updater.md')
    if not os.path.exists(meta_spec_path):
        print("Error: Meta-spec for spec updating not found")
        return
    
    print(f"Updating spec: {spec_name}")
    print(f"Analyzing codebase at: {os.path.abspath(analysis_path)}")
    print(f"Using AI tool: {ai_tool}")
    
    try:
        # Read the meta-spec for updating
        with open(meta_spec_path, 'r', encoding='utf-8') as f:
            meta_spec_content = f.read()
        
        # Read the existing spec
        with open(file_path, 'r', encoding='utf-8') as f:
            existing_spec_content = f.read()
        
        # Create codebase summary
        codebase_summary = create_codebase_summary(analysis_path)
        
        # Create update prompt combining all three elements
        from datetime import datetime
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        update_prompt = f"""{meta_spec_content}

===============================================================================

EXISTING SPECIFICATION TO UPDATE:

{existing_spec_content}

===============================================================================

CURRENT CODEBASE ANALYSIS:

{codebase_summary}

===============================================================================

UPDATE INSTRUCTIONS:

Please perform an intelligent update of the existing specification based on the current codebase analysis, following the update guidelines in the meta-specification. 

Key Requirements:
1. Preserve human intent in Purpose, Goals, and business context sections
2. Update technical sections (Database Schema, Services, Endpoints, UI Layout, Pages) to reflect current codebase
3. Add new functionality discovered in codebase analysis
4. Flag any conflicts between existing spec and current code reality
5. Maintain technology-agnostic language and Autobot format standards
6. Include update summary showing what changed

The application is named "{spec_name}" and this update is being performed on {current_date}.

Save the updated specification by overwriting the existing file at: {file_path}

Include clear update notes documenting:
- What sections were modified and why
- New functionality that was added
- Any conflicts that need human review
- Content that was intentionally preserved
"""
        
        # Create temporary file with update prompt
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as temp_file:
            temp_file.write(update_prompt)
            temp_file_path = temp_file.name
        
        try:
            # Use AI tool to update the spec
            print("Performing intelligent spec update...")
            print("This may take a moment as we analyze the codebase and merge with existing spec...")
            
            module = get_ai_tool_module(ai_tool)
            
            # Create appropriate command for updating
            if ai_tool == 'claude':
                # Use the temp file directly with claude
                cmd = f"claude -p --allowedTools 'Bash,Edit,Write' < {temp_file_path}"
            else:
                # Fall back to the module's execute method for other tools
                cmd = module.execute(temp_file_path)
            
            # Execute the AI tool command
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Specification update completed successfully")
                print(f"Updated spec saved to: {file_path}")
                print("")
                print("🔍 IMPORTANT: Please review the updated specification carefully!")
                print("   - Check that business intent was preserved")
                print("   - Verify new functionality is accurate")
                print("   - Look for any flagged conflicts")
                print("   - Ensure technical details match current codebase")
                print("")
                print("Consider running 'autobot show {spec_name}' to review the updated content.")
                
                # Show a brief summary if available
                if result.stdout:
                    # Look for update summary in the output
                    lines = result.stdout.split('\n')
                    summary_started = False
                    for line in lines:
                        if 'update' in line.lower() and ('summary' in line.lower() or 'changes' in line.lower()):
                            summary_started = True
                        elif summary_started and line.strip():
                            print(f"  {line}")
                        elif summary_started and not line.strip():
                            break
            else:
                print(f"❌ Error during spec update: {result.stderr}")
                print("The original specification remains unchanged.")
                return
                
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_file_path)
            except:
                pass
                
    except Exception as e:
        print(f"Error during spec update: {e}")
        print("The original specification remains unchanged.")
        return

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

def create_codebase_summary(path="."):
    """Create a comprehensive summary of the codebase for AI analysis"""
    summary_parts = []
    
    # Add project overview
    summary_parts.append("=== CODEBASE ANALYSIS REQUEST ===")
    summary_parts.append(f"Please analyze the following codebase located at: {os.path.abspath(path)}")
    summary_parts.append("")
    
    # Read README if available
    readme_files = ['README.md', 'README.txt', 'README.rst', 'readme.md']
    for readme in readme_files:
        readme_path = os.path.join(path, readme)
        if os.path.exists(readme_path):
            try:
                with open(readme_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    summary_parts.append("=== README CONTENT ===")
                    summary_parts.append(content[:3000])  # First 3000 chars
                    summary_parts.append("")
                    break
            except:
                pass
    
    # Directory structure
    summary_parts.append("=== PROJECT STRUCTURE ===")
    for root, dirs, files in os.walk(path):
        # Skip hidden and common ignore directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv', 'env', 'dist', 'build', 'target']]
        
        level = root.replace(path, '').count(os.sep)
        indent = ' ' * 2 * level
        summary_parts.append(f"{indent}{os.path.basename(root)}/")
        
        # Limit depth to avoid overwhelming output
        if level < 3:
            subindent = ' ' * 2 * (level + 1)
            for file in files[:10]:  # Limit files per directory
                if not file.startswith('.'):
                    summary_parts.append(f"{subindent}{file}")
            if len(files) > 10:
                summary_parts.append(f"{subindent}... and {len(files) - 10} more files")
    
    summary_parts.append("")
    
    # Configuration files content
    config_files = []
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv', 'env']]
        for file in files:
            if file.lower() in ['package.json', 'requirements.txt', 'cargo.toml', 'go.mod', 'pom.xml', 'composer.json', 'gemfile', 'setup.py']:
                config_files.append(os.path.join(root, file))
    
    if config_files:
        summary_parts.append("=== CONFIGURATION FILES ===")
        for config_file in config_files[:5]:  # Limit to 5 config files
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    summary_parts.append(f"--- {os.path.relpath(config_file, path)} ---")
                    summary_parts.append(content[:1000])  # First 1000 chars
                    summary_parts.append("")
            except:
                pass
    
    # Sample source files
    source_extensions = ['.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.go', '.rs', '.php', '.rb']
    source_files = []
    
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv', 'env']]
        for file in files:
            if any(file.endswith(ext) for ext in source_extensions):
                source_files.append(os.path.join(root, file))
    
    if source_files:
        summary_parts.append("=== KEY SOURCE FILES (SAMPLES) ===")
        # Prioritize main files, routes, models
        priority_patterns = ['main', 'app', 'index', 'server', 'route', 'model', 'controller', 'service']
        
        priority_files = []
        other_files = []
        
        for file_path in source_files:
            file_name = os.path.basename(file_path).lower()
            if any(pattern in file_name for pattern in priority_patterns):
                priority_files.append(file_path)
            else:
                other_files.append(file_path)
        
        # Show priority files first, then others
        sample_files = priority_files[:3] + other_files[:2]  # Max 5 files
        
        for file_path in sample_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    summary_parts.append(f"--- {os.path.relpath(file_path, path)} ---")
                    summary_parts.append(content[:2000])  # First 2000 chars
                    summary_parts.append("")
            except:
                pass
    
    summary_parts.append("=== ANALYSIS INSTRUCTIONS ===")
    summary_parts.append("Based on the above codebase information, please generate a comprehensive application specification following the standardized Autobot format. Focus on understanding WHAT this application does functionally, rather than HOW it's implemented technically. Create a technology-agnostic specification that could be used to rebuild this application with completely different technologies while preserving all core functionality and user experience.")
    
    return "\n".join(summary_parts)

def parse_path_argument(args):
    """Parse --path argument from command line args"""
    if '--path' in args:
        idx = args.index('--path')
        if idx + 1 < len(args):
            return args[idx + 1]
        else:
            print("Missing value for --path. Using current directory.")
    return "."

def infer_spec(spec_name, source_path=None, ai_tool=None):
    """Infer a spec from an existing codebase using AI analysis"""
    
    # Use provided path or current directory
    analysis_path = source_path if source_path else "."
    
    if not os.path.exists(analysis_path):
        print(f"Path does not exist: {analysis_path}")
        return
    
    if ai_tool is None:
        ai_tool = get_default_ai_tool()
    
    print(f"Analyzing codebase at: {os.path.abspath(analysis_path)}")
    print(f"Using AI tool: {ai_tool}")
    
    # Create a temporary combined prompt file
    meta_spec_path = os.path.join(META_DIR, 'codebase-analyzer.md')
    if not os.path.exists(meta_spec_path):
        print("Error: Meta-spec for codebase analysis not found")
        return
    
    try:
        # Read the meta-spec
        with open(meta_spec_path, 'r', encoding='utf-8') as f:
            meta_spec_content = f.read()
        
        # Create codebase summary
        codebase_summary = create_codebase_summary(analysis_path)
        
        # Combine meta-spec with codebase summary
        combined_prompt = f"""{meta_spec_content}

===============================================================================

{codebase_summary}

===============================================================================

Please analyze the codebase information provided above and generate a complete application specification following the exact format outlined in the meta-specification. The specification should be for an application named "{spec_name}" and should be technology-agnostic while capturing all functional requirements.

Save the generated specification as "{spec_name}.md" in the Autobot specs system.
"""
        
        # Create temporary file with combined prompt
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as temp_file:
            temp_file.write(combined_prompt)
            temp_file_path = temp_file.name
        
        try:
            # Use AI tool to generate the spec
            print("Generating specification using AI analysis...")
            
            module = get_ai_tool_module(ai_tool)
            
            # For infer command, we need to handle the content differently
            # Instead of using the execute function directly, we'll construct a safer command
            if ai_tool == 'claude':
                # Use the temp file directly with claude
                cmd = f"claude -p --allowedTools 'Bash,Edit,Write' < {temp_file_path}"
            else:
                # Fall back to the module's execute method for other tools
                cmd = module.execute(temp_file_path)
            
            # Execute the AI tool command
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("AI analysis completed successfully")
                
                # Check if the spec was created by the AI tool
                spec_file_path = os.path.join(SPECS_DIR, f"{spec_name}.md")
                
                if os.path.exists(spec_file_path):
                    print(f"Generated spec: {spec_file_path}")
                    print("Review and refine the generated spec to match your specific requirements.")
                else:
                    print("Note: The AI tool completed but the spec file was not found in the expected location.")
                    print("The AI may have provided the specification in its output. Check the generated content.")
                    if result.stdout:
                        print("\nAI Tool Output:")
                        print(result.stdout)
            else:
                print(f"Error running AI tool: {result.stderr}")
                return
                
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_file_path)
            except:
                pass
                
    except Exception as e:
        print(f"Error during spec inference: {e}")
        return

def main():
    args = sys.argv[1:]
    if len(args) == 0 or (len(args) == 1 and args[0] == 'help'):
        show_help()
        return
    if args[0] == 'ls' and len(args) == 1:
        list_specs()
        return
    if args[0] == 'generate' and len(args) >= 2:
        ai_tool = parse_ai_tool(args)
        spec_name = args[1]
        generate_from_spec(spec_name, ai_tool)
        return
    if args[0] == 'dryrun' and len(args) >= 2:
        ai_tool = parse_ai_tool(args)
        spec_name = args[1]
        dryrun_generation(spec_name, ai_tool)
        return
    if args[0] == 'show' and len(args) == 2:
        show_spec(args[1])
        return
    if args[0] == 'create' and len(args) == 2:
        create_spec(args[1])
        return
    if args[0] == 'refine' and len(args) >= 2:
        ai_tool = parse_ai_tool(args)
        spec_name = args[1]
        refine_spec(spec_name, ai_tool)
        return
    if args[0] == 'update' and len(args) >= 2:
        ai_tool = parse_ai_tool(args)
        source_path = parse_path_argument(args)
        spec_name = args[1]
        update_spec(spec_name, source_path, ai_tool)
        return
    if args[0] == 'infer' and len(args) >= 2:
        ai_tool = parse_ai_tool(args)
        source_path = parse_path_argument(args)
        spec_name = args[1]
        infer_spec(spec_name, source_path, ai_tool)
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
