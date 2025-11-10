# Claude Code Development Harness - Skills Repository

This directory contains project-local skills for the Claude Code Development Harness.

## Overview

**Total Skills:** 59
- **User Skills:** 38 (from ~/.claude/skills/)
- **Plugin Skills:** 20 (from Superpowers plugin)
- **Local Skills:** 1 (fixing-claude-code-hooks)

**Special Directories:**
- **commands/** - Slash command implementations (not a skill)

## Directory Structure

Skills are organized in a **flat structure** where each skill has its own directory:

```
skills/
├── skill-name/
│   ├── SKILL.md              # Main skill file (required)
│   ├── supporting-files.*    # Optional supporting files
│   └── scripts/              # Optional executable scripts
└── README.md
```

## Skill Categories

### Meta (4 skills)
Skills about skills and project management
- `gardening-skills-wiki` - Maintain skills wiki health
- `using-skills` - How to use skills effectively
- `writing-skills` - TDD approach to creating skills
- `sharing-skills` - Contributing skills upstream

### Development (17 skills)
Software development workflows and practices
- `brainstorming` - Interactive design refinement
- `condition-based-waiting` - Replace timeouts with polling
- `defense-in-depth` - Layered security approach
- `dispatching-parallel-agents` - Parallel subagent execution
- `executing-plans` - Execute implementation plans
- `finishing-a-development-branch` - Complete feature branches
- `receiving-code-review` - Handle code review feedback
- `requesting-code-review` - Request quality code reviews
- `root-cause-tracing` - Trace bugs to root causes
- `subagent-driven-development` - Development with subagents
- `systematic-debugging` - Four-phase debugging framework
- `test-driven-development` - RED-GREEN-REFACTOR cycle
- `testing-anti-patterns` - Avoid common testing mistakes
- `testing-skills-with-subagents` - Test skills with agents
- `using-git-worktrees` - Isolated git workspaces
- `verification-before-completion` - Verify work before completion
- `writing-plans` - Create detailed implementation plans

### Debugging (1 skill)
- `fixing-claude-code-hooks` - Fix Claude Code hook errors

### Obsidian (8 skills)
Knowledge management in Obsidian
- `creating-obsidian-notes` - Prevent duplicates and orphans
- `discovering-vault-knowledge` - Find existing knowledge
- `moving-notes-safely` - Move notes without breaking links
- `obsidian-linking-strategy` - Create effective links
- `para-classification-decisions` - PARA method classification
- `retrieving-journal-entries` - Find journal entries
- `synthesis-dashboard-creation` - Create dashboard views
- `vault-weekly-review` - Weekly vault maintenance

### Physical Training (5 skills)
Workout and training programs
- `mobility-cycle-design` - 6-week mobility programs
- `mobility-session-design` - Individual mobility sessions
- `physical-training-benchmark-week` - Benchmark testing
- `strength-cycle-design` - 6-week strength programs
- `strength-workout-design` - Individual strength sessions

### Knowledge Resources (7 skills)
Framework and mental model management
- `context-aware-reasoning` - Apply contextual reasoning
- `discovering-relevant-frameworks` - Find applicable frameworks
- `maintaining-book-notes` - Organize book summaries
- `maintaining-influential-people-notes` - Track thought leaders
- `maintaining-mental-model-notes` - Document mental models
- `solving-with-frameworks` - Fast targeted framework application
- `understanding-with-frameworks` - Deep framework synthesis

### Cognitive Biases (5 skills)
Understanding and mitigating biases
- `deep-dive-research` - Research biases in depth
- `domain-specific-application` - Apply biases to domains
- `mitigation-strategies` - Debiasing techniques
- `pre-decision-checklist` - Pre-decision bias check
- `quick-recognition` - 2-minute bias identification

### Problem Solving (6 skills)
Advanced problem-solving techniques
- `collision-zone-thinking` - Force unrelated concepts together
- `inversion-exercise` - Flip core assumptions
- `meta-pattern-recognition` - Spot universal patterns
- `scale-game` - Test at extreme scales
- `simplification-cascades` - Progressive simplification
- `when-stuck` - Dispatch to right technique

### Architecture (1 skill)
- `preserving-productive-tensions` - Maintain beneficial tensions

### Collaboration (1 skill)
- `remembering-conversations` - Search past conversations

### Decision Making (1 skill)
- `thinking-through-a-decision` - Structured decision process

### Research (1 skill)
- `tracing-knowledge-lineages` - Track knowledge evolution

### Commands (1 skill)
- `commands` - Custom slash commands

### Superpowers (1 skill)
- `using-superpowers` - Using Superpowers plugin

## Usage

Skills are invoked by Claude Code automatically based on context, or explicitly:

```
Skill(skill-name)
```

For example:
```
Skill(systematic-debugging)
Skill(test-driven-development)
Skill(fixing-claude-code-hooks)
```

## Synchronization

These skills are **hard copies** from:
1. Global user skills: `~/.claude/skills/`
2. Plugin skills: `~/.claude/plugins/cache/superpowers/skills/`

To update from upstream sources, run:
```bash
./sync-skills.sh
```

## Maintenance

Run skills health check:
```bash
./check-skills-health.sh
```

This validates:
- Proper directory structure
- Valid frontmatter format
- No broken links
- No orphaned files

## Contributing

To add a new skill:
1. Follow `writing-skills` TDD methodology
2. Create `skills/skill-name/SKILL.md`
3. Use only `name` and `description` in frontmatter
4. Test with subagents before deploying
5. Run health check
6. Commit to project

## Version Control

All skills in this directory are version controlled with the project.
This enables:
- Project-specific skill customization
- Skill evolution tracking
- Team collaboration on skills
- Rollback capabilities

---

Last Updated: 2025-11-09
Total Skills: 60
