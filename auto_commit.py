#!/usr/bin/env python3
"""
Auto-commit script that generates meaningful commit messages from git changes.
Excludes changes in the docs folder.
"""

import subprocess
import sys
import argparse
from pathlib import Path
from collections import defaultdict


def run_command(cmd, capture_output=True):
    """Run a shell command and return output."""
    result = subprocess.run(cmd, shell=True, capture_output=capture_output, text=True)
    if result.returncode != 0 and capture_output:
        print(f"Error running command: {cmd}")
        print(f"Error: {result.stderr}")
        return None
    return result.stdout.strip() if capture_output else result.returncode


def get_changed_files(exclude_folders=None):
    """Get list of changed files, excluding specified folders."""
    if exclude_folders is None:
        exclude_folders = ['docs']
    
    output = run_command("git status --porcelain")
    if not output:
        return []
    
    files = []
    for line in output.split('\n'):
        if not line:
            continue
        status = line[:2]
        filepath = line[3:]
        
        # Exclude specified folders
        skip = False
        for folder in exclude_folders:
            if filepath.startswith(f"{folder}/"):
                skip = True
                break
        if skip:
            continue
        
        files.append((status, filepath))
    
    return files


def categorize_changes(files):
    """Categorize changes by type."""
    categories = defaultdict(list)
    
    for status, filepath in files:
        status_code = status.strip()
        filename = Path(filepath).name
        
        if status_code.startswith('A'):
            categories['added'].append(filepath)
        elif status_code.startswith('D'):
            categories['deleted'].append(filepath)
        elif status_code.startswith('M'):
            categories['modified'].append(filepath)
        elif status_code.startswith('R'):
            categories['renamed'].append(filepath)
        else:
            categories['modified'].append(filepath)
    
    return categories


def get_file_types(files):
    """Extract file types from list of files."""
    types = set()
    for filepath in files:
        ext = Path(filepath).suffix
        if ext:
            types.add(ext.lstrip('.'))
        elif '.' not in Path(filepath).name:
            # Files without extension
            types.add(Path(filepath).name)
    return types


def generate_commit_message(categories):
    """Generate a meaningful commit message from categorized changes."""
    if not categories:
        return "Update project files"
    
    parts = []
    
    # Count changes by category
    added = categories.get('added', [])
    deleted = categories.get('deleted', [])
    modified = categories.get('modified', [])
    renamed = categories.get('renamed', [])
    
    # Build message based on what changed
    messages = []
    
    if added:
        add_types = get_file_types(added)
        if len(added) == 1:
            messages.append(f"Add {Path(added[0]).name}")
        else:
            file_desc = ", ".join(sorted(add_types))
            messages.append(f"Add {len(added)} files ({file_desc})")
    
    if deleted:
        if len(deleted) == 1:
            messages.append(f"Remove {Path(deleted[0]).name}")
        else:
            messages.append(f"Remove {len(deleted)} files")
    
    if modified:
        mod_types = get_file_types(modified)
        if len(modified) == 1:
            messages.append(f"Update {Path(modified[0]).name}")
        else:
            file_desc = ", ".join(sorted(mod_types))
            messages.append(f"Update {len(modified)} files ({file_desc})")
    
    if renamed:
        messages.append(f"Rename {len(renamed)} files")
    
    # Combine messages
    if len(messages) == 1:
        commit_msg = messages[0]
    else:
        commit_msg = "; ".join(messages)
    
    return commit_msg


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Auto-commit with smart commit messages",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python auto_commit.py                           # Exclude docs (default)
  python auto_commit.py --exclude docs _build    # Exclude docs and _build
  python auto_commit.py --exclude ""              # Exclude nothing
        """
    )
    parser.add_argument(
        '--exclude',
        nargs='+',
        default=['docs'],
        help='Folders to exclude from commit (default: docs)'
    )
    
    args = parser.parse_args()
    
    # Handle empty exclude list
    exclude_folders = args.exclude if args.exclude != [''] else []
    
    print("Analyzing git changes...")
    
    changed_files = get_changed_files(exclude_folders)
    
    if not changed_files:
        exclude_str = f" (excluding {', '.join(exclude_folders)})" if exclude_folders else ""
        print(f"No changes to commit{exclude_str}.")
        return 0
    
    print(f"\nFound {len(changed_files)} changed file(s):")
    for status, filepath in changed_files:
        print(f"  {status} {filepath}")
    
    categories = categorize_changes(changed_files)
    commit_message = generate_commit_message(categories)
    
    print(f"\nGenerated commit message: {commit_message}")
    
    # Ask for confirmation
    response = input("\nProceed with commit? (y/n): ").strip().lower()
    if response != 'y':
        print("Commit cancelled.")
        return 1
    
    # Add files (excluding specified folders)
    print("\nAdding files...")
    for status, filepath in changed_files:
        run_command(f"git add \"{filepath}\"", capture_output=False)
    
    # Commit
    print("Creating commit...")
    exit_code = run_command(f"git commit -m \"{commit_message}\"", capture_output=False)
    
    if exit_code == 0:
        print(f"✓ Commit successful: '{commit_message}'")
        return 0
    else:
        print("✗ Commit failed.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
