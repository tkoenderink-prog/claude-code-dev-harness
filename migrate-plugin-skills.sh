#!/bin/bash

# Source and destination
SRC="$HOME/.claude/plugins/cache/superpowers/skills"
DEST="./skills"

# Plugin skills to migrate (all 21)
SKILLS=(
  "brainstorming"
  "commands"
  "condition-based-waiting"
  "defense-in-depth"
  "dispatching-parallel-agents"
  "executing-plans"
  "finishing-a-development-branch"
  "receiving-code-review"
  "requesting-code-review"
  "root-cause-tracing"
  "sharing-skills"
  "subagent-driven-development"
  "systematic-debugging"
  "test-driven-development"
  "testing-anti-patterns"
  "testing-skills-with-subagents"
  "using-git-worktrees"
  "using-superpowers"
  "verification-before-completion"
  "writing-plans"
  "writing-skills"
)

# Copy each skill
copied=0
missing=0

for skill in "${SKILLS[@]}"; do
  if [ -d "$SRC/$skill" ]; then
    echo "Copying $skill..."
    cp -r "$SRC/$skill" "$DEST/"
    ((copied++))
  else
    echo "WARNING: $skill not found in $SRC"
    ((missing++))
  fi
done

echo ""
echo "Plugin skills migration complete:"
echo "  Copied: $copied skills"
echo "  Missing: $missing skills"
