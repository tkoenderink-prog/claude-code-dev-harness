---
description: Push harness improvements back to central repository
---

# Harness Contribution (Push)

You are helping the user contribute harness improvements back to the central repository.

## Process

Execute these steps to create a pull request with the user's improvements.

### Step 1: Load Configuration

Read `.claude/VERSION.lock` to get the repository URL.

### Step 2: Clone Central Repository

```bash
REPO_URL=$(grep "repo_url:" .claude/VERSION.lock | cut -d' ' -f2)

cd /tmp
rm -rf harness-remote
git clone $REPO_URL harness-remote
cd harness-remote
```

### Step 3: Detect Changed Core Files

Compare each core file (non-PROJ-) with remote:

```bash
CHANGED_FILES=()

# Check agents
for file in $CLAUDE_PROJECT_DIR/.claude/agents/*.md; do
  filename=$(basename "$file")
  if [[ ! $filename =~ ^PROJ- ]]; then
    if [ -f "agents/$filename" ]; then
      if ! diff -q "$file" "agents/$filename" > /dev/null 2>&1; then
        CHANGED_FILES+=("agents/$filename")
      fi
    fi
  fi
done

# Check skills
for category in $CLAUDE_PROJECT_DIR/.claude/skills/*/; do
  category_name=$(basename "$category")
  for file in "$category"*.md; do
    filename=$(basename "$file")
    if [[ ! $filename =~ ^PROJ- ]]; then
      if [ -f "skills/$category_name/$filename" ]; then
        if ! diff -q "$file" "skills/$category_name/$filename" > /dev/null 2>&1; then
          CHANGED_FILES+=("skills/$category_name/$filename")
        fi
      fi
    fi
  done
done

# Check templates
for file in $CLAUDE_PROJECT_DIR/.claude/templates/*.md; do
  filename=$(basename "$file")
  if [[ ! $filename =~ ^PROJ- ]]; then
    if [ -f "templates/$filename" ]; then
      if ! diff -q "$file" "templates/$filename" > /dev/null 2>&1; then
        CHANGED_FILES+=("templates/$filename")
      fi
    fi
  fi
done

# Check commands
for file in $CLAUDE_PROJECT_DIR/.claude/commands/*.md; do
  filename=$(basename "$file")
  if [[ ! $filename =~ ^PROJ- ]]; then
    if [ -f "commands/$filename" ]; then
      if ! diff -q "$file" "commands/$filename" > /dev/null 2>&1; then
        CHANGED_FILES+=("commands/$filename")
      fi
    fi
  fi
done

# Check hooks
for file in $CLAUDE_PROJECT_DIR/.claude/hooks/*; do
  filename=$(basename "$file")
  if [[ ! $filename =~ ^PROJ- ]]; then
    if [ -f "hooks/$filename" ]; then
      if ! diff -q "$file" "hooks/$filename" > /dev/null 2>&1; then
        CHANGED_FILES+=("hooks/$filename")
      fi
    fi
  fi
done
```

If no changes found:
```
ℹ️  No harness improvements detected.

All core files match the central repository.
Only project-specific (PROJ-) files have changes.

To contribute improvements:
1. Modify core harness files (agents, skills, templates, etc.)
2. Test thoroughly in your project
3. Run /harness-push again
```

### Step 4: Show Changes to User

For each changed file, show diff preview:

```bash
for file in "${CHANGED_FILES[@]}"; do
  echo "📝 $file:"
  diff -u "/tmp/harness-remote/$file" "$CLAUDE_PROJECT_DIR/.claude/$file" | head -n 30
  echo ""
done
```

Display summary:
```
📤 Detected ${#CHANGED_FILES[@]} modified core files:
$(for f in "${CHANGED_FILES[@]}"; do echo "  - $f"; done)

Changes preview shown above (first 30 lines of each diff).
```

### Step 5: Gather Contribution Details

Ask the user three questions:

1. **Change type**:
   - `patch` - Bug fix (version x.y.Z+1)
   - `minor` - New feature (version x.Y+1.0)
   - `major` - Breaking change (version X+1.0.0)

2. **Description**: Brief description of changes (1-2 sentences)

3. **Breaking changes**: Any breaking changes? (yes/no, if yes, describe)

### Step 6: Calculate New Version

```bash
CURRENT=$(cat /tmp/harness-remote/VERSION)
IFS='.' read -r MAJOR MINOR PATCH <<< "$CURRENT"

case $CHANGE_TYPE in
  patch)
    PATCH=$((PATCH + 1))
    ;;
  minor)
    MINOR=$((MINOR + 1))
    PATCH=0
    ;;
  major)
    MAJOR=$((MAJOR + 1))
    MINOR=0
    PATCH=0
    ;;
esac

NEW_VERSION="$MAJOR.$MINOR.$PATCH"
echo "Version: $CURRENT → $NEW_VERSION"
```

### Step 7: Create Contribution Branch

```bash
cd /tmp/harness-remote
BRANCH="claude/contribution-$(date +%Y%m%d-%H%M%S)"
git checkout -b $BRANCH
```

### Step 8: Copy Changed Files

```bash
for file in "${CHANGED_FILES[@]}"; do
  mkdir -p "$(dirname "$file")"
  cp "$CLAUDE_PROJECT_DIR/.claude/$file" "$file"
done
```

### Step 9: Update VERSION File

```bash
echo "$NEW_VERSION" > VERSION
```

### Step 10: Update CHANGELOG.md

Insert new entry at the top:

```bash
# Read current changelog (skip first line with # Changelog)
CURRENT_CHANGELOG=$(tail -n +2 CHANGELOG.md)

# Create new changelog with new entry
cat > CHANGELOG.md << EOF
# Changelog

## [$NEW_VERSION] - $(date +%Y-%m-%d)

### Summary
$USER_DESCRIPTION

### Changed Files
$(for file in "${CHANGED_FILES[@]}"; do echo "- \`$file\`"; done)

### Breaking Changes
$BREAKING_CHANGES

### Type
$CHANGE_TYPE

$CURRENT_CHANGELOG
EOF
```

### Step 11: Commit Changes

```bash
git add .
git commit -m "$(cat <<EOF
feat: $USER_DESCRIPTION

Version bump: $CURRENT → $NEW_VERSION
Type: $CHANGE_TYPE

Modified files:
$(for file in "${CHANGED_FILES[@]}"; do echo "- $file"; done)

$BREAKING_CHANGES
EOF
)"
```

### Step 12: Push Branch

```bash
git push -u origin $BRANCH
```

### Step 13: Create Pull Request

Use GitHub CLI to create PR:

```bash
gh pr create \
  --title "Harness v$NEW_VERSION: $USER_DESCRIPTION" \
  --body "$(cat <<'EOF'
## Summary
$USER_DESCRIPTION

## Version Change
$CURRENT → $NEW_VERSION ($CHANGE_TYPE)

## Modified Components
$(for file in "${CHANGED_FILES[@]}"; do echo "- \`$file\`"; done)

## Test Plan
- [x] Tested in project: ${CLAUDE_PROJECT_DIR##*/}
- [x] All features working correctly
- [x] Documentation updated
- [x] CHANGELOG.md updated

## Breaking Changes
$BREAKING_CHANGES

## Additional Notes
This contribution was automatically generated using /harness-push command.
EOF
)"
```

### Step 14: Log Operation

```bash
echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) | PUSH | PR created | $NEW_VERSION | ${CHANGED_FILES[*]}" \
  >> $CLAUDE_PROJECT_DIR/.claude-state/harness/sync-log.txt
```

### Step 15: Cleanup

```bash
cd $CLAUDE_PROJECT_DIR
rm -rf /tmp/harness-remote
```

### Step 16: Report Success

```
✅ Pull request created successfully!

📤 Contribution Details:
- Version: v$CURRENT → v$NEW_VERSION ($CHANGE_TYPE)
- Files: ${#CHANGED_FILES[@]} modified
- Branch: $BRANCH

🔗 Pull Request:
{PR_URL}

📝 Title: "Harness v$NEW_VERSION: $USER_DESCRIPTION"

✨ Next Steps:
1. Review the PR on GitHub: {PR_URL}
2. Address any review comments if needed
3. Once merged, other projects can pull with /harness-pull
4. The new version will be v$NEW_VERSION

💡 Thank you for contributing to the harness!
```

## Error Handling

If `gh` CLI not available:
```
❌ GitHub CLI (gh) not found.

To create the pull request manually:
1. Push completed: {branch_url}
2. Visit: https://github.com/{user}/{repo}/pulls
3. Create PR from branch: $BRANCH
4. Use title: "Harness v$NEW_VERSION: $USER_DESCRIPTION"
5. Copy changelog entry to PR description
```

If push fails:
```
❌ Failed to push branch.

Check:
- Network connectivity
- GitHub authentication (gh auth status)
- Repository permissions

Branch created locally at: /tmp/harness-remote
You can manually push: cd /tmp/harness-remote && git push -u origin $BRANCH
```

## Success Criteria

- Changed files detected correctly
- Version bumped appropriately
- CHANGELOG.md updated
- PR created (or instructions provided)
- User clearly informed
