#!/usr/bin/env python3
"""
Generate and execute skill renames with prefix scheme.
Maps skills to prefixes: dev-, think-, cc-, vault-, physical-
"""

import json
import os
import subprocess
from pathlib import Path
from collections import defaultdict

# Load categorization data
STATE_DIR = Path("/home/user/claude-code-dev-harness/.claude-state")
SKILLS_DIR = Path("/home/user/claude-code-dev-harness/.claude/skills")

with open(STATE_DIR / "skills-categorization.json") as f:
    data = json.load(f)

# Prefix mapping (update 'personal' to 'physical')
PREFIX_MAP = {
    "claude_code": "cc-",
    "software_dev": "dev-",
    "thinking_planning": "think-",
    "obsidian_vault": "vault-",
    "personal": "physical-",  # Changed from personal to physical
}

# Build skill -> prefix mapping
skill_to_prefix = {}
for category, skills in data["categorization"].items():
    prefix = PREFIX_MAP[category]
    for skill in skills:
        skill_to_prefix[skill] = prefix

# Get current skill directories (exclude non-skill items)
current_skills = [
    d.name for d in SKILLS_DIR.iterdir()
    if d.is_dir() and d.name not in ["README.md", "commands", "skill-evaluator"]
]

# Track renames, conflicts, already_correct
renames = {}
already_correct = []
not_in_categorization = []
conflicts = defaultdict(int)

print(f"Found {len(current_skills)} skills in directory")
print(f"Found {len(skill_to_prefix)} skills in categorization data\n")

# Process each skill
for skill_name in sorted(current_skills):
    # Check if already has a prefix
    if skill_name.startswith(("dev-", "think-", "cc-", "vault-", "physical-")):
        already_correct.append(skill_name)
        print(f"✓ Already correct: {skill_name}")
        continue

    # Look up prefix
    if skill_name not in skill_to_prefix:
        not_in_categorization.append(skill_name)
        print(f"⚠ Not in categorization: {skill_name}")
        continue

    prefix = skill_to_prefix[skill_name]
    new_name = f"{prefix}{skill_name}"

    # Check for conflicts
    if (SKILLS_DIR / new_name).exists():
        conflicts[new_name] += 1
        new_name = f"{prefix}{skill_name}-{conflicts[new_name]}"
        print(f"⚠ Conflict resolved: {skill_name} -> {new_name}")

    renames[skill_name] = new_name

print(f"\n{'='*60}")
print(f"Summary before execution:")
print(f"{'='*60}")
print(f"To rename: {len(renames)}")
print(f"Already correct: {len(already_correct)}")
print(f"Not in categorization: {len(not_in_categorization)}")
print(f"Total accounted: {len(renames) + len(already_correct) + len(not_in_categorization)}")
print(f"Total in directory: {len(current_skills)}")

# Count by prefix
prefix_counts = defaultdict(int)
for new_name in renames.values():
    for prefix in PREFIX_MAP.values():
        if new_name.startswith(prefix):
            prefix_counts[prefix] += 1
            break

for skill in already_correct:
    for prefix in PREFIX_MAP.values():
        if skill.startswith(prefix):
            prefix_counts[prefix] += 1
            break

print(f"\nSkills per category (after renames):")
for prefix_name, prefix in PREFIX_MAP.items():
    count = prefix_counts[prefix]
    print(f"  {prefix_name:20} ({prefix}): {count}")

print(f"\n{'='*60}")
print("Executing renames with git mv...")
print(f"{'='*60}\n")

# Execute renames using two-step process (mv + git add) to avoid cross-device link issues
success_count = 0
failed_renames = []

for old_name, new_name in sorted(renames.items()):
    old_path = SKILLS_DIR / old_name
    new_path = SKILLS_DIR / new_name

    try:
        # Step 1: Move the directory
        mv_result = subprocess.run(
            ["mv", str(old_path), str(new_path)],
            cwd="/home/user/claude-code-dev-harness",
            capture_output=True,
            text=True,
            check=True
        )

        # Step 2: Stage the deletion and addition with git
        rm_result = subprocess.run(
            ["git", "rm", "-r", f".claude/skills/{old_name}"],
            cwd="/home/user/claude-code-dev-harness",
            capture_output=True,
            text=True,
            check=True
        )

        add_result = subprocess.run(
            ["git", "add", f".claude/skills/{new_name}"],
            cwd="/home/user/claude-code-dev-harness",
            capture_output=True,
            text=True,
            check=True
        )

        print(f"✓ {old_name} -> {new_name}")
        success_count += 1
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed: {old_name} -> {new_name}")
        print(f"  Error: {e.stderr}")
        failed_renames.append((old_name, new_name, str(e.stderr)))

        # Try to rollback if mv succeeded but git commands failed
        if new_path.exists():
            try:
                subprocess.run(["mv", str(new_path), str(old_path)], check=False)
            except:
                pass

print(f"\n{'='*60}")
print(f"Execution complete:")
print(f"{'='*60}")
print(f"Successful: {success_count}/{len(renames)}")
print(f"Failed: {len(failed_renames)}")

if failed_renames:
    print("\nFailed renames:")
    for old, new, error in failed_renames:
        print(f"  {old} -> {new}: {error}")

# Save mapping file
mapping_file = STATE_DIR / "skill-renames.json"
mapping_data = {
    "renames": renames,
    "already_correct": already_correct,
    "not_in_categorization": not_in_categorization,
    "failed": [{"old": old, "new": new, "error": err} for old, new, err in failed_renames],
    "statistics": {
        "total_skills": len(current_skills),
        "renamed": success_count,
        "already_correct": len(already_correct),
        "not_in_categorization": len(not_in_categorization),
        "failed": len(failed_renames),
        "by_prefix": dict(prefix_counts)
    }
}

with open(mapping_file, "w") as f:
    json.dump(mapping_data, f, indent=2)

print(f"\nMapping saved to: {mapping_file}")
