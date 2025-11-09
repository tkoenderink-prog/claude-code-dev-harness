---
description: Fix common issues after harness update
---

# Harness Post-Update Troubleshooting

You are helping the user diagnose and fix issues after a harness update.

## Process

Run diagnostics and fix common issues automatically.

### Step 1: Run Full Diagnostic

Execute comprehensive health check:

```bash
echo "🔍 Harness Diagnostic Report"
echo "============================"
echo ""

echo "📋 Version Information:"
if [ -f ".claude/VERSION.lock" ]; then
  cat .claude/VERSION.lock
else
  echo "❌ VERSION.lock not found!"
fi
echo ""

echo "👥 Agents:"
if [ -d ".claude/agents" ]; then
  ls -1 .claude/agents/
  echo "Total: $(ls .claude/agents/*.md 2>/dev/null | wc -l)"
else
  echo "❌ agents directory not found!"
fi
echo ""

echo "🎯 Skills:"
if [ -d ".claude/skills" ]; then
  echo "Total skills: $(find .claude/skills -name "*.md" | wc -l)"
  echo "Organized in $(find .claude/skills -mindepth 1 -maxdepth 1 -type d | wc -l) categories"
else
  echo "❌ skills directory not found!"
fi
echo ""

echo "📄 Templates:"
if [ -d ".claude/templates" ]; then
  ls -1 .claude/templates/
else
  echo "❌ templates directory not found!"
fi
echo ""

echo "🪝 Hooks:"
if [ -d ".claude/hooks" ]; then
  ls -1 .claude/hooks/
  echo "Permissions:"
  ls -l .claude/hooks/
else
  echo "❌ hooks directory not found!"
fi
echo ""

echo "📝 CLAUDE.md Markers:"
if [ -f "CLAUDE.md" ]; then
  echo "HARNESS-CORE markers: $(grep -c "HARNESS-CORE" CLAUDE.md 2>/dev/null || echo "0")"
  echo "PROJECT-SPECIFIC markers: $(grep -c "PROJECT-SPECIFIC" CLAUDE.md 2>/dev/null || echo "0")"
  if grep -q "<!-- HARNESS-CORE-BEGIN -->" CLAUDE.md && \
     grep -q "<!-- HARNESS-CORE-END -->" CLAUDE.md && \
     grep -q "<!-- PROJECT-SPECIFIC-BEGIN -->" CLAUDE.md && \
     grep -q "<!-- PROJECT-SPECIFIC-END -->" CLAUDE.md; then
    echo "✅ All markers present"
  else
    echo "❌ Markers missing or incomplete"
  fi
else
  echo "❌ CLAUDE.md not found!"
fi
echo ""

echo "💾 State Directory:"
if [ -d ".claude-state/harness" ]; then
  echo "State files: $(find .claude-state/harness -type f | wc -l)"
  echo "Recent backups:"
  ls -t .claude-state/harness/backups/*.zip 2>/dev/null | head -3 || echo "  No backups found"
else
  echo "❌ State directory not found!"
fi
echo ""

echo "📊 Recent Sync Operations:"
if [ -f ".claude-state/harness/sync-log.txt" ]; then
  tail -5 .claude-state/harness/sync-log.txt
else
  echo "No sync history"
fi
```

### Step 2: Check for Common Issues

#### Issue 1: Missing CLAUDE.md Markers

```bash
if ! grep -q "<!-- HARNESS-CORE-BEGIN -->" CLAUDE.md 2>/dev/null; then
  echo "❌ Issue detected: CLAUDE.md missing markers"
  echo "🔧 Fixing..."

  # Backup current
  cp CLAUDE.md CLAUDE.md.backup-$(date +%Y%m%d-%H%M%S)

  # Wrap in PROJECT-SPECIFIC (safe default)
  cat > CLAUDE.md.new << 'EOF'
# Claude Code v2.1: Professional Autonomy Harness

<!-- HARNESS-CORE-BEGIN -->
[Core content will be inserted on next /harness-pull]
<!-- HARNESS-CORE-END -->

<!-- PROJECT-SPECIFIC-BEGIN -->
EOF

  cat CLAUDE.md >> CLAUDE.md.new

  echo "<!-- PROJECT-SPECIFIC-END -->" >> CLAUDE.md.new

  mv CLAUDE.md.new CLAUDE.md

  echo "✅ Markers restored"
  echo "⚠️  Run /harness-pull to update core content"
fi
```

#### Issue 2: Hook Permissions

```bash
if [ -d ".claude/hooks" ]; then
  FIXED=0
  for hook in .claude/hooks/*; do
    if [ -f "$hook" ] && [ ! -x "$hook" ]; then
      echo "🔧 Fixing permissions: $hook"
      chmod +x "$hook"
      FIXED=$((FIXED + 1))
    fi
  done
  if [ $FIXED -gt 0 ]; then
    echo "✅ Fixed $FIXED hook permissions"
  else
    echo "✅ Hook permissions verified"
  fi
fi
```

#### Issue 3: Hook Syntax Errors

```bash
if [ -f ".claude/hooks/session-start" ]; then
  # Check if it's Python (should be)
  if head -1 .claude/hooks/session-start | grep -q "python"; then
    if python3 -m py_compile .claude/hooks/session-start 2>/dev/null; then
      echo "✅ session-start hook syntax OK"
    else
      echo "❌ session-start hook has syntax errors"
      echo "   Run: python3 -m py_compile .claude/hooks/session-start"
    fi
  fi
fi

if [ -f ".claude/hooks/session-end" ]; then
  if head -1 .claude/hooks/session-end | grep -q "python"; then
    if python3 -m py_compile .claude/hooks/session-end 2>/dev/null; then
      echo "✅ session-end hook syntax OK"
    else
      echo "❌ session-end hook has syntax errors"
      echo "   Run: python3 -m py_compile .claude/hooks/session-end"
    fi
  fi
fi
```

#### Issue 4: State Directory Structure

```bash
REQUIRED_DIRS=(
  ".claude-state/harness/backups"
  ".claude-state/harness/remote-cache"
)

CREATED=0
for dir in "${REQUIRED_DIRS[@]}"; do
  if [ ! -d "$dir" ]; then
    echo "🔧 Creating missing directory: $dir"
    mkdir -p "$dir"
    CREATED=$((CREATED + 1))
  fi
done

if [ ! -f ".claude-state/harness/sync-log.txt" ]; then
  echo "🔧 Creating sync log"
  cat > .claude-state/harness/sync-log.txt << 'EOF'
# Harness Sync Log
# Format: TIMESTAMP | ACTION | DETAILS | STATUS
EOF
  CREATED=$((CREATED + 1))
fi

if [ $CREATED -gt 0 ]; then
  echo "✅ Created $CREATED missing state components"
else
  echo "✅ State directory structure verified"
fi
```

#### Issue 5: Agent Tool Mismatches

```bash
echo "🔍 Checking agent tool access..."

# Read what tools agents expect
if [ -d ".claude/agents" ]; then
  echo "Expected tools by agents:"
  grep -h "^- \*\*Tools\*\*:" .claude/agents/*.md 2>/dev/null | sort -u

  echo ""
  echo "⚠️  Compare with .claude/settings.json to ensure tools are granted"
  echo "   If mismatches found, update settings.json manually"
else
  echo "❌ No agents directory found"
fi
```

#### Issue 6: Broken Skill References

```bash
echo "🔍 Checking for broken skill references..."

BROKEN=0
CHECKED=0

# Check in agents
if [ -d ".claude/agents" ]; then
  while IFS= read -r line; do
    # Extract skill path from various reference formats
    # Format: skills/category/skill-name.md
    SKILL_REF=$(echo "$line" | grep -o 'skills/[^)]*\.md' | sed 's/\.md$//')

    if [ -n "$SKILL_REF" ]; then
      CHECKED=$((CHECKED + 1))
      if [ ! -f ".claude/$SKILL_REF.md" ]; then
        echo "❌ Broken reference: .claude/$SKILL_REF.md"
        BROKEN=$((BROKEN + 1))
      fi
    fi
  done < <(grep -r "skills/" .claude/agents/ 2>/dev/null)
fi

# Check in skills themselves
if [ -d ".claude/skills" ]; then
  while IFS= read -r line; do
    SKILL_REF=$(echo "$line" | grep -o 'skills/[^)]*\.md' | sed 's/\.md$//')

    if [ -n "$SKILL_REF" ]; then
      CHECKED=$((CHECKED + 1))
      if [ ! -f ".claude/$SKILL_REF.md" ]; then
        echo "❌ Broken reference: .claude/$SKILL_REF.md"
        BROKEN=$((BROKEN + 1))
      fi
    fi
  done < <(grep -r "skills/" .claude/skills/ 2>/dev/null)
fi

if [ $BROKEN -eq 0 ]; then
  echo "✅ No broken skill references found (checked $CHECKED references)"
else
  echo "⚠️  Found $BROKEN broken references out of $CHECKED checked"
  echo "   Consider running /harness-pull to get missing skills"
fi
```

### Step 3: Provide Rollback Instructions

If major issues found, provide rollback procedure:

```
🆘 Emergency Rollback Procedure

If the harness is seriously broken, you can restore from backup:

1. Find latest backup:
   ls -t .claude-state/harness/backups/*.zip | head -1

2. Extract to temporary location:
   LATEST_BACKUP=$(ls -t .claude-state/harness/backups/*.zip | head -1)
   unzip "$LATEST_BACKUP" -d /tmp/harness-restore

3. Remove corrupted files:
   rm -rf .claude/agents .claude/skills .claude/templates .claude/commands .claude/hooks

4. Restore from backup:
   cp -r /tmp/harness-restore/.claude/* .claude/
   cp /tmp/harness-restore/CLAUDE.md CLAUDE.md
   cp /tmp/harness-restore/.claude/VERSION.lock .claude/VERSION.lock

5. Verify restoration:
   /harness-fix-after-update

6. Cleanup:
   rm -rf /tmp/harness-restore

7. Reconsider the update:
   - Check CHANGELOG.md for breaking changes
   - Review migration notes
   - Update project-specific files if needed
```

### Step 4: Advanced Diagnostics

If issues persist, run deeper checks:

```bash
echo "🔬 Advanced Diagnostics"
echo "======================"
echo ""

echo "📦 File Integrity:"
# Check for empty files
EMPTY_FILES=$(find .claude -type f -empty)
if [ -n "$EMPTY_FILES" ]; then
  echo "❌ Empty files found:"
  echo "$EMPTY_FILES"
else
  echo "✅ No empty files"
fi

echo ""
echo "🔗 Symlink Check:"
# Check for broken symlinks
BROKEN_LINKS=$(find .claude -type l ! -exec test -e {} \; -print)
if [ -n "$BROKEN_LINKS" ]; then
  echo "❌ Broken symlinks found:"
  echo "$BROKEN_LINKS"
else
  echo "✅ No broken symlinks"
fi

echo ""
echo "📐 File Format Check:"
# Check markdown files are valid
MD_ERRORS=0
while IFS= read -r md_file; do
  # Basic validation: file should have content and not be binary
  if file "$md_file" | grep -q "text"; then
    :  # OK
  else
    echo "❌ Invalid file: $md_file"
    MD_ERRORS=$((MD_ERRORS + 1))
  fi
done < <(find .claude -name "*.md")

if [ $MD_ERRORS -eq 0 ]; then
  echo "✅ All markdown files valid"
else
  echo "⚠️  Found $MD_ERRORS problematic files"
fi

echo ""
echo "🔍 Configuration Consistency:"
# Check VERSION.lock exists and is valid
if [ -f ".claude/VERSION.lock" ]; then
  if grep -q "version:" .claude/VERSION.lock && \
     grep -q "repo_url:" .claude/VERSION.lock && \
     grep -q "updated_at:" .claude/VERSION.lock; then
    echo "✅ VERSION.lock is valid"
  else
    echo "❌ VERSION.lock is incomplete"
  fi
else
  echo "❌ VERSION.lock missing"
fi
```

### Step 5: Final Summary

```
📊 Diagnostic Summary
====================

Issues Found:
{list issues detected}

Fixes Applied:
{list automatic fixes}

Manual Actions Needed:
{list any manual steps}

Status: {HEALTHY / NEEDS ATTENTION / CRITICAL}

Recommendations:
{specific recommendations based on findings}

✅ Harness troubleshooting complete!
```

## Common Issue Patterns

### Pattern 1: After Major Version Update

If you updated across major versions (e.g., 1.x to 2.x):

1. Check CHANGELOG.md for breaking changes
2. Review migration guide (if provided)
3. Update project-specific integrations
4. Re-test all workflows
5. Consider gradual rollout

### Pattern 2: Merge Conflicts in CLAUDE.md

If CLAUDE.md has conflicts after update:

1. Extract PROJECT-SPECIFIC section (between markers)
2. Run /harness-pull again
3. Manually insert saved PROJECT-SPECIFIC content
4. Verify markers are intact

### Pattern 3: Tool Access Errors

If agents report "tool not available":

1. Check `.claude/settings.json`
2. Verify tools listed match agent requirements
3. Restart Claude Code session
4. Re-run /harness-fix-after-update

### Pattern 4: State Corruption

If state directory is corrupted:

1. Backup `.claude-state/`
2. Remove `.claude-state/harness/`
3. Re-run /harness-pull
4. Restore project-specific state if needed

## Success Criteria

- All diagnostics run successfully
- Common issues detected and fixed automatically
- Clear report provided to user
- Rollback instructions available if needed
- User can resume normal development
