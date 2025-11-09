# Claude Code Development Harness

Professional autonomy system for Claude Code enabling 30-minute daily interaction for full project progress.

## Version: 2.1.0

## Overview

The Claude Code Development Harness is a comprehensive framework that enables autonomous software development with minimal human intervention. It provides a complete set of agents, skills, and workflows to handle complex development tasks.

## Features

- **5 Specialist Agents**: Orchestrator, Architect, Engineer, Tester, Reviewer
- **110 Core Skills** across 11 categories:
  - API Design & Integration
  - Architecture & System Design
  - Database Design & Optimization
  - Debugging & Troubleshooting
  - Deployment & DevOps
  - Development Patterns
  - Documentation
  - Refactoring
  - Security
  - Testing
- **Smart Orchestration**: Intelligent task routing and delegation
- **TDD Workflow**: Tests-first development pattern
- **Decision Framework**: 95%+ autonomous decision-making
- **State Management**: Persistent context across sessions

## Installation

### ⚠️ Important: Bootstrap Required

You **cannot** run `/harness-install` in a new project because that command doesn't exist until the harness is installed (chicken-and-egg problem). Use one of the bootstrap methods below for first-time installation.

### Method 1: One-Line Install (Easiest)

```bash
curl -sSL https://raw.githubusercontent.com/tkoenderink-prog/claude-code-dev-harness/main/install.sh | bash
```

This will:
- Clone the harness repository
- Install all files to your current directory
- Set correct permissions
- Create VERSION.lock and state directories
- Update .gitignore

### Method 2: Manual Install

```bash
# In your project directory
git clone --depth 1 https://github.com/tkoenderink-prog/claude-code-dev-harness.git /tmp/harness
cp -r /tmp/harness/.claude .
cp /tmp/harness/CLAUDE.md .
chmod +x .claude/hooks/*
mkdir -p .claude-state/harness/{backups,remote-cache}
echo ".claude-state/" >> .gitignore
rm -rf /tmp/harness
```

Then create `.claude/VERSION.lock`:
```yaml
harness_version: "2.1.0"
installed_date: "2025-11-09"
repo_url: "https://github.com/tkoenderink-prog/claude-code-dev-harness"
last_check: "2025-11-09T00:00:00Z"
cache_duration_hours: 6
```

### Method 3: Ask Claude Code

If you're already in Claude Code, just ask:

```
Please install the Claude Code harness from
https://github.com/tkoenderink-prog/claude-code-dev-harness

Follow the bootstrap procedure from BOOTSTRAP.md
```

### After Installation

Once installed, you'll have:
- ✅ All `/harness-*` commands available
- ✅ Automatic update checking every 6 hours
- ✅ Complete agent and skill library
- ✅ State management and version tracking

**Verify installation:**
```bash
ls -la .claude/
cat .claude/VERSION.lock
```

For detailed bootstrap instructions, see [BOOTSTRAP.md](BOOTSTRAP.md)

## Directory Structure

```
.claude/
├── agents/               # 5 specialist agents
│   ├── orchestrator.md  # Chief of Staff
│   ├── architect.md     # Technical design
│   ├── engineer.md      # Implementation
│   ├── tester.md        # Quality assurance
│   └── reviewer.md      # Code review
├── skills/              # 110 core skills
│   ├── api/
│   ├── architecture/
│   ├── database/
│   ├── debugging/
│   ├── deployment/
│   ├── development/
│   ├── documentation/
│   ├── refactoring/
│   ├── security/
│   └── testing/
├── hooks/               # Lifecycle hooks
│   ├── session-start
│   ├── user-prompt-submit
│   └── stop
├── prompts/             # Prompt templates
│   ├── decision-framework.md
│   ├── question-batching.md
│   └── tdd-workflow.md
├── commands/            # Slash commands (Phase 3)
└── settings.json        # Configuration
```

## Project-Specific Customization

You can add project-specific agents and skills using the `PROJ-` prefix:

```
.claude/
├── agents/
│   ├── PROJ-domain-expert.md    # Your custom agent
│   └── orchestrator.md           # Core harness (don't modify)
└── skills/
    └── development/
        ├── PROJ-business-rules.md  # Your custom skill
        └── tdd-implementation.md   # Core harness (don't modify)
```

**Important**: Files with `PROJ-` prefix will be preserved during harness updates.

## Usage

### Basic Workflow

1. **Start a session**: Claude loads harness automatically via session-start hook
2. **Give high-level goal**: "Create a REST API for user management"
3. **Orchestrator takes over**: Delegates to specialists
4. **Autonomous execution**: Minimal questions, maximum progress

### Example Task

```
User: "Implement user authentication with JWT tokens"

Orchestrator:
- Delegates to Architect for design
- Architect creates API design
- Delegates to Engineer for implementation
- Engineer writes code and tests
- Delegates to Tester for verification
- Tester runs tests
- Delegates to Reviewer for code review
- Reviewer checks quality

Result: Complete, tested, reviewed implementation
```

## Configuration

Edit `.claude/settings.json` to customize:

```json
{
  "allow_all_tools": false,
  "tool_allowlist": {
    "orchestrator": ["Task", "TodoWrite", "Read", "Write", "Edit", "Grep", "Glob", "Bash"],
    "architect": ["Read", "Write", "Edit", "Grep", "Glob"],
    "engineer": ["Read", "Write", "Edit", "Bash", "Grep", "Glob"],
    "tester": ["Bash", "Read", "Write", "Edit", "Grep"],
    "reviewer": ["Read", "Grep", "Glob", "Edit"]
  }
}
```

## Harness Management Commands

The harness includes built-in version management commands:

- **`/harness-install`** - Install harness into new project
  - Interactive installation wizard
  - Creates CLAUDE.md with marker sections
  - Sets up VERSION.lock for version tracking
  - Creates state directory structure

- **`/harness-pull`** - Pull updates from central repository
  - Checks for new versions
  - Shows changelog before updating
  - Creates automatic backups
  - Preserves PROJECT-SPECIFIC content and PROJ- files
  - Safe, reversible updates

- **`/harness-push`** - Contribute improvements back
  - Detects changed core files
  - Creates pull request automatically
  - Handles version bumping
  - Updates CHANGELOG.md

- **`/harness-fix-after-update`** - Troubleshoot issues
  - Comprehensive diagnostics
  - Auto-fixes common problems
  - Validates file integrity
  - Emergency rollback procedures

### Automatic Update Checking

The session-start hook automatically checks for harness updates:
- Checks every 6 hours (configurable)
- Fast git ls-remote (no clone required)
- 5-second timeout for network operations
- Works offline (graceful failure)
- Cached results to minimize latency

## Version History

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

## Architecture

The harness follows a hierarchical agent model:

```
User
  └── Orchestrator (Chief of Staff)
      ├── Architect (Technical Design)
      ├── Engineer (Implementation)
      ├── Tester (Quality Assurance)
      └── Reviewer (Code Review)
```

Each agent:
- Has specific decision authority
- Uses focused skill sets
- Delegates when appropriate
- Maintains autonomous operation

## Contributing

Improvements and contributions are welcome!

Future versions will support automated contribution via `/harness-push` command.

## Support

For issues or questions:
- Create an issue on GitHub
- Review [CLAUDE.md](CLAUDE.md) for complete specification

## License

MIT License - See [LICENSE](LICENSE) file

## Acknowledgments

Built for Claude Code v2 Professional Autonomy model.
Target: 30 minutes daily user interaction for full project progress.
