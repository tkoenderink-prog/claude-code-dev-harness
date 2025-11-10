# Comprehensive Cleanup Plan

## Executive Summary

**Goal:** Remove all "Superpowers" references and branding, clean up temporary files, and establish this as the "Claude Code Development Harness" project.

**Current State:** 136 skills properly migrated to `.claude/skills/`, but with legacy references and temporary files.

## Skill Count Clarification

**TOTAL: 136 skills in `.claude/skills/`**

Breakdown by source:
- **77 converted skills** - From old `.claude/skills/category/` structure (template/placeholder skills, now properly formatted)
- **38 user skills** - From `~/.claude/skills/` (your personal custom skills)
- **20 development skills** - From former development skills library (now integrated)
- **1 local skill** - `fixing-claude-code-hooks` (project-specific)

**Note:** The 20 "development skills" are now just regular skills - no longer tied to development skills library.

---

## Phase 1: Remove Temporary Files

### Files to Delete

1. **Backup archives** (no longer needed - everything in git):
   - `skills-backup-20251109-214148.tar.gz`
   - `claude-skills-backup-20251110-071624.tar.gz`

2. **Temporary migration scripts** (one-time use only):
   - `convert-claude-skills.py`
   - `migrate-global-skills.sh`
   - `migrate-plugin-skills.sh`

3. **Cache and system files**:
   - `.DS_Store` (root)
   - `.claude/.DS_Store`
   - `.claude/hooks/__pycache__/` (entire directory)
   - `.claude-state/.DS_Store`

4. **Empty skills directory**:
   - `skills/` (entire directory - only has README.md which is redundant)

**Actions:**
```bash
# Remove backups
rm -f *.tar.gz

# Remove temporary scripts
rm -f convert-claude-skills.py migrate-global-skills.sh migrate-plugin-skills.sh

# Remove cache/system files
find . -name ".DS_Store" -delete
find . -name "__pycache__" -type d -exec rm -rf {} +

# Remove empty skills directory
rm -rf skills/
```

---

## Phase 2: Remove "Superpowers" References

### Files Requiring Updates (22 files, 63 references)

#### A. Project Documentation

**1. `CLAUDE.md`**
- Remove mention of "development skills library"
- Change "Development Skills: 20" to "Development Skills: 20"
- Remove plugin attribution

**2. `.claude/skills/README.md`**
- Change "Development Skills: 20 (from development skills library)" to "Development Skills: 20"
- Update description to remove Superpowers branding

**3. `sync-skills.sh`**
- Change `PLUGIN_SRC` variable name to `DEV_SKILLS_SRC` or similar
- Update comments

#### B. Skill Files (19 files)

**Core Skills:**
1. `.claude/skills/using-superpowers/SKILL.md` → **RENAME** to `using-skills-advanced/` or **DELETE** if redundant
2. `.claude/skills/brainstorming/SKILL.md` - Remove "superpowers:" prefix
3. `.claude/skills/executing-plans/SKILL.md` - Remove "superpowers:" prefix
4. `.claude/skills/systematic-debugging/SKILL.md` - Remove "superpowers:" prefix
5. `.claude/skills/testing-skills-with-subagents/SKILL.md` - Remove "superpowers:" prefix
6. `.claude/skills/writing-plans/SKILL.md` - Remove "superpowers:" prefix
7. `.claude/skills/writing-skills/SKILL.md` - Update references
8. `.claude/skills/subagent-driven-development/SKILL.md` - Update references
9. `.claude/skills/sharing-skills/SKILL.md` - Remove `~/.config/superpowers/` paths
10. `.claude/skills/requesting-code-review/SKILL.md` - Update references
11. `.claude/skills/using-skills/SKILL.md` - Update if has references
12. `.claude/skills/pulling-updates-from-skills-repository/SKILL.md` - Update paths

**Conversation Skills:**
13. `.claude/skills/remembering-conversations/SKILL.md`
14. `.claude/skills/remembering-conversations/DEPLOYMENT.md`
15. `.claude/skills/remembering-conversations/INDEXING.md`
16. `.claude/skills/remembering-conversations/tool/migrate-to-config.sh`
17. `.claude/skills/remembering-conversations/tool/prompts/search-agent.md`
18. `.claude/skills/remembering-conversations/tool/test-deployment.sh`

**Actions:**
- Replace `superpowers:skill-name` with just `skill-name`
- Replace `~/.config/superpowers/` with `~/.claude/` or project-appropriate paths
- Update skill descriptions to remove Superpowers branding

---

## Phase 3: Update .gitignore

Add to `.gitignore`:
```
# Python cache
__pycache__/
*.py[cod]
*$py.class

# macOS
.DS_Store

# Backups
*.tar.gz
*.bak

# Temporary scripts
convert-*.py
migrate-*.sh
```

---

## Phase 4: Rename/Reorganize Problem Skills

### Decision Point: `using-superpowers/`

**Option A: Rename**
- Rename to `using-skills-advanced/` or `advanced-skill-usage/`
- Update content to be generic

**Option B: Delete**
- If content is redundant with `using-skills/`, delete entirely

**Option C: Merge**
- Merge content into `using-skills/SKILL.md`

**Recommendation:** Check content first, then decide

---

## Phase 5: Update Documentation

### Files to Update

**1. `CLAUDE.md`**

Current references:
```
- **Development Skills:** 20 (from development skills library)
```

Change to:
```
- **Development Skills:** 20 (core development workflows)
```

**2. `.claude/skills/README.md`**

Update all skill source descriptions to remove "Superpowers" branding.

**3. Create `SKILLS-ORIGIN.md`** (optional)

Document the skill origins for transparency:
```markdown
# Skills Origin

This project includes 136 skills from various sources:

## Sources

### Converted Skills (77)
Originally template skills in categorized structure, converted to proper format.
Categories: Architecture, Database, Debugging, Deployment, Development, Documentation, Security, Testing

### Personal Skills (38)
Custom skills from ~/.claude/skills/ for specific workflows:
- Obsidian knowledge management (8)
- Physical training programs (5)
- Cognitive bias awareness (5)
- Problem-solving techniques (6)
- Knowledge resources (7)
- Decision making (1)
- Other specialized skills (6)

### Development Workflow Skills (20)
Core development practices and patterns:
- TDD, systematic debugging, code review
- Git workflows, planning, brainstorming
- Testing strategies, verification
- Originally from Claude Code community

### Local Skills (1)
- fixing-claude-code-hooks (project-specific)
```

---

## Phase 6: Final Validation

### Validation Checklist

- [ ] No "superpowers" references in any file (case-insensitive)
- [ ] No "Superpowers" branding in documentation
- [ ] All paths updated to project-standard locations
- [ ] Skills health check passes
- [ ] All 136 skills still accessible
- [ ] Git status clean (no untracked cruft)
- [ ] README accurately describes project
- [ ] No temporary files remaining

### Validation Commands

```bash
# Check for superpowers references
grep -ri "superpowers" . --exclude-dir=.git | wc -l
# Should be 0

# Verify skill count
find .claude/skills -name "SKILL.md" | wc -l
# Should be 136

# Run health check
./check-skills-health.sh
# Should pass with 0 errors

# Check for temp files
find . -name "*.tar.gz" -o -name "*.pyc" -o -name ".DS_Store" -o -name "migrate-*.sh"
# Should return nothing
```

---

## Phase 7: Commit Strategy

### Commit 1: Remove temporary files
```
git rm skills/ -r
git rm *.tar.gz
git rm convert-claude-skills.py migrate-*.sh
git commit -m "Remove temporary migration files and empty skills/ directory"
```

### Commit 2: Update .gitignore
```
git add .gitignore
git commit -m "Update .gitignore for Python, macOS, and backup files"
```

### Commit 3: Remove Superpowers references
```
# After updating all files
git add -A
git commit -m "Remove Superpowers branding and references

- Replace 'superpowers:skill-name' with 'skill-name' in all skills
- Update documentation to use 'Development Skills' instead of 'Development Skills'
- Update paths from ~/.config/superpowers/ to project-standard paths
- Rename using-superpowers to using-skills-advanced
- Clean project of external branding

All 136 skills remain functional and accessible."
```

---

## Summary

**Files to Delete:** 8 items
**Files to Update:** 22 files (63 references)
**Validation Steps:** 7 checks
**Expected Result:** Clean project with 136 skills, no external branding, proper organization

**Time Estimate:** 30-45 minutes for full cleanup

---

## Risk Mitigation

**Backups:** All changes committed to git - can rollback anytime

**Testing:** Run health check after each phase to ensure nothing breaks

**Incremental:** Do cleanup in phases with commits to isolate issues
