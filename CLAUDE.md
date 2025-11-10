# Claude Code v2: Professional Autonomy Harness

<!-- HARNESS-CORE-BEGIN -->

## Mission Statement
Claude Code v2 enables autonomous software development with minimal human intervention.
Target: 30 minutes daily user interaction for full project progress.
Model: Professional autonomy with orchestrated specialist agents.

## Core Architecture

### Agent Hierarchy
```
User
  └── Orchestrator (Chief of Staff)
      ├── Architect (Technical Design)
      ├── Engineer (Implementation)
      ├── Tester (Quality Assurance)
      ├── Reviewer (Code Review)
      └── [Future: DevOps, Security, Performance]
```

### Communication Model
- **User ↔ Orchestrator**: Strategic decisions, question batches
- **Orchestrator ↔ Specialists**: Task delegation via Task tool
- **Specialists ↔ Skills**: Implementation via skill library
- **All Agents ↔ State**: Shared state via .claude-state/

## Decision Framework

### Decision Boundaries
```yaml
User Decisions (5%):
  - Business strategy and priorities
  - Major architectural directions
  - Resource allocation and budgets
  - External integrations approval
  - Production deployment authorization

Orchestrator Decisions (45%):
  - Task decomposition and planning
  - Agent coordination and routing
  - Question batching and timing
  - Progress tracking and reporting
  - State management and persistence

Specialist Decisions (50%):
  - Technical implementation details
  - Code structure and patterns
  - Testing strategies
  - Performance optimizations
  - Documentation approaches
```

### Escalation Criteria
1. **Always Escalate**: Legal, financial, security-critical, user data
2. **Batch & Escalate**: Multiple viable approaches, unclear requirements
3. **Decide Autonomously**: Clear technical path, established patterns

## Question Batching Strategy

### Batching Rules
1. **Frequency**: Maximum 2 batches per day (morning/afternoon)
2. **Threshold**: Accumulate 3+ questions before interrupting
3. **Priority**: P0 (blocker) can bypass batching
4. **Format**: Structured decision matrix with recommendations

### Question Template
```markdown
## Decision Batch - [Timestamp]

### Context
[Brief project state]

### Questions
1. **[Question]**
   - Option A: [Description] ✓ Recommended
   - Option B: [Description]
   - Impact: [High/Medium/Low]

2. **[Question]**
   - Option A: [Description]
   - Option B: [Description] ✓ Recommended
   - Impact: [High/Medium/Low]

### Default Actions
If no response by [time], will proceed with recommendations.
```

## State Management System

### State Files Location
All state stored in `.claude-state/` directory (gitignored).

### Core State Files

#### session.yaml
```yaml
session_id: uuid
started_at: timestamp
last_active: timestamp
current_task: string
current_agent: string
pending_questions: []
completed_tasks: []
active_threads: {}
```

#### preferences.yaml
```yaml
user_preferences:
  code_style: string
  test_framework: string
  documentation_format: string
  review_strictness: string

learned_patterns:
  - pattern: string
    confidence: float
    last_used: timestamp

project_conventions:
  - convention: string
    examples: []
```

#### decisions.yaml
```yaml
decisions:
  - id: uuid
    timestamp: datetime
    question: string
    options: []
    chosen: string
    rationale: string
    decided_by: user|orchestrator|agent
    outcome: string

patterns:
  - pattern: string
    frequency: int
    auto_decide: boolean
```

#### progress.yaml
```yaml
current_sprint:
  goal: string
  started: datetime
  tasks:
    - id: uuid
      description: string
      status: pending|active|completed|blocked
      assigned_to: agent_name
      started_at: timestamp
      completed_at: timestamp
      blockers: []

metrics:
  tasks_completed_today: int
  decisions_made: int
  questions_asked: int
  autonomous_success_rate: float
```

#### context.json
```json
{
  "project": {
    "name": "string",
    "type": "web|cli|library|api",
    "stack": [],
    "dependencies": {},
    "structure": {}
  },
  "recent_changes": [],
  "active_features": [],
  "known_issues": [],
  "test_results": {},
  "performance_metrics": {}
}
```

## Skill Library Organization

### Skill Categories (100 total skills)
1. **development/** - Core coding skills
2. **testing/** - Test creation and execution
3. **architecture/** - Design and structure
4. **debugging/** - Issue resolution
5. **refactoring/** - Code improvement
6. **api/** - API design and integration
7. **database/** - Data modeling and queries
8. **deployment/** - CI/CD and releases
9. **security/** - Security practices
10. **documentation/** - Docs and comments

### Skill Metadata Structure
```yaml
name: skill-name
category: category-name
trigger: when to use this skill
expertise: beginner|intermediate|expert
time_estimate: estimated-time
dependencies: [other-skills]
```

### Skill Selection Algorithm
1. Parse user request for keywords
2. Match against skill triggers
3. Check skill dependencies
4. Estimate time requirements
5. Return skill chain for execution

### Project Skills Repository

This project includes a comprehensive local skills repository in `.claude/skills/`:

**Total Skills:** 136 active skills
- **Converted Skills:** 77 (from old categorized structure)
- **User Skills:** 38 (from ~/.claude/skills/)
- **Plugin Skills:** 20 (from Superpowers plugin)
- **Local Skills:** 1 (fixing-claude-code-hooks)

**Structure:** Official Claude Code format - flat directory with `skill-name/SKILL.md`

**Usage:**
```
Skill(skill-name)
```

**Categories:**
- Architecture (10) - System design patterns
- Database (10) - DB optimization & patterns
- Debugging (10) - Debugging techniques
- Deployment (7) - CI/CD strategies
- Development (10) - Core dev practices
- Documentation (10) - Technical writing
- Security (10) - Security practices
- Testing (10) - Testing strategies
- Meta (4) - Skills about skills
- Superpowers (17) - Dev workflows
- Obsidian (8) - Knowledge management
- Physical Training (5) - Workout programs
- Knowledge Resources (7) - Mental models
- Cognitive Biases (5) - Bias awareness
- Problem Solving (6) - Problem-solving
- Other (7) - Specialized skills

**Synchronization:** Update from global sources:
```bash
./sync-skills.sh
```

**Health Checks:** Validate structure:
```bash
./check-skills-health.sh
```

**Documentation:** See `.claude/skills/README.md` and `skills/README.md` for complete catalogs.

**Key Skills for Development:**
- `systematic-debugging` - Four-phase debugging framework
- `test-driven-development` - RED-GREEN-REFACTOR cycle
- `writing-skills` - TDD approach to creating skills
- `api-design` - REST/GraphQL API design
- `tdd-implementation` - TDD practices
- `fixing-claude-code-hooks` - Diagnose hook errors
- `root-cause-analysis` - RCA methodology
- `security-testing` - Security test strategies

## Workflow Patterns

### Standard Development Workflow
```mermaid
graph LR
    Request --> Orchestrator
    Orchestrator --> Architect[Design]
    Architect --> Engineer[Implement]
    Engineer --> Tester[Test]
    Tester --> Reviewer[Review]
    Reviewer --> Orchestrator
    Orchestrator --> Complete
```

### TDD Workflow
```mermaid
graph LR
    Requirement --> Tester[Write Tests]
    Tester --> Engineer[Implementation]
    Engineer --> Tester2[Run Tests]
    Tester2 --> Reviewer[Code Review]
    Reviewer --> Complete
```

### Debugging Workflow
```mermaid
graph LR
    Issue --> Tester[Reproduce]
    Tester --> Engineer[Investigate]
    Engineer --> Architect[Root Cause]
    Architect --> Engineer2[Fix]
    Engineer2 --> Tester2[Verify]
    Tester2 --> Complete
```

## Agent Capabilities

### Orchestrator
- **Primary Role**: Chief of Staff, user interface
- **Tools**: Task, TodoWrite, Read, Write, Edit, Grep, Glob, Bash
- **Decisions**: Task routing, question batching, progress tracking
- **Skills**: orchestration-*, state-*, planning-*

### Architect
- **Primary Role**: Technical design and architecture
- **Tools**: Read, Write, Edit, Grep, Glob, WebSearch
- **Decisions**: Design patterns, architecture, technology choices
- **Skills**: architecture-*, design-*, pattern-*

### Engineer
- **Primary Role**: Code implementation
- **Tools**: Read, Write, Edit, Bash, Grep, Glob
- **Decisions**: Implementation details, code structure
- **Skills**: development-*, refactoring-*, api-*

### Tester
- **Primary Role**: Quality assurance
- **Tools**: Bash, Read, Write, Edit, Grep
- **Decisions**: Test strategies, coverage requirements
- **Skills**: testing-*, debugging-*, validation-*

### Reviewer
- **Primary Role**: Code review and standards
- **Tools**: Read, Grep, Glob, Edit
- **Decisions**: Code quality, standards compliance
- **Skills**: review-*, documentation-*, security-*

## Hook System

### Available Hooks
1. **SessionStart**: Load state, resume context
2. **SessionEnd**: Save state, summarize progress
3. **TaskComplete**: Update progress, trigger next

### Hook Execution Flow
```
User Input
    → SessionStart Hook (load state)
    → Orchestrator (process)
    → Specialists (execute)
    → TaskComplete Hook (update)
    → SessionEnd Hook (save)
```

## Success Metrics

### Autonomy Metrics
- **Decision Autonomy**: >95% decisions without user
- **Task Completion**: >80% tasks completed first try
- **Question Efficiency**: <2 interruptions/day
- **State Coherence**: 100% state consistency

### Quality Metrics
- **Test Coverage**: >80% on new code
- **Review Pass Rate**: >90% first review
- **Bug Introduction**: <1 per 100 lines
- **Documentation**: 100% public APIs

### Performance Metrics
- **Response Time**: <30s for decisions
- **Task Throughput**: 10+ tasks/day
- **Skill Utilization**: >50% skills used/week
- **State Size**: <10MB total

## File References

### Agent Files
- `agents/orchestrator.md` - Chief of Staff agent
- `agents/architect.md` - Technical design agent
- `agents/engineer.md` - Implementation agent
- `agents/tester.md` - QA agent
- `agents/reviewer.md` - Code review agent

### Key Skills
- `skills/development/tdd-implementation.md`
- `skills/testing/test-strategy-design.md`
- `skills/architecture/system-design.md`
- `skills/debugging/root-cause-analysis.md`
- `skills/refactoring/code-cleanup.md`

### Hooks
- `hooks/SessionStart.md` - Session initialization
- `hooks/SessionEnd.md` - Session cleanup
- `hooks/TaskComplete.md` - Task completion

### Prompts
- `prompts/decision-framework.md` - Decision logic
- `prompts/question-batching.md` - Batching rules
- `prompts/tdd-workflow.md` - TDD process

## Quick Start Guide

### First Session
1. Orchestrator reads `SessionStart` hook
2. Loads state from `.claude-state/`
3. Presents current context to user
4. Begins autonomous operation

### Task Execution
1. User provides high-level goal
2. Orchestrator decomposes into tasks
3. Delegates to specialists via Task tool
4. Specialists execute using skills
5. Progress tracked in state files

### Question Handling
1. Questions accumulated in `pending_questions`
2. Batched when threshold reached
3. Presented with recommendations
4. Defaults applied if no response

## Configuration

### Environment Variables
```bash
CLAUDE_AUTONOMY_LEVEL=high|medium|low
CLAUDE_BATCH_THRESHOLD=3
CLAUDE_BATCH_TIMEOUT=30m
CLAUDE_STATE_DIR=.claude-state
```

### Customization Points
1. Adjust decision boundaries in agents
2. Modify skill triggers and expertise
3. Configure state schemas
4. Customize hook behaviors
5. Tune batching thresholds

## Troubleshooting

### Common Issues
1. **State Corruption**: Delete `.claude-state/`, restart
2. **Skill Not Found**: Check skill category and name
3. **Agent Timeout**: Increase timeout in Task tool
4. **Question Overflow**: Reduce batch threshold

### Debug Mode
Enable debug output:
```bash
CLAUDE_DEBUG=true
CLAUDE_LOG_LEVEL=verbose
```

## Best Practices

### For Users
1. Provide clear, high-level goals
2. Respond to question batches promptly
3. Review daily progress summaries
4. Trust autonomous decisions

### For Developers
1. Keep agents under 100 lines
2. Put details in skills, not agents
3. Use state files for persistence
4. Reference skills, don't duplicate
5. Test hooks independently

## Version History
- v2.0.0 - Professional Autonomy model
- v1.0.0 - Basic automation
- v0.1.0 - Initial prototype

## License and Attribution
Claude Code v2 - Professional Autonomy Harness
Developed for 30-minute daily interaction goal
Based on Option 2 design specification

<!-- HARNESS-CORE-END -->
