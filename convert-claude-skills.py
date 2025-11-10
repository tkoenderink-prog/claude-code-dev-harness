#!/usr/bin/env python3
"""
Convert .claude/skills/ from categorized structure to flat structure
and fix frontmatter to use only name + description fields.
"""

import os
import re
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

def extract_frontmatter(content):
    """Extract YAML frontmatter from markdown content."""
    match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
    if not match:
        return {}, content

    frontmatter_text = match.group(1)
    body = match.group(2)

    # Parse YAML manually (simple key: value format)
    frontmatter = {}
    for line in frontmatter_text.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            frontmatter[key.strip()] = value.strip()

    return frontmatter, body

def generate_description(name, category, trigger, old_desc=None):
    """Generate a proper description with 'Use when...' format."""
    # Clean up the name for description
    skill_name = name.replace('-', ' ')

    # Use trigger if available, otherwise use name
    trigger_text = trigger if trigger and trigger != name else skill_name

    # Create description starting with "Use when"
    description = f"Use when working with {trigger_text} in your project"

    # Add category context if useful
    if category and category not in ['development', 'general']:
        description += f" - provides {category} best practices and implementation patterns"
    else:
        description += " - provides best practices and implementation patterns"

    return description

def convert_skill_file(source_file, temp_dir):
    """Convert a single skill file to new format."""
    try:
        # Read the file
        with open(source_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract frontmatter and body
        frontmatter, body = extract_frontmatter(content)

        if not frontmatter:
            print(f"  ⚠️  WARNING: {source_file.name} has no frontmatter")
            return None

        # Get skill name (without .md extension)
        skill_name = source_file.stem

        # Extract relevant fields
        name = frontmatter.get('name', skill_name)
        category = frontmatter.get('category', '')
        trigger = frontmatter.get('trigger', '')

        # Generate new description
        description = generate_description(name, category, trigger)

        # Create new frontmatter with only name and description
        new_frontmatter = f"""---
name: {name}
description: {description}
---
"""

        # Combine new frontmatter with body
        new_content = new_frontmatter + body

        # Create target directory
        target_dir = temp_dir / name
        target_dir.mkdir(exist_ok=True)

        # Write to SKILL.md
        target_file = target_dir / "SKILL.md"
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return name

    except Exception as e:
        print(f"  ❌ ERROR processing {source_file}: {e}")
        return None

def main():
    base_dir = Path.cwd()
    source_dir = base_dir / ".claude" / "skills"
    temp_dir = base_dir / ".claude" / "skills-converted"

    # Create temp directory
    temp_dir.mkdir(exist_ok=True)

    print("=== Converting .claude/skills/ to flat structure ===")
    print()

    # Find all .md files in categorized structure
    skill_files = list(source_dir.glob("*/*.md"))

    print(f"Found {len(skill_files)} skills to convert")
    print()

    # Convert skills in parallel
    converted = []
    failed = []

    with ThreadPoolExecutor(max_workers=8) as executor:
        # Submit all conversion tasks
        future_to_file = {
            executor.submit(convert_skill_file, skill_file, temp_dir): skill_file
            for skill_file in skill_files
        }

        # Process completed tasks
        for future in as_completed(future_to_file):
            skill_file = future_to_file[future]
            try:
                result = future.result()
                if result:
                    converted.append(result)
                    print(f"  ✅ Converted: {result}")
                else:
                    failed.append(skill_file.name)
            except Exception as e:
                failed.append(skill_file.name)
                print(f"  ❌ Failed: {skill_file.name} - {e}")

    print()
    print(f"=== Conversion Complete ===")
    print(f"Converted: {len(converted)} skills")
    print(f"Failed: {len(failed)} skills")
    print()
    print(f"Converted skills are in: {temp_dir}")
    print()

    return 0 if len(failed) == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
