# Bootstrap Installation for New Projects

## The Bootstrapping Problem

You can't run `/harness-install` in a new project because that command is part of the harness itself. This guide shows you how to install the harness for the very first time.

## Quick Bootstrap (Copy-Paste Method)

### Step 1: Clone and Copy

Run these commands in your project directory:

```bash
# Clone the harness to a temporary location
git clone https://github.com/tkoenderink-prog/claude-code-dev-harness.git /tmp/harness-temp

# Copy the harness structure to your project
cp -r /tmp/harness-temp/.claude .
cp /tmp/harness-temp/CLAUDE.md CLAUDE.md

# Make hooks executable
chmod +x .claude/hooks/*

# Cleanup
rm -rf /tmp/harness-temp

# Add to gitignore
echo ".claude-state/" >> .gitignore
```

### Step 2: Create VERSION.lock

Create `.claude/VERSION.lock`:

```yaml
harness_version: "2.1.0"
installed_date: "2025-11-09"
repo_url: "https://github.com/tkoenderink-prog/claude-code-dev-harness"
last_check: "2025-11-09T00:00:00Z"
cache_duration_hours: 6
```

### Step 3: Create State Directory

```bash
mkdir -p .claude-state/harness/backups
mkdir -p .claude-state/harness/remote-cache
cat > .claude-state/harness/sync-log.txt << 'EOF'
# Harness Sync Log
# Format: TIMESTAMP | ACTION | DETAILS | STATUS
EOF
```

### Step 4: Update CLAUDE.md

Your `CLAUDE.md` now has the full harness specification. Add project-specific content at the end:

```markdown
<!-- PROJECT-SPECIFIC-BEGIN -->

## Project-Specific Configuration

This project uses the Claude Code Development Harness v2.1.0.

### Version Info
- Current version: 2.1.0
- Central repo: https://github.com/tkoenderink-prog/claude-code-dev-harness
- Last update: 2025-11-09

### Harness Management Commands
- `/harness-install` - Install harness into new project (now available!)
- `/harness-pull` - Pull updates from central repository
- `/harness-push` - Push improvements back to central repository
- `/harness-fix-after-update` - Troubleshoot post-update issues

### Project-Specific Customizations

**Custom Agents** (preserved during updates):
- None currently (create with PROJ- prefix in `.claude/agents/`)

**Custom Skills** (preserved during updates):
- None currently (create with PROJ- prefix in `.claude/skills/`)

### Update Policy
- Auto-check on session start (6-hour cache)
- Manual updates only (never automatic)
- Backups created before each update in `.claude-state/harness/backups/`
- Conflicts resolved manually with .CONFLICT files

<!-- PROJECT-SPECIFIC-END -->
```

### Step 5: Verify Installation

```bash
ls -la .claude/
# Should see: agents/ commands/ hooks/ prompts/ skills/ settings.json

cat .claude/VERSION.lock
# Should show version 2.1.0
```

**Done!** The harness is now installed. All commands including `/harness-install`, `/harness-pull`, and `/harness-push` are now available.

---

## One-Line Bootstrap (Advanced)

For experienced users, here's a one-liner:

```bash
curl -sSL https://raw.githubusercontent.com/tkoenderink-prog/claude-code-dev-harness/main/VERSION && \
git clone --depth 1 https://github.com/tkoenderink-prog/claude-code-dev-harness.git /tmp/h && \
cp -r /tmp/h/.claude . && cp /tmp/h/CLAUDE.md . && chmod +x .claude/hooks/* && \
mkdir -p .claude-state/harness/{backups,remote-cache} && \
echo "harness_version: \"2.1.0\"
installed_date: \"$(date +%Y-%m-%d)\"
repo_url: \"https://github.com/tkoenderink-prog/claude-code-dev-harness\"
last_check: \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"
cache_duration_hours: 6" > .claude/VERSION.lock && \
echo ".claude-state/" >> .gitignore && \
rm -rf /tmp/h && \
echo "✅ Harness v2.1.0 installed!"
```

---

## Alternative: Ask Claude Code to Bootstrap

If you're already in a Claude Code session, you can ask:

```
Please bootstrap the Claude Code harness v2.1.0 from
https://github.com/tkoenderink-prog/claude-code-dev-harness

Clone it to /tmp, copy .claude/ and CLAUDE.md to my project,
create VERSION.lock, set up state directories, and update .gitignore.
```

Claude will execute the bootstrap steps for you.

---

## After Bootstrap

Once installed, you can use all harness commands:

- **`/harness-pull`** - Check for and install updates
- **`/harness-push`** - Contribute improvements back
- **`/harness-fix-after-update`** - Run diagnostics

The harness will also automatically check for updates every 6 hours when you start a new session.

---

## Troubleshooting Bootstrap

### Issue: Permission denied on hooks

**Solution:**
```bash
chmod +x .claude/hooks/*
```

### Issue: CLAUDE.md markers not working

**Solution:** Make sure CLAUDE.md from the harness has the marker structure. The file should start with `<!-- HARNESS-CORE-BEGIN -->` around line 3.

### Issue: Commands not showing up

**Solution:** Restart your Claude Code session after bootstrap. The commands are loaded when Claude Code starts.

### Issue: Git clone fails

**Solution:** Download the repository as ZIP:
1. Go to https://github.com/tkoenderink-prog/claude-code-dev-harness
2. Click "Code" → "Download ZIP"
3. Extract and copy `.claude/` and `CLAUDE.md` to your project

---

## Future: Easier Bootstrap

In future versions, we're considering:
- A `curl | bash` installer script
- GitHub template repository (click "Use this template")
- VS Code extension for one-click install
- Claude Code native installation command

For now, the copy-paste method above is the recommended bootstrap approach.
