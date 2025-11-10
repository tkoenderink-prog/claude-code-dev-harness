#!/bin/bash

# Validate skills directory health

set -e

echo "=== Skills Health Check ==="
echo ""

SKILLS_DIR="./skills"
errors=0
warnings=0

# Check 1: All skills have SKILL.md
echo "Check 1: Verifying SKILL.md files..."
for skill_dir in "$SKILLS_DIR"/*; do
  if [ -d "$skill_dir" ]; then
    skill=$(basename "$skill_dir")

    # Skip README.md and special directories
    if [ "$skill" = "README.md" ] || [ "$skill" = "commands" ]; then
      continue
    fi

    if [ ! -f "$skill_dir/SKILL.md" ]; then
      echo "  ❌ ERROR: $skill missing SKILL.md"
      ((errors++))
    fi
  fi
done

# Check 2: Frontmatter validation
echo "Check 2: Validating frontmatter..."
for skill_file in "$SKILLS_DIR"/*/SKILL.md; do
  skill=$(basename "$(dirname "$skill_file")")

  # Check for name field
  if ! grep -q "^name:" "$skill_file"; then
    echo "  ❌ ERROR: $skill missing 'name' field"
    ((errors++))
  fi

  # Check for description field
  if ! grep -q "^description:" "$skill_file"; then
    echo "  ❌ ERROR: $skill missing 'description' field"
    ((errors++))
  fi

  # Check for unsupported fields
  if grep -qE "^(category|trigger|expertise|time_estimate|dependencies):" "$skill_file"; then
    echo "  ⚠️  WARNING: $skill has unsupported frontmatter fields"
    ((warnings++))
  fi
done

# Check 3: Directory naming
echo "Check 3: Checking directory naming..."
for skill_dir in "$SKILLS_DIR"/*; do
  if [ -d "$skill_dir" ]; then
    skill=$(basename "$skill_dir")

    # Check for non-kebab-case
    if [[ ! "$skill" =~ ^[a-z0-9-]+$ ]]; then
      echo "  ⚠️  WARNING: $skill not in kebab-case"
      ((warnings++))
    fi
  fi
done

# Summary
total_skills=$(find "$SKILLS_DIR" -name "SKILL.md" | wc -l | tr -d ' ')
echo ""
echo "=== Health Check Complete ==="
echo "Total skills: $total_skills"
echo "Errors: $errors"
echo "Warnings: $warnings"
echo ""

if [ $errors -eq 0 ]; then
  echo "✅ All checks passed!"
  exit 0
else
  echo "❌ Found $errors errors that need fixing"
  exit 1
fi
