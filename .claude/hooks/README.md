# Claude Code Hook System

Complete implementation of skill usage tracking and conversation archiving hooks.

## Overview

This hook system provides:

1. **Skill Usage Tracking** - Tracks every Skill tool invocation
2. **Conversation Archiving** - Archives main session transcripts
3. **Subagent Archiving** - Archives subagent (Task) conversation logs
4. **Error Resilience** - Never crashes Claude Code (always exits 0)
5. **Performance** - <10 seconds execution time per hook

## Architecture

```
.claude/hooks/
├── lib/                          # Shared libraries
│   ├── common.py                 # File locking, JSON utils, logging
│   ├── sanitizer.py              # Sensitive data removal
│   ├── skill_tracker.py          # Skill usage tracking logic
│   └── conversation_archiver.py  # Conversation archiving logic
├── post-tool-use                 # NEW: Skill tracking hook
├── subagent-stop                 # NEW: Subagent archiving hook
├── stop                          # UPDATED: Main session archiving
├── session-start                 # Existing hook
├── user-prompt-submit            # Existing hook
└── test-hooks.sh                 # Test suite

.claude-state/logs/
├── skill-usage.json              # Aggregate skill usage data
├── hook-errors.log               # Hook error log
├── main-session/                 # Main session archives
│   └── YYYY-MM/
│       ├── YYYY-MM-DD_HH-MM-SS_{session_id}.jsonl
│       ├── YYYY-MM-DD_HH-MM-SS_{session_id}.meta.json
│       └── index.json
└── subagent/                     # Subagent archives
    ├── architect/
    ├── engineer/
    ├── tester/
    ├── reviewer/
    └── orchestrator/
        └── YYYY-MM/
            ├── YYYY-MM-DD_HH-MM-SS_{task_id}.jsonl
            ├── YYYY-MM-DD_HH-MM-SS_{task_id}.meta.json
            └── index.json
```

## Hooks

### PostToolUse Hook (`post-tool-use`)

**Purpose:** Track Skill tool invocations

**Triggers:** After any Skill tool use

**What it tracks:**
- Skill name
- Session ID
- Context/reason for invocation
- Success/failure status
- Timestamp

**Performance:** <1 second

**Output:** Updates `.claude-state/logs/skill-usage.json`

### Stop Hook (`stop`)

**Purpose:** Archive main session conversations

**Triggers:** When Claude Code session ends

**What it does:**
- Updates session.yaml with end timestamp
- Copies transcript to archive
- Generates metadata (message count, tools used, skills invoked)
- Updates archive index
- Logs to last-session.json

**Performance:** <5 seconds

**Output:**
- `.claude-state/logs/main-session/YYYY-MM/...`
- Updates archive index

### SubagentStop Hook (`subagent-stop`)

**Purpose:** Archive subagent (Task) conversations

**Triggers:** When Task tool completes

**What it does:**
- Copies subagent transcript to archive
- Generates metadata (task ID, agent type, outcome)
- Updates subagent-specific index
- Correlates with parent session

**Performance:** <3 seconds

**Output:**
- `.claude-state/logs/subagent/{agent_type}/YYYY-MM/...`
- Updates archive index

## Data Schemas

### Skill Usage (`skill-usage.json`)

```json
{
  "schema_version": "1.0",
  "last_updated": "2025-11-10T09:52:22.279956",
  "total_invocations": 42,
  "skills": {
    "systematic-debugging": {
      "count": 5,
      "first_used": "2025-11-10T08:00:00Z",
      "last_used": "2025-11-10T09:52:22Z",
      "invocations": [...],
      "sessions": ["session-001", "session-002"],
      "success_count": 4,
      "failure_count": 1,
      "success_rate": 0.8,
      "avg_duration_ms": 1234
    }
  },
  "sessions": {
    "session-001": {
      "started": "2025-11-10T08:00:00Z",
      "skills_used": ["systematic-debugging", "tdd"],
      "total_invocations": 3
    }
  },
  "daily_stats": {
    "2025-11-10": {
      "invocations": 12,
      "unique_skills": ["systematic-debugging", "tdd", "api-design"],
      "unique_sessions": ["session-001", "session-002"]
    }
  }
}
```

### Archive Metadata (`*.meta.json`)

```json
{
  "schema_version": "1.0",
  "session_id": "abc123",
  "type": "main_session",
  "archived_at": "2025-11-10T10:00:00Z",
  "message_count": 47,
  "tool_calls": 23,
  "skills_used": ["systematic-debugging", "tdd"],
  "files_modified": ["/path/to/file.py"],
  "size_bytes": 125000,
  "sanitized": false,
  "archive_path": "main-session/2025-11/..."
}
```

## Configuration

Hooks are configured in `.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Skill",
        "type": "command",
        "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/post-tool-use"
      }
    ],
    "Stop": [
      {
        "type": "command",
        "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/stop"
      }
    ],
    "SubagentStop": [
      {
        "type": "command",
        "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/subagent-stop"
      }
    ]
  }
}
```

## Testing

Run the test suite:

```bash
./.claude/hooks/test-hooks.sh
```

This tests:
- ✓ post-tool-use hook execution
- ✓ Skill tracking functionality
- ✓ Multiple skill invocations
- ✓ Non-Skill tool filtering
- ✓ stop hook execution
- ✓ subagent-stop hook execution
- ✓ Directory structure
- ✓ Hook permissions
- ✓ Library syntax validation
- ✓ Error logging

## Manual Testing

### Test Skill Tracking

```bash
echo '{
  "tool_name": "Skill",
  "tool_input": {
    "skill_name": "test-skill",
    "context": "Manual test"
  },
  "session_id": "test-001"
}' | ./.claude/hooks/post-tool-use

# Check result
cat .claude-state/logs/skill-usage.json | python3 -m json.tool
```

### Test Stop Hook

```bash
echo '{
  "session_id": "test-002",
  "transcript_path": "/path/to/transcript.jsonl"
}' | ./.claude/hooks/stop

# Check result
ls -la .claude-state/logs/main-session/
cat .claude-state/last-session.json
```

### Test Subagent Hook

```bash
echo '{
  "task_id": "task-001",
  "agent_type": "architect",
  "parent_session_id": "test-003",
  "outcome": "success"
}' | ./.claude/hooks/subagent-stop

# Check result
ls -la .claude-state/logs/subagent/architect/
```

## Libraries

### `common.py`

Provides:
- `file_lock(path, timeout)` - File locking context manager
- `log_error(message, level)` - Error logging
- `load_json(path, default)` - JSON loading with defaults
- `save_json(path, data)` - Safe JSON saving
- `get_session_id(hook_input)` - Extract session ID
- `get_month_dir()` - Get YYYY-MM directory name
- `format_timestamp()` - Format timestamp for filenames
- `ensure_permissions(path)` - Set secure file permissions

### `sanitizer.py`

Provides:
- `sanitize_content(text)` - Remove sensitive data
- `sanitize_dict(data)` - Recursively sanitize dictionary
- `is_sensitive(text)` - Check if text contains sensitive data

Detects and removes:
- API keys
- Passwords
- Tokens
- Email addresses
- SSH keys
- AWS keys
- GitHub tokens
- JWTs
- Connection strings

### `skill_tracker.py`

Provides:
- `SkillTracker` class - Batched skill tracking
- `track_skill_usage()` - Convenience function

Features:
- Batched writes (10 invocations)
- File locking for concurrency
- Success rate calculation
- Session correlation
- Daily statistics

### `conversation_archiver.py`

Provides:
- `ConversationArchiver` class - Archive conversations

Features:
- Monthly organization (YYYY-MM)
- Metadata generation
- Transcript analysis
- Optional sanitization
- Index generation
- Session correlation

## Error Handling

All hooks follow these principles:

1. **Never crash Claude Code** - Always exit 0
2. **Graceful degradation** - Continue even if logging fails
3. **Silent errors** - Log to `.claude-state/logs/hook-errors.log`
4. **Auto-recovery** - Next invocation retries
5. **Minimal performance impact** - Fast failures

Error log format:

```
[2025-11-10T10:00:00] [ERROR] Failed to flush skill tracking: [Errno 13] Permission denied
[2025-11-10T10:00:01] [WARNING] Transcript not found: /path/to/missing.jsonl
[2025-11-10T10:00:02] [INFO] Archived session abc123
```

## Performance

Target performance (met):
- PostToolUse: <1 second
- Stop: <5 seconds
- SubagentStop: <3 seconds
- Total per session: <10 seconds

Optimizations:
- Batched writes (10x)
- File locking with timeout
- In-memory caching
- Async operations where possible
- Minimal JSON parsing

## Security

Security features:
- Sanitizer removes sensitive data
- File permissions: 0600 (rw-------)
- Directory permissions: 0700 (rwx------)
- No network access
- Audit logging

## Maintenance

### View Skill Usage

```bash
# All skills
cat .claude-state/logs/skill-usage.json | python3 -m json.tool

# Top 10 skills
cat .claude-state/logs/skill-usage.json | \
  python3 -c "import json, sys; data=json.load(sys.stdin); \
  skills=sorted(data['skills'].items(), key=lambda x: x[1]['count'], reverse=True); \
  print('\\n'.join([f'{k}: {v[\"count\"]}' for k,v in skills[:10]]))"
```

### View Archives

```bash
# List main sessions
ls -lh .claude-state/logs/main-session/2025-11/

# List architect tasks
ls -lh .claude-state/logs/subagent/architect/2025-11/

# View metadata
cat .claude-state/logs/main-session/2025-11/*.meta.json | python3 -m json.tool
```

### Clean Up Old Archives

```bash
# Delete archives older than 6 months
find .claude-state/logs/main-session -type d -name "2025-*" -mtime +180 -exec rm -rf {} \;
find .claude-state/logs/subagent -type d -name "2025-*" -mtime +180 -exec rm -rf {} \;
```

### Check Hook Errors

```bash
# View recent errors
tail -50 .claude-state/logs/hook-errors.log

# Count errors by type
grep -oP '\[(ERROR|WARNING|INFO)\]' .claude-state/logs/hook-errors.log | sort | uniq -c
```

## Troubleshooting

### Hook not executing

```bash
# Check if hook is executable
ls -la .claude/hooks/post-tool-use

# Make executable
chmod +x .claude/hooks/post-tool-use
```

### Skill tracking not working

```bash
# Check error log
cat .claude-state/logs/hook-errors.log

# Test hook manually
echo '{"tool_name":"Skill","tool_input":{"skill_name":"test"}}' | \
  ./.claude/hooks/post-tool-use

# Check file permissions
ls -la .claude-state/logs/skill-usage.json
```

### Import errors

```bash
# Check Python syntax
python3 -m py_compile .claude/hooks/lib/skill_tracker.py

# Test import
python3 -c "import sys; sys.path.insert(0, '.claude/hooks/lib'); import skill_tracker"
```

### File locking issues

```bash
# Check for stale lock files
find .claude-state/logs -name "*.lock"

# Remove stale locks (only if no Claude Code running!)
find .claude-state/logs -name "*.lock" -delete
```

## Future Enhancements

Potential improvements:
- [ ] Async archiving (background process)
- [ ] Compression for old archives (gzip)
- [ ] Full-text search index
- [ ] Web dashboard for analytics
- [ ] Export to CSV/Excel
- [ ] Skill recommendation engine
- [ ] Performance profiling per skill
- [ ] Cost tracking (token usage)

## References

- Architecture: `docs/HOOK-SYSTEM-ARCHITECTURE.md`
- Implementation Guide: `docs/HOOK-IMPLEMENTATION-GUIDE.md`
- Decision Matrix: `docs/HOOK-SYSTEM-DECISION-MATRIX.md`
- Diagrams: `docs/HOOK-SYSTEM-DIAGRAMS.md`

---

**Version:** 1.0.0
**Implemented:** 2025-11-10
**Status:** Production Ready
