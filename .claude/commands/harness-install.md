---
description: Install Claude Code harness from central repository
---

# Harness Installation

You are helping the user install the Claude Code v2.1 harness into their project.

## Process

Follow these steps in order. Use the Bash, Write, Read, and Edit tools to execute the operations.

### Step 1: Gather Configuration

Ask the user three questions:

1. **GitHub username**: What is your GitHub username? (for constructing repo URL)
2. **Version preference**: Do you want the latest version or a specific version? (default: latest)
3. **Create examples**: Should I create project-specific example files? (yes/no, default: no)

Wait for user responses before proceeding.

### Step 2: Clone Central Repository

Use the Bash tool to clone the harness repository to a temporary location:

```bash
cd /tmp
rm -rf harness-temp
git clone https://github.com/{username}/claude-code-dev-harness harness-temp
```

If a specific version was requested, checkout that tag:

```bash
cd /tmp/harness-temp
git checkout {version_tag}
```

### Step 3: Extract Version Information

Read the VERSION file from the cloned repo to determine what version is being installed:

```bash
cat /tmp/harness-temp/VERSION
```

Store this version for use in later steps.

### Step 4: Copy Core Harness Files

Use Bash to copy the harness structure to the current project. The project directory is available in the environment:

```bash
# Determine project directory
PROJECT_DIR="/home/user/Claude-code-app"

# Create .claude directory structure if it doesn't exist
mkdir -p "$PROJECT_DIR/.claude"

# Copy core components
cp -r /tmp/harness-temp/.claude/agents "$PROJECT_DIR/.claude/" 2>/dev/null || true
cp -r /tmp/harness-temp/.claude/skills "$PROJECT_DIR/.claude/" 2>/dev/null || true
cp -r /tmp/harness-temp/.claude/templates "$PROJECT_DIR/.claude/" 2>/dev/null || true
cp -r /tmp/harness-temp/.claude/commands "$PROJECT_DIR/.claude/" 2>/dev/null || true
cp -r /tmp/harness-temp/.claude/hooks "$PROJECT_DIR/.claude/" 2>/dev/null || true
cp -r /tmp/harness-temp/.claude/prompts "$PROJECT_DIR/.claude/" 2>/dev/null || true

# Make hooks executable
chmod +x "$PROJECT_DIR/.claude/hooks/"* 2>/dev/null || true

# Copy settings.json only if it doesn't exist (preserve existing settings)
if [ ! -f "$PROJECT_DIR/.claude/settings.json" ]; then
  cp /tmp/harness-temp/.claude/settings.json "$PROJECT_DIR/.claude/" 2>/dev/null || true
fi
```

### Step 5: Create CLAUDE.md with Markers

Use the Read tool to read the core CLAUDE.md from `/tmp/harness-temp/CLAUDE.md`.

Then use the Write tool to create a new CLAUDE.md in the project directory that combines the core harness content with a project-specific section:

Structure:
```markdown
# Claude Code v2.1: Professional Autonomy Harness

<!-- HARNESS-CORE-BEGIN -->
{full content from /tmp/harness-temp/CLAUDE.md}
<!-- HARNESS-CORE-END -->

<!-- PROJECT-SPECIFIC-BEGIN -->

## Project-Specific Configuration

This project uses the Claude Code Development Harness v{VERSION}.

### Version Info
- Installed version: {VERSION}
- Installation date: {TODAY}
- Central repo: https://github.com/{username}/claude-code-dev-harness

### Harness Management Commands
- `/harness-pull` - Pull updates from central repository
- `/harness-push` - Push improvements back to central repository
- `/harness-fix-after-update` - Troubleshoot issues after updates

### Custom Components
None yet. Create project-specific agents and skills with `PROJ-` prefix to keep them separate from core harness files.

### Project Customizations
Add your project-specific configuration, conventions, and notes here.

<!-- PROJECT-SPECIFIC-END -->
```

Replace placeholders with actual values:
- `{VERSION}` - from the VERSION file
- `{TODAY}` - current date in YYYY-MM-DD format
- `{username}` - GitHub username provided by user

### Step 6: Create VERSION.lock

Use the Write tool to create `.claude/VERSION.lock` in the project directory:

```yaml
harness_version: "{VERSION}"
installed_date: "{YYYY-MM-DD}"
repo_url: "https://github.com/{username}/claude-code-dev-harness"
last_check: "{ISO8601_TIMESTAMP}"
cache_duration_hours: 6
```

Replace placeholders:
- `{VERSION}` - from VERSION file
- `{YYYY-MM-DD}` - current date
- `{username}` - GitHub username
- `{ISO8601_TIMESTAMP}` - current timestamp in ISO 8601 format (e.g., 2025-11-09T14:30:00Z)

### Step 7: Create State Directory Structure

Use Bash to create the harness state directory:

```bash
PROJECT_DIR="/home/user/Claude-code-app"

mkdir -p "$PROJECT_DIR/.claude-state/harness/backups"
mkdir -p "$PROJECT_DIR/.claude-state/harness/remote-cache"

cat > "$PROJECT_DIR/.claude-state/harness/sync-log.txt" << 'EOF'
# Harness Sync Log
# Format: TIMESTAMP | ACTION | DETAILS | STATUS
EOF
```

### Step 8: Update .gitignore

Use Bash to ensure `.claude-state/` is in .gitignore:

```bash
PROJECT_DIR="/home/user/Claude-code-app"

if [ ! -f "$PROJECT_DIR/.gitignore" ]; then
  echo ".claude-state/" > "$PROJECT_DIR/.gitignore"
elif ! grep -q "^\.claude-state/" "$PROJECT_DIR/.gitignore" 2>/dev/null; then
  echo ".claude-state/" >> "$PROJECT_DIR/.gitignore"
fi
```

### Step 9: Cleanup Temporary Files

Remove the temporary clone:

```bash
rm -rf /tmp/harness-temp
```

### Step 10: Count Installed Components

Use Bash to count what was installed:

```bash
PROJECT_DIR="/home/user/Claude-code-app"

echo "Agents: $(find "$PROJECT_DIR/.claude/agents" -name "*.md" 2>/dev/null | wc -l)"
echo "Skills: $(find "$PROJECT_DIR/.claude/skills" -name "*.md" 2>/dev/null | wc -l)"
echo "Skill categories: $(find "$PROJECT_DIR/.claude/skills" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l)"
echo "Templates: $(find "$PROJECT_DIR/.claude/templates" -name "*.md" 2>/dev/null | wc -l)"
echo "Commands: $(find "$PROJECT_DIR/.claude/commands" -name "*.md" 2>/dev/null | wc -l)"
echo "Hooks: $(find "$PROJECT_DIR/.claude/hooks" -type f 2>/dev/null | wc -l)"
```

### Step 11: Report Success

Provide a comprehensive installation summary using the counts from Step 10:

```
✅ Harness v{VERSION} installed successfully!

📦 Installed Components:
- {agent_count} specialist agents
- {skill_count} skills across {category_count} categories
- {template_count} templates
- {command_count} commands
- {hook_count} lifecycle hooks

📁 Created Structure:
- .claude/ - Harness configuration and components
- .claude-state/harness/ - State and backups (gitignored)
- CLAUDE.md - Harness specification with marker sections
- .claude/VERSION.lock - Version tracking

🚀 Next Steps:
1. Review the PROJECT-SPECIFIC section in CLAUDE.md for customization
2. Test the harness with a simple task: "Create a hello world function"
3. Check for updates anytime with: /harness-pull
4. Create project-specific skills with PROJ- prefix if needed

💡 Tips:
- The harness can check for updates periodically
- All updates require manual approval
- Backups are created automatically before updates
- Use /harness-push to contribute improvements back to central repo
- All custom files should use PROJ- prefix to avoid conflicts with core harness
```

Replace placeholders with actual counts and version information.

## Error Handling

If any step fails:

1. **Git clone fails**: Check network connection and repository URL. Verify the username and repository name are correct.

2. **File copy fails**: Check disk space and permissions. Ensure the project directory is writable.

3. **Directory creation fails**: Check permissions and available disk space.

4. **Version file not found**: The repository may be corrupted. Try re-cloning.

Always cleanup `/tmp/harness-temp` even if installation fails.

## Success Criteria

- All harness files copied to project directory
- CLAUDE.md contains both HARNESS-CORE and PROJECT-SPECIFIC marker sections
- VERSION.lock exists and tracks installation metadata
- State directories created in .claude-state/harness/
- .gitignore updated to exclude .claude-state/
- User sees clear success message with component counts
