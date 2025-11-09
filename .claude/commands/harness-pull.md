---
description: Pull harness updates from central repository
---

# Harness Update (Pull)

You are helping the user pull harness updates from the central repository.

## Process

Execute these steps in order using available tools (Bash, Read, Write, Edit, Grep).

### Step 1: Load Current Configuration

Read `.claude/VERSION.lock` to get current installation metadata:

```bash
PROJECT_DIR="/home/user/Claude-code-app"
cat "$PROJECT_DIR/.claude/VERSION.lock"
```

Parse the YAML to extract:
- `harness_version` - Current installed version
- `repo_url` - Repository URL
- `last_check` - Last update check timestamp

Store these values for use in subsequent steps.

### Step 2: Clone Central Repository

Use Bash to clone the latest version from the central repository:

```bash
# Use repo URL from VERSION.lock
REPO_URL="https://github.com/{username}/claude-code-dev-harness"

cd /tmp
rm -rf harness-remote
git clone --depth 1 "$REPO_URL" harness-remote
```

If the clone fails, inform the user and stop:
```
❌ Failed to clone harness repository
Check your network connection and repository URL: {repo_url}
```

### Step 3: Compare Versions

Read the VERSION file from the remote repository:

```bash
cat /tmp/harness-remote/VERSION
```

Compare the remote version with the current version:
- Parse both as semantic versions (major.minor.patch)
- Determine if an update is available

**If already up to date:**

Display message and stop:
```
✅ Already on latest version v{CURRENT_VERSION}

No updates available. Your harness is up to date.

Last check: {last_check from VERSION.lock}
```

Cleanup and exit:
```bash
rm -rf /tmp/harness-remote
```

**If update available, proceed to next step.**

### Step 4: Show Changelog

Read the CHANGELOG.md from the remote repository and extract the relevant section for the new version:

```bash
cd /tmp/harness-remote
# Extract changelog section between the new version and the next ## heading
sed -n "/^## \[{REMOTE_VERSION}\]/,/^## /p" CHANGELOG.md | head -n -1
```

Display to user:
```
📋 Harness Update Available

Current version: v{CURRENT_VERSION}
Latest version: v{REMOTE_VERSION}

Changes in v{REMOTE_VERSION}:
{changelog_content}

=====================================
```

### Step 5: Ask for Confirmation

Ask the user: **"Update from v{CURRENT_VERSION} to v{REMOTE_VERSION}? (yes/no)"**

Wait for user response.

**If user says no:**
- Cleanup temp files
- Display: "Update cancelled. Your harness remains on v{CURRENT_VERSION}"
- Exit gracefully

**If user says yes:**
- Proceed to next step

### Step 6: Create Backup

Use Bash to create a timestamped backup of current harness files:

```bash
PROJECT_DIR="/home/user/Claude-code-app"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
BACKUP_FILE="$PROJECT_DIR/.claude-state/harness/backups/backup-$TIMESTAMP.zip"

cd "$PROJECT_DIR"

zip -r "$BACKUP_FILE" \
  .claude/agents/ \
  .claude/skills/ \
  .claude/templates/ \
  .claude/commands/ \
  .claude/hooks/ \
  .claude/prompts/ \
  CLAUDE.md \
  .claude/VERSION.lock \
  2>/dev/null

echo "💾 Backup created: $BACKUP_FILE"
```

Verify the backup was created successfully. If backup fails, warn the user and ask if they want to proceed anyway.

### Step 7: Preserve Project-Specific Content

Extract and save the PROJECT-SPECIFIC section from current CLAUDE.md:

```bash
PROJECT_DIR="/home/user/Claude-code-app"

sed -n '/<!-- PROJECT-SPECIFIC-BEGIN -->/,/<!-- PROJECT-SPECIFIC-END -->/p' \
  "$PROJECT_DIR/CLAUDE.md" > /tmp/project-specific.md
```

Verify the extraction was successful:

```bash
if [ ! -s /tmp/project-specific.md ]; then
  echo "⚠️  Warning: Could not extract PROJECT-SPECIFIC section"
  echo "CLAUDE.md may not have marker comments"
fi
```

If the file is empty or doesn't exist, create a default PROJECT-SPECIFIC section:

```markdown
<!-- PROJECT-SPECIFIC-BEGIN -->

## Project-Specific Configuration

This project uses the Claude Code Development Harness v{REMOTE_VERSION}.

### Version Info
- Updated version: {REMOTE_VERSION}
- Update date: {TODAY}
- Central repo: {repo_url}

### Harness Management Commands
- `/harness-pull` - Pull updates from central repository
- `/harness-push` - Push improvements back to central repository
- `/harness-fix-after-update` - Troubleshoot issues after updates

### Custom Components
None yet. Create project-specific agents and skills with `PROJ-` prefix.

<!-- PROJECT-SPECIFIC-END -->
```

### Step 8: Update Core Files

Update harness components, carefully preserving any PROJ- prefixed files:

```bash
PROJECT_DIR="/home/user/Claude-code-app"

# Update agents (skip PROJ- prefixed files)
if [ -d "/tmp/harness-remote/.claude/agents" ]; then
  for file in /tmp/harness-remote/.claude/agents/*.md; do
    filename=$(basename "$file")
    if [[ ! "$filename" =~ ^PROJ- ]]; then
      cp "$file" "$PROJECT_DIR/.claude/agents/$filename"
    fi
  done
fi

# Update skills recursively (skip PROJ- prefixed files)
if [ -d "/tmp/harness-remote/.claude/skills" ]; then
  find /tmp/harness-remote/.claude/skills -name "*.md" | while read file; do
    rel_path="${file#/tmp/harness-remote/.claude/skills/}"
    filename=$(basename "$file")
    if [[ ! "$filename" =~ ^PROJ- ]]; then
      mkdir -p "$PROJECT_DIR/.claude/skills/$(dirname "$rel_path")"
      cp "$file" "$PROJECT_DIR/.claude/skills/$rel_path"
    fi
  done
fi

# Update templates (all of them, no PROJ- concept for templates)
if [ -d "/tmp/harness-remote/.claude/templates" ]; then
  cp -r /tmp/harness-remote/.claude/templates/* "$PROJECT_DIR/.claude/templates/" 2>/dev/null || true
fi

# Update commands (preserve PROJ- prefixed commands)
if [ -d "/tmp/harness-remote/.claude/commands" ]; then
  for file in /tmp/harness-remote/.claude/commands/*.md; do
    filename=$(basename "$file")
    if [[ ! "$filename" =~ ^PROJ- ]]; then
      cp "$file" "$PROJECT_DIR/.claude/commands/$filename"
    fi
  done
fi

# Update hooks
if [ -d "/tmp/harness-remote/.claude/hooks" ]; then
  cp -r /tmp/harness-remote/.claude/hooks/* "$PROJECT_DIR/.claude/hooks/" 2>/dev/null || true
  chmod +x "$PROJECT_DIR/.claude/hooks/"* 2>/dev/null || true
fi

# Update prompts if they exist
if [ -d "/tmp/harness-remote/.claude/prompts" ]; then
  cp -r /tmp/harness-remote/.claude/prompts/* "$PROJECT_DIR/.claude/prompts/" 2>/dev/null || true
fi

# Note: settings.json is NOT updated automatically to preserve project-specific settings
# User should manually merge if needed
```

### Step 9: Rebuild CLAUDE.md

Combine the new harness core with the preserved project-specific content:

```bash
PROJECT_DIR="/home/user/Claude-code-app"

# Extract new HARNESS-CORE section from remote
sed -n '/<!-- HARNESS-CORE-BEGIN -->/,/<!-- HARNESS-CORE-END -->/p' \
  /tmp/harness-remote/CLAUDE.md > /tmp/harness-core.md

# Build new CLAUDE.md
cat > "$PROJECT_DIR/CLAUDE.md" << 'EOF'
# Claude Code v2.1: Professional Autonomy Harness
EOF

cat /tmp/harness-core.md >> "$PROJECT_DIR/CLAUDE.md"
echo "" >> "$PROJECT_DIR/CLAUDE.md"
cat /tmp/project-specific.md >> "$PROJECT_DIR/CLAUDE.md"
```

Verify the new CLAUDE.md has both sections:

```bash
if ! grep -q "<!-- HARNESS-CORE-BEGIN -->" "$PROJECT_DIR/CLAUDE.md"; then
  echo "⚠️  Warning: CLAUDE.md may be malformed"
fi
```

### Step 10: Update VERSION.lock

Update version and last check timestamp:

```bash
PROJECT_DIR="/home/user/Claude-code-app"
REMOTE_VERSION=$(cat /tmp/harness-remote/VERSION)
CURRENT_TIME=$(date -u +%Y-%m-%dT%H:%M:%SZ)

sed -i "s/harness_version: .*/harness_version: \"$REMOTE_VERSION\"/" "$PROJECT_DIR/.claude/VERSION.lock"
sed -i "s/last_check: .*/last_check: \"$CURRENT_TIME\"/" "$PROJECT_DIR/.claude/VERSION.lock"
```

### Step 11: Log the Operation

Append to sync log:

```bash
PROJECT_DIR="/home/user/Claude-code-app"
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
CURRENT_VERSION=$(grep "harness_version:" "$BACKUP_FILE" | head -1 | cut -d'"' -f2)
REMOTE_VERSION=$(cat /tmp/harness-remote/VERSION)

echo "$TIMESTAMP | PULL | $CURRENT_VERSION -> $REMOTE_VERSION | SUCCESS" \
  >> "$PROJECT_DIR/.claude-state/harness/sync-log.txt"
```

### Step 12: Count Changes

Count updated components:

```bash
PROJECT_DIR="/home/user/Claude-code-app"

AGENT_COUNT=$(find "$PROJECT_DIR/.claude/agents" -name "*.md" ! -name "PROJ-*" | wc -l)
SKILL_COUNT=$(find "$PROJECT_DIR/.claude/skills" -name "*.md" ! -name "PROJ-*" | wc -l)
TEMPLATE_COUNT=$(find "$PROJECT_DIR/.claude/templates" -name "*.md" | wc -l)
COMMAND_COUNT=$(find "$PROJECT_DIR/.claude/commands" -name "*.md" ! -name "PROJ-*" | wc -l)
HOOK_COUNT=$(find "$PROJECT_DIR/.claude/hooks" -type f | wc -l)

PROJ_AGENT_COUNT=$(find "$PROJECT_DIR/.claude/agents" -name "PROJ-*.md" 2>/dev/null | wc -l)
PROJ_SKILL_COUNT=$(find "$PROJECT_DIR/.claude/skills" -name "PROJ-*.md" 2>/dev/null | wc -l)
PROJ_COMMAND_COUNT=$(find "$PROJECT_DIR/.claude/commands" -name "PROJ-*.md" 2>/dev/null | wc -l)
```

### Step 13: Cleanup Temporary Files

Remove temporary files:

```bash
rm -rf /tmp/harness-remote
rm -f /tmp/harness-core.md /tmp/project-specific.md
```

### Step 14: Report Results

Provide detailed update summary:

```
✅ Harness updated successfully!

📦 Version Change: v{CURRENT_VERSION} → v{REMOTE_VERSION}

💾 Backup: {backup_file_path}

📝 Updated Components:
- {agent_count} core agents
- {skill_count} core skills
- {template_count} templates
- {command_count} core commands
- {hook_count} hooks

🔒 Preserved:
- {proj_agent_count} PROJ- agents
- {proj_skill_count} PROJ- skills
- {proj_command_count} PROJ- commands
- PROJECT-SPECIFIC section in CLAUDE.md
- Custom settings.json configurations

⚠️  Manual Review Recommended:
- Check .claude/settings.json for new configuration options
- Review CHANGELOG for any breaking changes
- Test critical workflows to ensure compatibility

🔧 Troubleshooting:
If you encounter issues after update, use:
- /harness-fix-after-update - Auto-diagnose and fix common issues
- Or restore from backup: {backup_file_path}

📚 What's New:
{brief summary of key changes from changelog}
```

Replace placeholders with actual values from the update process.

## Advanced: Conflict Detection

If you want to detect local modifications to core files (optional advanced feature):

Before updating a core file, check if it differs from the original:

```bash
# For each core file being updated
FILE="agents/orchestrator.md"

# Create a hash of current file
CURRENT_HASH=$(md5sum "$PROJECT_DIR/.claude/$FILE" 2>/dev/null | cut -d' ' -f1)

# Compare with remote
REMOTE_HASH=$(md5sum "/tmp/harness-remote/.claude/$FILE" 2>/dev/null | cut -d' ' -f1)

if [ "$CURRENT_HASH" != "$REMOTE_HASH" ] && [ -n "$CURRENT_HASH" ]; then
  # File was modified locally
  cp "$PROJECT_DIR/.claude/$FILE" "$PROJECT_DIR/.claude/$FILE.local-$(date +%Y%m%d)"
  echo "⚠️  $FILE was locally modified. Saved as $FILE.local-*"
fi
```

Include any saved local versions in the final report.

## Error Handling

**Version comparison fails:**
- Default to showing update available
- Warn user about version parsing issue

**Backup creation fails:**
- Warn user
- Ask if they want to proceed without backup
- Stop if user declines

**File copy fails:**
- Try to continue with remaining files
- Report which files failed in final summary
- Suggest manual intervention

**CLAUDE.md reconstruction fails:**
- Keep backup of original
- Attempt manual merge
- Provide instructions for user to fix

Always cleanup `/tmp/harness-remote` even if update fails partially.

## Success Criteria

- Backup created successfully
- PROJECT-SPECIFIC section preserved in CLAUDE.md
- All core files updated (non-PROJ-)
- All PROJ- files untouched
- VERSION.lock updated with new version
- Sync log updated
- User informed with detailed report
- Temporary files cleaned up
