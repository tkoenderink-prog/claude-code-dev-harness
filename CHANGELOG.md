# Changelog

All notable changes to the Claude Code Development Harness will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
