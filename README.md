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

## Quick Install

### Prerequisites
- Claude Code environment
- Git

### Installation Steps

1. **Clone this repository**:
   ```bash
   cd /tmp
   git clone https://github.com/tkoenderink-prog/claude-code-dev-harness.git
   cd claude-code-dev-harness
   ```

2. **Copy to your project**:
   ```bash
   # Set your project directory
   export PROJECT_DIR=/path/to/your/project

   # Copy harness files
   mkdir -p $PROJECT_DIR/.claude
   cp -r .claude/* $PROJECT_DIR/.claude/
   cp CLAUDE.md $PROJECT_DIR/

   # Add to gitignore
   echo ".claude-state/" >> $PROJECT_DIR/.gitignore
   ```

3. **Verify installation**:
   ```bash
   cd $PROJECT_DIR
   ls -la .claude/
   ```

You should see:
- `agents/` - 5 core agents
- `skills/` - 11 skill categories
- `hooks/` - 3 lifecycle hooks
- `prompts/` - 3 prompt templates
- `commands/` - Empty (for future slash commands)
- `settings.json` - Configuration

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
