#!/bin/bash
#
# Deployment Script for Claude Code Development Harness v2.1.0
# This script deploys the harness to the claude-code-dev-harness repository
#

set -e  # Exit on error

HARNESS_REPO="https://github.com/tkoenderink-prog/claude-code-dev-harness.git"
DEPLOY_DIR="/tmp/harness-deploy"

echo "🚀 Claude Code Development Harness v2.1.0 Deployment"
echo "======================================================"
echo ""

# Step 1: Clone the target repository
echo "📦 Step 1: Cloning target repository..."
if [ -d "$DEPLOY_DIR" ]; then
    echo "   Removing existing deployment directory..."
    rm -rf "$DEPLOY_DIR"
fi

git clone "$HARNESS_REPO" "$DEPLOY_DIR"
cd "$DEPLOY_DIR"

echo "   ✓ Repository cloned"
echo ""

# Step 2: Copy harness files
echo "📁 Step 2: Copying harness files..."
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Copy all files except this deployment script and git directory
rsync -av --exclude='.git' --exclude='DEPLOY.sh' "$SCRIPT_DIR/" "$DEPLOY_DIR/"

echo "   ✓ Files copied"
echo ""

# Step 3: Verify structure
echo "🔍 Step 3: Verifying file structure..."
EXPECTED_FILES=(
    "VERSION"
    "README.md"
    "CHANGELOG.md"
    "LICENSE"
    "CLAUDE.md"
    ".claude/agents/orchestrator.md"
    ".claude/commands/harness-install.md"
    ".claude/hooks/session-start"
)

MISSING_FILES=()
for file in "${EXPECTED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        MISSING_FILES+=("$file")
    fi
done

if [ ${#MISSING_FILES[@]} -gt 0 ]; then
    echo "   ❌ Missing files:"
    for file in "${MISSING_FILES[@]}"; do
        echo "      - $file"
    done
    exit 1
else
    echo "   ✓ All critical files present"
fi
echo ""

# Step 4: Count files
echo "📊 Step 4: File statistics..."
AGENTS=$(ls .claude/agents/*.md 2>/dev/null | wc -l)
SKILLS=$(find .claude/skills -name "*.md" 2>/dev/null | wc -l)
COMMANDS=$(ls .claude/commands/*.md 2>/dev/null | wc -l)
HOOKS=$(ls .claude/hooks/* 2>/dev/null | wc -l)

echo "   Agents:   $AGENTS"
echo "   Skills:   $SKILLS"
echo "   Commands: $COMMANDS"
echo "   Hooks:    $HOOKS"
echo ""

# Step 5: Make hooks executable
echo "🔧 Step 5: Setting permissions..."
chmod +x .claude/hooks/*
echo "   ✓ Hooks are executable"
echo ""

# Step 6: Git operations
echo "📝 Step 6: Committing to repository..."
git add .
git status --short

echo ""
read -p "   Ready to commit and push? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "   Deployment cancelled."
    echo "   Files are staged in: $DEPLOY_DIR"
    exit 0
fi

git commit -m "Initial release: Claude Code Development Harness v2.1.0

Complete cross-project harness versioning system with:
- 5 specialist agents (orchestrator, architect, engineer, tester, reviewer)
- 100+ core skills across 10 categories
- 4 harness management commands (install, pull, push, fix)
- Enhanced session-start hook with version checking
- Complete documentation and MIT license

Features:
- Bidirectional sync (pull updates, push improvements)
- Safe updates with automatic backups
- Project isolation via PROJ- prefix
- Semantic versioning with automated bumping
- Offline support with graceful degradation

Ready for installation in multiple projects.
"

echo "   ✓ Changes committed"
echo ""

# Step 7: Create tag
echo "🏷️  Step 7: Creating version tag..."
git tag -a v2.1.0 -m "Version 2.1.0 - Cross-Project Harness with Version Management"
echo "   ✓ Tag v2.1.0 created"
echo ""

# Step 8: Push to GitHub
echo "⬆️  Step 8: Pushing to GitHub..."
git push -u origin main
git push origin v2.1.0
echo "   ✓ Pushed to GitHub"
echo ""

# Step 9: Verification
echo "✅ Step 9: Deployment verification..."
git log --oneline -1
git tag --list
echo ""

# Success!
echo "🎉 Deployment Complete!"
echo "======================="
echo ""
echo "Repository: $HARNESS_REPO"
echo "Tag:        v2.1.0"
echo "Files:      $(find . -type f | wc -l) files deployed"
echo ""
echo "Next steps:"
echo "1. Visit https://github.com/tkoenderink-prog/claude-code-dev-harness"
echo "2. Verify the files and documentation"
echo "3. Use /harness-install in your projects to install the harness"
echo ""
echo "Deployment directory: $DEPLOY_DIR"
echo "(This directory can be safely deleted after verification)"
