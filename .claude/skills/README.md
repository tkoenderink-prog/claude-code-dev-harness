# Claude Code Development Harness - Skills Repository

This directory contains project-local skills for the Claude Code Development Harness.

## Overview

**Total Skills:** 136 active skills + 1 special directory
- **Converted Skills:** 77 (from old categorized structure)
- **User Skills:** 38 (from ~/.claude/skills/)
- **Plugin Skills:** 20 (from Superpowers plugin)
- **Local Skills:** 1 (fixing-claude-code-hooks)
- **Special:** commands/ (slash command implementations)

All skills are in the official Claude Code format: `.claude/skills/skill-name/SKILL.md`

## Usage

Skills are invoked automatically by Claude Code or explicitly:

```
Skill(skill-name)
```

For full catalog with categories, see: `skills/README.md`

For synchronization and maintenance, see project root scripts:
- `./sync-skills.sh` - Update from upstream
- `./check-skills-health.sh` - Validate structure

---

Last Updated: 2025-11-10
Total Skills: 136
