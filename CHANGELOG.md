# Changelog

All notable changes to the Claude Code Development Harness will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.3.0] - 2025-11-10

### Added - Elite Skills Library

**New Meta-Skill:**
- `cc-skill-in-practice-optimizer` - Analyzes real usage logs to optimize skills based on actual agent behavior
  - Score: 92/100 (Exemplary)
  - 5-phase process: Collect → Evaluate → Analyze → Synthesize → HITL
  - Presents 3 optimization tiers (minimal/medium/maximum effort)
  - Default: analyzes last 25 skill invocations
  - Includes real example from skill-evaluator analysis

**New Documentation:**
- `docs/SKILL-DESIGN-BEST-PRACTICES.md` - Research-backed guidelines for creating high-quality AI agent skills
  - 10 core principles (cognitive load, progressive disclosure, scanability, etc.)
  - Based on Miller's Law, Sweller's Cognitive Load Theory, Kahneman's biases research
  - Templates and quality benchmarks
  - 40+ academic sources cited
- `REPOSITORY-STATUS.md` - Complete guide for repository access and integration

**Skills Library Quality:**
- **Total Skills:** 66 elite skills (100% high-quality, 0% templates)
- **Average Score:** 85+/100
- **Exemplary (90-100):** 8 skills (12%)
- **Strong (80-89):** 47 skills (71%)
- **Good/Adequate:** 11 skills (17%)

**Gold Standard Skills (90-100 score):**
- `think-quick-recognition` (91) - Cognitive bias diagnostic
- `dev-test-driven-development` (91) - TDD with "Iron Law"
- `think-solving-with-frameworks` (91) - Framework action mode
- `dev-systematic-debugging` (90) - Four-phase debugging framework
- `cc-writing-skills` (90) - TDD for skills creation
- `think-mitigation-strategies` (90) - Debiasing techniques
- `vault-maintaining-book-notes` (89) - Knowledge integration
- `think-context-aware-reasoning` (86) - Meta-framework

### Changed
- CLAUDE.md updated with comprehensive skills library documentation
- Skills organized by prefix-based categorization (dev-, think-, cc-, vault-, physical-)
- Flat directory structure maintained (no nested categories)

### Technical Details
- Total documentation added: 1,630 lines (680 + 950)
- Skills transformation complete: 135 → 66 elite skills
- All template skills removed (72 templates eliminated)
- 7 comprehensive skills created to replace templates
- Quality threshold: Minimum 60/100, target 80+/100

---

## [2.2.0] - 2025-11-09

### Added - Skills Transformation and Categorization

**Prefix-Based Categorization System:**
- `dev-` - Software Development (15 skills)
- `think-` - Thinking & Planning (19 skills)
- `cc-` - Claude Code Meta-skills (15 skills)
- `vault-` - Obsidian Vault/PKM (12 skills)
- `physical-` - Physical Training (5 skills)

**New Comprehensive Skills Created:**
1. `dev-security-fundamentals` - OWASP Top 10 2024 coverage
2. `dev-secrets-management` - Cloud secrets with zero-downtime rotation
3. `dev-secure-coding` - XSS, SQL injection, CSRF protection
4. `dev-system-design` - Architecture patterns with real examples
5. `dev-scalability-patterns` - Load balancing, caching, auto-scaling
6. `dev-query-optimization` - Index strategies, EXPLAIN plans
7. `dev-integration-tests` - Docker, Testcontainers, CI/CD

**Skills Quality Analysis:**
- Analyzed all 135 existing skills using `cc-skill-evaluator`
- Removed 72 template/placeholder skills (53% of library)
- Retained 56 high-quality skills (average 85+/100)
- Created 7 new comprehensive skills to fill gaps
- Final count: 66 elite skills (63 existing + 3 new during transformation)

**Documentation:**
- `.claude-state/COMPREHENSIVE-SKILLS-ANALYSIS.md` - Complete transformation analysis
- `TRANSFORMATION-SUMMARY.md` - Executive summary of changes
- All skills follow official Claude Code format

### Changed
- Skills library restructured with flat directory layout
- All skills renamed with prefix-based categorization
- Skills metadata updated with consistent format
- CLAUDE.md updated with skills organization documentation

### Removed
- 72 template/placeholder skills eliminated
- Nested category structure removed in favor of flat layout with prefixes

### Technical Details
- Skills transformation phases: Analysis → Removal → Creation → Categorization
- Quality scoring: 5 dimensions (Functional, Clarity, Modularity, Performance, Coverage)
- Score range: 0-100 (20 points per dimension)
- Prefix convention enables clear scope boundaries and easy discovery

---

## [2.1.1] - 2025-11-09

### Fixed
- **CRITICAL:** VERSION.lock format corrected from properties (`key=value`) to YAML (`key: "value"`)
- Field names now match specification: `harness_version`, `repo_url`, `installed_date`, `last_check`
- Version checking in session-start hook now works correctly
- harness-pull and harness-push commands can now parse VERSION.lock

### Changed
- VERSION.lock format is now strict YAML with quoted values

## [2.1.0] - 2025-11-09

### Added - Cross-Project Versioning System

**Harness Management Commands:**
- `/harness-install` - Interactive installation wizard for new projects
- `/harness-pull` - Pull updates from central repository with backup
- `/harness-push` - Contribute improvements back via automated PR
- `/harness-fix-after-update` - Comprehensive troubleshooting and diagnostics

**Version Management:**
- `.claude/VERSION.lock` - Tracks installed harness version and configuration
- CLAUDE.md marker system for clean core/project separation:
  - `<!-- HARNESS-CORE-BEGIN/END -->` - Auto-updated core content
  - `<!-- PROJECT-SPECIFIC-BEGIN/END -->` - Preserved project customizations
- Automatic version checking on session start (6-hour cache)
- State directory: `.claude-state/harness/` for backups and sync logs

**Enhanced Session Hook:**
- Version checking integrated into session-start hook
- Fast git ls-remote for update detection (no clone required)
- 5-second timeout with graceful offline handling
- Cached results to minimize session start latency

**Core Harness Components:**
- 5 specialist agents (orchestrator, architect, engineer, tester, reviewer)
- 110 core skills across 11 categories:
  - API (10 skills)
  - Architecture (10 skills)
  - Database (10 skills)
  - Debugging (10 skills)
  - Deployment (10 skills)
  - Development (10 skills)
  - Documentation (10 skills)
  - Refactoring (10 skills)
  - Security (10 skills)
  - Testing (10 skills)
- 3 lifecycle hooks (session-start, user-prompt-submit, stop)
- 3 prompts (decision-framework, question-batching, tdd-workflow)
- Complete CLAUDE.md specification

### Changed
- Session-start hook enhanced with version checking capabilities
- README.md updated with harness management documentation
- CLAUDE.md structured with marker sections for clean updates

### Features
- **Bidirectional Sync**: Pull updates from central, push improvements back
- **Safe Updates**: Automatic backups before every update operation
- **Project Isolation**: PROJ- prefix preserves project-specific customizations
- **Conflict Resolution**: Manual handling with .CONFLICT files
- **Semantic Versioning**: MAJOR.MINOR.PATCH with automatic bump calculation
- **Offline Support**: Full functionality when network unavailable

### Installation
- Central repository: `https://github.com/tkoenderink-prog/claude-code-dev-harness`
- Installation: Run `/harness-install` command
- Updates: Automatic check every 6 hours, manual with `/harness-pull`

### Technical Details
- Version tracking via `.claude/VERSION.lock` (YAML format)
- Backup system: Zip archives in `.claude-state/harness/backups/`
- Sync logging: `.claude-state/harness/sync-log.txt`
- Cache directory: `.claude-state/harness/remote-cache/`
- PROJ- prefix convention for project-specific files
- Marker-based CLAUDE.md splitting for clean updates

---

## Version Format

- **MAJOR**: Breaking changes, architectural redesign
- **MINOR**: New features, backward-compatible
- **PATCH**: Bug fixes, documentation updates
