#!/bin/bash
#
# Claude Code Development Harness - Bootstrap Installer
# Version: 2.1.0
#
# Usage:
#   curl -sSL https://raw.githubusercontent.com/tkoenderink-prog/claude-code-dev-harness/main/install.sh | bash
#
# Or download and run:
#   wget https://raw.githubusercontent.com/tkoenderink-prog/claude-code-dev-harness/main/install.sh
#   chmod +x install.sh
#   ./install.sh
#

set -e  # Exit on error

REPO_URL="https://github.com/tkoenderink-prog/claude-code-dev-harness.git"
TEMP_DIR="/tmp/harness-bootstrap-$$"
VERSION="2.1.0"

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  Claude Code Development Harness v${VERSION}                        ║"
echo "║  Bootstrap Installer                                           ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check if we're in a directory
if [ ! -d "$(pwd)" ]; then
    echo "❌ Error: Not in a valid directory"
    exit 1
fi

echo "📁 Installation directory: $(pwd)"
echo ""

# Warning if .claude already exists
if [ -d ".claude" ]; then
    echo "⚠️  Warning: .claude/ directory already exists!"
    echo ""
    read -p "   Overwrite existing harness? (yes/no): " CONFIRM
    if [ "$CONFIRM" != "yes" ]; then
        echo "   Installation cancelled."
        exit 0
    fi
    echo "   Backing up existing .claude/ to .claude.backup..."
    rm -rf .claude.backup
    mv .claude .claude.backup
fi

# Step 1: Clone repository
echo "📦 Step 1/6: Cloning harness repository..."
git clone --depth 1 --quiet "$REPO_URL" "$TEMP_DIR" 2>/dev/null || {
    echo "❌ Error: Failed to clone repository"
    echo "   Make sure you have git installed and internet access"
    exit 1
}
echo "   ✓ Repository cloned"
echo ""

# Step 2: Copy harness structure
echo "📁 Step 2/6: Installing harness files..."
cp -r "$TEMP_DIR/.claude" .
cp "$TEMP_DIR/CLAUDE.md" CLAUDE.md
echo "   ✓ Files copied"
echo ""

# Step 3: Set permissions
echo "🔧 Step 3/6: Setting permissions..."
chmod +x .claude/hooks/*
echo "   ✓ Hooks are executable"
echo ""

# Step 4: Create VERSION.lock
echo "📝 Step 4/6: Creating VERSION.lock..."
cat > .claude/VERSION.lock << EOF
harness_version: "$VERSION"
installed_date: "$(date +%Y-%m-%d)"
repo_url: "$REPO_URL"
last_check: "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
cache_duration_hours: 6
EOF
echo "   ✓ VERSION.lock created"
echo ""

# Step 5: Create state directory
echo "📂 Step 5/6: Creating state directory..."
mkdir -p .claude-state/harness/backups
mkdir -p .claude-state/harness/remote-cache
cat > .claude-state/harness/sync-log.txt << 'EOF'
# Harness Sync Log
# Format: TIMESTAMP | ACTION | DETAILS | STATUS
EOF
echo "   ✓ State directory created"
echo ""

# Step 6: Update .gitignore
echo "📋 Step 6/6: Updating .gitignore..."
if [ ! -f ".gitignore" ]; then
    touch .gitignore
fi

if ! grep -q "^\.claude-state/" .gitignore 2>/dev/null; then
    echo ".claude-state/" >> .gitignore
    echo "   ✓ Added .claude-state/ to .gitignore"
else
    echo "   ✓ .gitignore already configured"
fi
echo ""

# Cleanup
rm -rf "$TEMP_DIR"

# Verification
echo "🔍 Verification:"
AGENTS=$(ls .claude/agents/*.md 2>/dev/null | wc -l)
SKILLS=$(find .claude/skills -name "*.md" 2>/dev/null | wc -l)
COMMANDS=$(ls .claude/commands/*.md 2>/dev/null | wc -l)
HOOKS=$(ls .claude/hooks/* 2>/dev/null | wc -l)

echo "   Agents:   $AGENTS"
echo "   Skills:   $SKILLS"
echo "   Commands: $COMMANDS"
echo "   Hooks:    $HOOKS"
echo ""

# Add PROJECT-SPECIFIC section to CLAUDE.md if not present
if ! grep -q "PROJECT-SPECIFIC-BEGIN" CLAUDE.md 2>/dev/null; then
    echo "📝 Adding PROJECT-SPECIFIC section to CLAUDE.md..."
    cat >> CLAUDE.md << 'EOF'

<!-- PROJECT-SPECIFIC-BEGIN -->

## Project-Specific Configuration

This project uses the Claude Code Development Harness v2.1.0.

### Version Info
- Current version: 2.1.0
- Central repo: https://github.com/tkoenderink-prog/claude-code-dev-harness
- Last update: $(date +%Y-%m-%d)

### Harness Management Commands
- `/harness-install` - Install harness into new project
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
EOF
    echo "   ✓ PROJECT-SPECIFIC section added"
    echo ""
fi

# Success message
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  ✅ Installation Complete!                                     ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "📦 Installed Components:"
echo "   • 5 specialist agents (orchestrator, architect, engineer, tester, reviewer)"
echo "   • $SKILLS skills across 10 categories"
echo "   • $COMMANDS harness management commands"
echo "   • $HOOKS lifecycle hooks"
echo ""
echo "🚀 Next Steps:"
echo "   1. Start/restart your Claude Code session"
echo "   2. All harness commands are now available:"
echo "      • /harness-pull    - Check for updates"
echo "      • /harness-push    - Contribute improvements"
echo "      • /harness-fix     - Run diagnostics"
echo "   3. Try a test task: 'Create a hello world function'"
echo ""
echo "📚 Documentation:"
echo "   • Review CLAUDE.md for complete specification"
echo "   • Check .claude/VERSION.lock for version info"
echo "   • Visit https://github.com/tkoenderink-prog/claude-code-dev-harness"
echo ""
echo "💡 The harness will auto-check for updates every 6 hours"
echo ""
