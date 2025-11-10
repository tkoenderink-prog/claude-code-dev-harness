#!/bin/bash

# Sync skills from global and plugin sources

set -e

echo "=== Skills Synchronization ==="
echo ""

# Configuration
GLOBAL_SRC="$HOME/.claude/skills"
DEV_SKILLS_SRC="$HOME/.claude/plugins/cache/claude-dev-skills"
DEST="./.claude/skills"

# Exclude local-only skills
EXCLUDE_SKILLS=(
  "fixing-claude-code-hooks"  # Local only
)

# Function to check if skill should be excluded
should_exclude() {
  local skill="$1"
  for excluded in "${EXCLUDE_SKILLS[@]}"; do
    if [ "$skill" = "$excluded" ]; then
      return 0
    fi
  done
  return 1
}

# Sync global user skills
echo "Syncing global user skills from $GLOBAL_SRC..."
synced_count=0
for skill_dir in "$GLOBAL_SRC"/*; do
  skill=$(basename "$skill_dir")

  if should_exclude "$skill"; then
    echo "  SKIP: $skill (local-only)"
    continue
  fi

  if [ -d "$skill_dir" ]; then
    echo "  SYNC: $skill"
    rsync -a --delete "$skill_dir/" "$DEST/$skill/"
    ((synced_count++))
  fi
done
echo "Synced $synced_count global skills"
echo ""

# Sync development skills
echo "Syncing development skills from $DEV_SKILLS_SRC..."
synced_count=0
for skill_dir in "$DEV_SKILLS_SRC"/*; do
  skill=$(basename "$skill_dir")

  if [ -d "$skill_dir" ]; then
    echo "  SYNC: $skill"
    rsync -a --delete "$skill_dir/" "$DEST/$skill/"
    ((synced_count++))
  fi
done
echo "Synced $synced_count development skills"
echo ""

# Summary
total_skills=$(find "$DEST" -name "SKILL.md" | wc -l | tr -d ' ')
echo "=== Synchronization Complete ==="
echo "Total skills: $total_skills"
echo ""
echo "Run './check-skills-health.sh' to validate"
