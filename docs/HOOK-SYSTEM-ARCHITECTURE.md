# Hook System Architecture - Technical Design Document

**Version:** 1.0
**Date:** 2025-11-10
**Status:** Design Complete - Ready for Implementation
**Architect:** Claude Sonnet 4.5

---

## Executive Summary

This document specifies a comprehensive hook system architecture for Claude Code that implements:
1. **Skill Usage Tracking** via PostToolUse hooks
2. **Conversation Archiving** for main sessions and subagents
3. **Fast, non-blocking, error-resilient execution**

**Key Metrics:**
- Execution time: <10 seconds per hook
- Error resilience: 100% (never crash Claude Code)
- Security: Safe handling of sensitive data
- Storage: Organized, searchable, indexed

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Directory Structure](#directory-structure)
3. [Data Schemas](#data-schemas)
4. [Hook Specifications](#hook-specifications)
5. [Settings Configuration](#settings-configuration)
6. [Error Handling Strategy](#error-handling-strategy)
7. [Performance Optimization](#performance-optimization)
8. [Security Considerations](#security-considerations)
9. [Testing Strategy](#testing-strategy)
10. [Implementation Plan](#implementation-plan)

---

## 1. System Overview

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     Claude Code Session                      │
└─────────────────────┬───────────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
  SessionStart   PostToolUse    UserPromptSubmit
      Hook          Hook            Hook
        │             │             │
        │             │             │
        ▼             ▼             ▼
  ┌─────────────────────────────────────┐
  │      Logging & Tracking System      │
  ├─────────────────────────────────────┤
  │  • Skill Usage Tracker              │
  │  • Conversation Archiver            │
  │  • Index Generator                  │
  └─────────────────────────────────────┘
                      │
                      ▼
  ┌─────────────────────────────────────┐
  │      .claude-state/logs/            │
  ├─────────────────────────────────────┤
  │  • skill-usage.json                 │
  │  • main-session/YYYY-MM/            │
  │  • subagent/{type}/YYYY-MM/         │
  │  • index.json                       │
  └─────────────────────────────────────┘
```

### Component Responsibilities

| Component | Responsibility | Execution Time |
|-----------|---------------|----------------|
| **skill-usage-tracker** | Track Skill tool invocations | <1s |
| **conversation-archiver** | Archive main session logs | <5s |
| **subagent-archiver** | Archive subagent logs | <3s |
| **index-generator** | Generate searchable indexes | <2s |
| **sanitizer** | Remove sensitive data | <1s |

---

## 2. Directory Structure

### Complete File Tree

```
.claude-state/
├── logs/
│   ├── skill-usage.json              # Aggregate skill usage data
│   ├── skill-usage-index.json        # Searchable skill usage index
│   ├── main-session/                 # Main conversation archives
│   │   ├── 2025-01/
│   │   │   ├── 2025-01-10_14-30-00_abc123.jsonl
│   │   │   ├── 2025-01-10_14-30-00_abc123.meta.json
│   │   │   ├── 2025-01-15_09-15-30_def456.jsonl
│   │   │   └── 2025-01-15_09-15-30_def456.meta.json
│   │   ├── 2025-02/
│   │   │   └── ...
│   │   └── index.json                # Main session index
│   ├── subagent/                     # Subagent conversation archives
│   │   ├── architect/
│   │   │   ├── 2025-01/
│   │   │   │   ├── 2025-01-10_14-35-00_task-xyz.jsonl
│   │   │   │   └── 2025-01-10_14-35-00_task-xyz.meta.json
│   │   │   └── index.json
│   │   ├── engineer/
│   │   │   ├── 2025-01/
│   │   │   └── index.json
│   │   ├── tester/
│   │   ├── reviewer/
│   │   └── orchestrator/
│   ├── sanitized/                    # Sanitized versions (if needed)
│   │   └── ...
│   └── archive-index.json            # Global archive index
└── harness/                          # Existing harness state
    └── ...

.claude/
├── hooks/
│   ├── session-start                 # Existing
│   ├── user-prompt-submit            # Existing (updated)
│   ├── stop                          # Existing (updated)
│   ├── post-tool-use                 # NEW: Skill tracking
│   ├── subagent-stop                 # NEW: Subagent archiving
│   └── lib/                          # Shared utilities
│       ├── skill_tracker.py
│       ├── conversation_archiver.py
│       ├── sanitizer.py
│       ├── indexer.py
│       └── common.py
├── settings.json                     # Updated configuration
└── ...
```

### Directory Ownership

| Directory | Purpose | Size Estimate | Retention |
|-----------|---------|---------------|-----------|
| `logs/skill-usage.json` | Skill tracking | ~100KB | Forever |
| `logs/main-session/` | Main conversations | ~1MB/month | 6 months |
| `logs/subagent/` | Subagent conversations | ~500KB/month | 6 months |
| `logs/index.json` | Search indexes | ~50KB | Forever |

---

## 3. Data Schemas

### 3.1 Skill Usage Schema

**File:** `.claude-state/logs/skill-usage.json`

```json
{
  "schema_version": "1.0",
  "last_updated": "2025-01-10T14:30:00Z",
  "total_invocations": 1234,
  "skills": {
    "systematic-debugging": {
      "count": 42,
      "first_used": "2025-01-05T10:15:00Z",
      "last_used": "2025-01-10T14:25:00Z",
      "invocations": [
        {
          "timestamp": "2025-01-10T14:25:00Z",
          "session_id": "abc123",
          "context": "Debugging authentication issue",
          "success": true,
          "duration_ms": 1234
        }
      ],
      "sessions": ["abc123", "def456", "ghi789"],
      "success_rate": 0.95,
      "avg_duration_ms": 1500
    },
    "test-driven-development": {
      "count": 38,
      "first_used": "2025-01-06T09:00:00Z",
      "last_used": "2025-01-10T13:45:00Z",
      "invocations": [],
      "sessions": ["abc123", "xyz999"],
      "success_rate": 1.0,
      "avg_duration_ms": 2100
    }
  },
  "sessions": {
    "abc123": {
      "started": "2025-01-10T14:00:00Z",
      "ended": "2025-01-10T15:30:00Z",
      "skills_used": ["systematic-debugging", "test-driven-development"],
      "total_invocations": 5
    }
  },
  "daily_stats": {
    "2025-01-10": {
      "invocations": 12,
      "unique_skills": 7,
      "sessions": 3
    }
  }
}
```

**Key Features:**
- Aggregate counts per skill
- Full invocation history (last 100 per skill)
- Session correlation
- Success rate tracking
- Performance metrics

### 3.2 Skill Usage Index Schema

**File:** `.claude-state/logs/skill-usage-index.json`

```json
{
  "schema_version": "1.0",
  "generated_at": "2025-01-10T14:30:00Z",
  "indexes": {
    "by_skill": {
      "systematic-debugging": [
        "2025-01-10T14:25:00Z|abc123",
        "2025-01-09T11:15:00Z|def456"
      ]
    },
    "by_session": {
      "abc123": [
        "systematic-debugging",
        "test-driven-development"
      ]
    },
    "by_date": {
      "2025-01-10": [
        "systematic-debugging",
        "test-driven-development",
        "api-design"
      ]
    },
    "by_category": {
      "development": ["systematic-debugging", "test-driven-development"],
      "architecture": ["api-design", "system-design"]
    }
  },
  "stats": {
    "total_skills_ever_used": 45,
    "total_sessions_tracked": 123,
    "date_range": {
      "start": "2025-01-01",
      "end": "2025-01-10"
    }
  }
}
```

### 3.3 Conversation Archive Metadata Schema

**File:** `.claude-state/logs/main-session/2025-01/2025-01-10_14-30-00_abc123.meta.json`

```json
{
  "schema_version": "1.0",
  "session_id": "abc123",
  "type": "main_session",
  "started_at": "2025-01-10T14:30:00Z",
  "ended_at": "2025-01-10T15:45:00Z",
  "duration_seconds": 4500,
  "message_count": 47,
  "tool_calls": 23,
  "skills_used": ["systematic-debugging", "test-driven-development"],
  "agents_invoked": ["architect", "engineer"],
  "files_modified": [
    "/path/to/file1.py",
    "/path/to/file2.js"
  ],
  "summary": "Implemented authentication system with JWT tokens",
  "tags": ["authentication", "security", "jwt"],
  "sanitized": false,
  "archive_path": "main-session/2025-01/2025-01-10_14-30-00_abc123.jsonl",
  "size_bytes": 125000,
  "hash": "sha256:abc123def456..."
}
```

### 3.4 Subagent Archive Metadata Schema

**File:** `.claude-state/logs/subagent/architect/2025-01/2025-01-10_14-35-00_task-xyz.meta.json`

```json
{
  "schema_version": "1.0",
  "task_id": "task-xyz",
  "agent_type": "architect",
  "parent_session_id": "abc123",
  "started_at": "2025-01-10T14:35:00Z",
  "ended_at": "2025-01-10T14:42:00Z",
  "duration_seconds": 420,
  "message_count": 12,
  "tool_calls": 5,
  "task_description": "Design authentication API endpoints",
  "outcome": "success",
  "deliverables": ["API specification", "Data model"],
  "archive_path": "subagent/architect/2025-01/2025-01-10_14-35-00_task-xyz.jsonl",
  "size_bytes": 25000,
  "hash": "sha256:xyz789abc123..."
}
```

### 3.5 Global Archive Index Schema

**File:** `.claude-state/logs/archive-index.json`

```json
{
  "schema_version": "1.0",
  "generated_at": "2025-01-10T15:00:00Z",
  "main_sessions": {
    "count": 123,
    "date_range": {
      "start": "2025-01-01",
      "end": "2025-01-10"
    },
    "by_month": {
      "2025-01": 15,
      "2024-12": 23
    },
    "total_size_bytes": 15000000
  },
  "subagent_sessions": {
    "count": 456,
    "by_agent": {
      "architect": 120,
      "engineer": 200,
      "tester": 80,
      "reviewer": 56
    },
    "total_size_bytes": 5000000
  },
  "search_index": {
    "by_session_id": {
      "abc123": "main-session/2025-01/2025-01-10_14-30-00_abc123.jsonl"
    },
    "by_date": {
      "2025-01-10": [
        "main-session/2025-01/2025-01-10_14-30-00_abc123.jsonl",
        "subagent/architect/2025-01/2025-01-10_14-35-00_task-xyz.jsonl"
      ]
    },
    "by_tag": {
      "authentication": ["abc123", "def456"],
      "security": ["abc123", "ghi789"]
    },
    "by_skill": {
      "systematic-debugging": ["abc123", "jkl012"]
    }
  }
}
```

---

## 4. Hook Specifications

### 4.1 PostToolUse Hook - Skill Tracker

**File:** `.claude/hooks/post-tool-use`

**Purpose:** Track every Skill tool invocation for usage analytics

**Trigger:** After any tool use (filtered by matcher)

**Matcher:** `Skill`

**Input:**
```json
{
  "tool_name": "Skill",
  "tool_input": {
    "skill_name": "systematic-debugging",
    "context": "Debugging authentication issue"
  },
  "tool_output": "Skill execution result...",
  "session_id": "abc123"
}
```

**Output:**
```json
{
  "continue": true,
  "suppressOutput": true
}
```

**Performance Requirements:**
- Execution time: <1 second
- Async file write (non-blocking)
- Batch updates every 10 invocations

**Error Handling:**
- Never fail (exit 0 always)
- Log errors to `.claude-state/logs/hook-errors.log`
- Graceful degradation on file lock

**Implementation Notes:**
- Use file locking for concurrent writes
- Keep last 100 invocations per skill (circular buffer)
- Update indexes asynchronously
- Cache skill metadata in memory

### 4.2 UserPromptSubmit Hook - Incremental Archiver

**File:** `.claude/hooks/user-prompt-submit` (UPDATE EXISTING)

**Purpose:** Archive user prompts incrementally

**Trigger:** Before processing user prompt

**Input:**
```json
{
  "userInput": "Design authentication system",
  "prompt": "Design authentication system",
  "session_id": "abc123"
}
```

**Output:**
```json
{
  "continue": true
}
```

**Performance Requirements:**
- Execution time: <0.5 seconds
- Append-only writes
- No blocking operations

**Implementation:**
- Append prompt to session log file
- Update session metadata (message count)
- No index generation (done at SessionEnd)

### 4.3 Stop Hook - Session Archiver

**File:** `.claude/hooks/stop` (UPDATE EXISTING)

**Purpose:** Finalize session archiving and generate indexes

**Trigger:** When Claude finishes responding or session ends

**Input:**
```json
{
  "session_id": "abc123",
  "hook_event_name": "Stop"
}
```

**Output:**
```json
{
  "continue": true
}
```

**Performance Requirements:**
- Execution time: <5 seconds
- Copy transcript file
- Generate metadata
- Update indexes

**Implementation:**
1. Copy transcript from Claude's location to archive
2. Generate metadata (session stats, skills used, etc.)
3. Update global index
4. Sanitize if needed
5. Clean up old archives (retention policy)

### 4.4 SubagentStop Hook - Subagent Archiver

**File:** `.claude/hooks/subagent-stop` (NEW)

**Purpose:** Archive subagent conversation logs

**Trigger:** When Task tool (subagent) completes

**Input:**
```json
{
  "task_id": "task-xyz",
  "agent_type": "architect",
  "parent_session_id": "abc123",
  "transcript_path": "/path/to/subagent.jsonl",
  "outcome": "success"
}
```

**Output:**
```json
{
  "continue": true
}
```

**Performance Requirements:**
- Execution time: <3 seconds
- Async processing
- Minimal I/O

**Implementation:**
1. Copy subagent transcript to archive
2. Generate metadata (task description, outcome, etc.)
3. Update subagent index
4. Link to parent session

---

## 5. Settings Configuration

### Updated `.claude/settings.json`

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",

  "hooks": {
    "SessionStart": [
      {
        "type": "command",
        "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/session-start"
      }
    ],

    "UserPromptSubmit": [
      {
        "type": "command",
        "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/user-prompt-submit"
      }
    ],

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
  },

  "permissions": {
    "allow": [
      "Read(**/*)",
      "Write(**/*)",
      "Edit(**/*)",
      "Bash"
    ],
    "deny": [
      "Read(.env*)",
      "Read(secrets/**)",
      "Read(**/*.key)",
      "Read(**/*.pem)",
      "Bash(rm -rf /)",
      "Bash(git push --force)"
    ]
  },

  "agents": {
    "orchestrator": {
      "model": "claude-sonnet-4-5",
      "tools": ["Task", "TodoWrite", "Read", "Write", "Edit", "Grep", "Glob", "Bash"],
      "max_context": 200000
    },
    "architect": {
      "model": "claude-sonnet-4-5",
      "tools": ["Read", "Grep", "Glob", "WebSearch"],
      "max_context": 100000
    },
    "engineer": {
      "model": "claude-sonnet-4-5",
      "tools": ["Read", "Write", "Edit", "Bash", "Grep", "Glob"],
      "max_context": 150000
    },
    "tester": {
      "model": "claude-sonnet-4-5",
      "tools": ["Bash", "Read", "Write", "Edit", "Grep"],
      "max_context": 100000
    },
    "reviewer": {
      "model": "claude-sonnet-4-5",
      "tools": ["Read", "Grep", "Glob", "Edit"],
      "max_context": 100000
    }
  },

  "logging": {
    "skill_tracking": {
      "enabled": true,
      "max_invocations_per_skill": 100,
      "batch_size": 10
    },
    "conversation_archiving": {
      "enabled": true,
      "retention_months": 6,
      "sanitize_sensitive_data": true,
      "compress_old_archives": true
    }
  }
}
```

---

## 6. Error Handling Strategy

### Principles

1. **Never Crash Claude Code**: All hooks return exit code 0
2. **Fail Gracefully**: Degraded operation on errors
3. **Silent Failures**: Log errors, don't show to user
4. **Recovery**: Auto-recover on next invocation

### Error Categories

| Error Type | Strategy | Example |
|------------|----------|---------|
| **File Lock** | Retry 3x with backoff | Concurrent writes |
| **Disk Full** | Log warning, skip write | Archive storage full |
| **Permission** | Log error, continue | Can't write to directory |
| **Timeout** | Abort operation, log | Slow I/O |
| **Invalid JSON** | Use defaults, log | Corrupted state file |
| **Missing File** | Create new, log | First run |

### Error Logging

**File:** `.claude-state/logs/hook-errors.log`

```
[2025-01-10T14:30:00Z] [post-tool-use] [WARNING] File lock timeout after 3 retries
[2025-01-10T14:30:05Z] [stop] [ERROR] Failed to copy transcript: Permission denied
[2025-01-10T14:30:10Z] [subagent-stop] [INFO] Recovered from previous error
```

### Error Response Template

```python
try:
    # Hook logic
    result = perform_operation()

    response = {
        "continue": True,
        "suppressOutput": True
    }

except Exception as e:
    # Log error silently
    log_error(f"Hook failed: {str(e)}")

    # Always continue
    response = {
        "continue": True,
        "suppressOutput": True
    }

print(json.dumps(response))
sys.exit(0)  # Always exit 0
```

---

## 7. Performance Optimization

### Optimization Techniques

1. **Lazy Loading**
   - Load skill-usage.json only when needed
   - Cache in memory for session duration

2. **Batch Writes**
   - Buffer skill invocations (10x batch)
   - Flush on Stop hook or timeout

3. **Async Operations**
   - Use threading for I/O operations
   - Don't block Claude Code execution

4. **Incremental Indexing**
   - Update indexes incrementally
   - Full rebuild only on corruption

5. **File Locking**
   - Use timeout-based locks (1 second max)
   - Retry with exponential backoff

6. **Compression**
   - Gzip archives older than 1 month
   - On-demand decompression

### Performance Budget

| Operation | Max Time | Strategy |
|-----------|----------|----------|
| Skill tracking | 1s | Batch + async |
| Incremental archive | 0.5s | Append-only |
| Session finalization | 5s | Copy + index |
| Subagent archive | 3s | Copy + metadata |
| Index generation | 2s | Incremental update |

### Memory Budget

| Component | Max Memory | Strategy |
|-----------|-----------|----------|
| Skill cache | 5MB | LRU eviction |
| Session buffer | 2MB | Flush on threshold |
| Index cache | 1MB | Lazy load |
| Total | <10MB | Monitor usage |

---

## 8. Security Considerations

### Sensitive Data Protection

**Sensitive Patterns to Sanitize:**
- API keys: `(api[_-]?key|apikey)\s*[:=]\s*['\"]?([a-zA-Z0-9_-]+)['\"]?`
- Passwords: `(password|passwd|pwd)\s*[:=]\s*['\"]?([^'\"\\s]+)['\"]?`
- Tokens: `(token|auth|bearer)\s*[:=]\s*['\"]?([a-zA-Z0-9._-]+)['\"]?`
- Email addresses: `[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}`
- SSH keys: `-----BEGIN (RSA|DSA|EC|OPENSSH) PRIVATE KEY-----`
- AWS keys: `AKIA[0-9A-Z]{16}`

### Sanitization Strategy

```python
def sanitize_content(content: str) -> str:
    """Remove sensitive data from content."""
    patterns = {
        'api_key': (r'(api[_-]?key|apikey)\s*[:=]\s*[\'"]?([a-zA-Z0-9_-]+)[\'"]?',
                    r'\1: ***REDACTED***'),
        'password': (r'(password|passwd|pwd)\s*[:=]\s*[\'"]?([^\'"\s]+)[\'"]?',
                     r'\1: ***REDACTED***'),
        'token': (r'(token|auth|bearer)\s*[:=]\s*[\'"]?([a-zA-Z0-9._-]+)[\'"]?',
                  r'\1: ***REDACTED***'),
        'email': (r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
                  r'***EMAIL***'),
        'ssh_key': (r'-----BEGIN (RSA|DSA|EC|OPENSSH) PRIVATE KEY-----[\s\S]+?-----END \1 PRIVATE KEY-----',
                    r'***SSH_KEY_REDACTED***'),
        'aws_key': (r'AKIA[0-9A-Z]{16}', r'***AWS_KEY***'),
    }

    sanitized = content
    for name, (pattern, replacement) in patterns.items():
        sanitized = re.sub(pattern, replacement, sanitized, flags=re.IGNORECASE)

    return sanitized
```

### Access Control

- Archive files: 0600 (owner read/write only)
- Directories: 0700 (owner access only)
- No network access from hooks
- No execution of user-provided code

### Audit Trail

**File:** `.claude-state/logs/security-audit.log`

```
[2025-01-10T14:30:00Z] [sanitizer] Redacted 3 API keys from session abc123
[2025-01-10T14:30:05Z] [archiver] Created archive with permissions 0600
[2025-01-10T14:30:10Z] [sanitizer] No sensitive data detected in session def456
```

---

## 9. Testing Strategy

### Test Levels

#### 9.1 Unit Tests

**File:** `tests/test_skill_tracker.py`

```python
import pytest
from claude.hooks.lib.skill_tracker import SkillTracker

def test_track_skill_invocation():
    tracker = SkillTracker()
    tracker.track("systematic-debugging", session_id="test123")

    usage = tracker.get_usage("systematic-debugging")
    assert usage["count"] == 1
    assert "test123" in usage["sessions"]

def test_batch_updates():
    tracker = SkillTracker(batch_size=3)

    # Should not write until batch size reached
    tracker.track("skill1", session_id="s1")
    tracker.track("skill2", session_id="s1")
    assert not tracker.is_flushed()

    # Should flush on 3rd invocation
    tracker.track("skill3", session_id="s1")
    assert tracker.is_flushed()
```

#### 9.2 Integration Tests

**File:** `tests/test_hooks_integration.py`

```python
import subprocess
import json
import tempfile
from pathlib import Path

def test_post_tool_use_hook():
    """Test PostToolUse hook with Skill tool."""
    hook_path = Path(".claude/hooks/post-tool-use")

    input_data = {
        "tool_name": "Skill",
        "tool_input": {
            "skill_name": "test-skill",
            "context": "Testing"
        },
        "session_id": "test123"
    }

    result = subprocess.run(
        [str(hook_path)],
        input=json.dumps(input_data),
        capture_output=True,
        text=True,
        timeout=5
    )

    assert result.returncode == 0
    output = json.loads(result.stdout)
    assert output["continue"] == True

    # Verify file was updated
    usage_file = Path(".claude-state/logs/skill-usage.json")
    assert usage_file.exists()

def test_conversation_archiving():
    """Test full conversation archiving workflow."""
    # Simulate session start
    # ... (submit prompts)
    # Trigger Stop hook
    # Verify archive created
    pass
```

#### 9.3 Performance Tests

**File:** `tests/test_performance.py`

```python
import time
import json
import subprocess
from pathlib import Path

def test_hook_execution_time():
    """Ensure hooks complete within time budget."""
    hooks = {
        "post-tool-use": 1.0,  # 1 second max
        "user-prompt-submit": 0.5,  # 0.5 seconds max
        "stop": 5.0,  # 5 seconds max
        "subagent-stop": 3.0,  # 3 seconds max
    }

    for hook_name, max_time in hooks.items():
        hook_path = Path(f".claude/hooks/{hook_name}")

        start = time.time()
        result = subprocess.run(
            [str(hook_path)],
            input='{}',
            capture_output=True,
            text=True,
            timeout=max_time + 1
        )
        duration = time.time() - start

        assert result.returncode == 0
        assert duration < max_time, f"{hook_name} took {duration}s, max {max_time}s"

def test_concurrent_writes():
    """Test file locking under concurrent writes."""
    # Spawn multiple processes writing to skill-usage.json
    # Verify no corruption
    pass
```

#### 9.4 Security Tests

**File:** `tests/test_security.py`

```python
from claude.hooks.lib.sanitizer import sanitize_content

def test_api_key_redaction():
    content = "API_KEY=sk_test_1234567890abcdef"
    sanitized = sanitize_content(content)
    assert "sk_test_1234567890abcdef" not in sanitized
    assert "***REDACTED***" in sanitized

def test_password_redaction():
    content = 'password="SuperSecret123"'
    sanitized = sanitize_content(content)
    assert "SuperSecret123" not in sanitized

def test_email_redaction():
    content = "Contact: user@example.com for support"
    sanitized = sanitize_content(content)
    assert "user@example.com" not in sanitized
    assert "***EMAIL***" in sanitized
```

### Test Execution

```bash
# Run all tests
pytest tests/ -v

# Run specific test category
pytest tests/test_performance.py -v

# Run with coverage
pytest tests/ --cov=.claude/hooks --cov-report=html

# Run integration tests only
pytest tests/test_hooks_integration.py -v -m integration
```

### Manual Testing

**File:** `tests/manual/test-hooks-manually.sh`

```bash
#!/bin/bash
# Manual hook testing script

PROJECT_DIR="$(pwd)"
export CLAUDE_PROJECT_DIR="$PROJECT_DIR"

echo "Testing PostToolUse hook (skill tracking)..."
echo '{
  "tool_name": "Skill",
  "tool_input": {
    "skill_name": "systematic-debugging",
    "context": "Manual test"
  },
  "session_id": "manual-test"
}' | .claude/hooks/post-tool-use | jq .

echo ""
echo "Testing UserPromptSubmit hook..."
echo '{
  "userInput": "Test prompt",
  "session_id": "manual-test"
}' | .claude/hooks/user-prompt-submit | jq .

echo ""
echo "Testing Stop hook..."
echo '{
  "session_id": "manual-test"
}' | .claude/hooks/stop | jq .

echo ""
echo "Checking skill-usage.json..."
cat .claude-state/logs/skill-usage.json | jq .skills

echo ""
echo "All manual tests complete!"
```

---

## 10. Implementation Plan

### Phase 1: Foundation (Week 1)

**Tasks:**
1. Create directory structure
2. Implement shared utilities (`lib/common.py`)
3. Create data schema validators
4. Set up error logging infrastructure

**Deliverables:**
- `.claude-state/logs/` directory structure
- `.claude/hooks/lib/common.py`
- `.claude/hooks/lib/sanitizer.py`
- Test suite foundation

### Phase 2: Skill Tracking (Week 1)

**Tasks:**
1. Implement `SkillTracker` class
2. Create `post-tool-use` hook
3. Implement batching and caching
4. Add index generation

**Deliverables:**
- `.claude/hooks/lib/skill_tracker.py`
- `.claude/hooks/post-tool-use`
- Unit tests for skill tracking
- Documentation

### Phase 3: Conversation Archiving (Week 2)

**Tasks:**
1. Implement `ConversationArchiver` class
2. Update `user-prompt-submit` hook
3. Update `stop` hook
4. Implement metadata generation

**Deliverables:**
- `.claude/hooks/lib/conversation_archiver.py`
- Updated hooks
- Archive index generation
- Integration tests

### Phase 4: Subagent Archiving (Week 2)

**Tasks:**
1. Implement subagent archiver
2. Create `subagent-stop` hook
3. Link subagent logs to parent sessions
4. Update global index

**Deliverables:**
- `.claude/hooks/subagent-stop`
- Subagent archive structure
- Parent-child linking
- Tests

### Phase 5: Optimization & Security (Week 3)

**Tasks:**
1. Performance profiling and optimization
2. Implement sanitization for sensitive data
3. Add compression for old archives
4. Security audit

**Deliverables:**
- Performance benchmarks
- Security tests
- Compression implementation
- Security audit report

### Phase 6: Documentation & Testing (Week 3)

**Tasks:**
1. Complete test coverage (>90%)
2. Write user documentation
3. Create troubleshooting guide
4. Performance testing

**Deliverables:**
- Full test suite
- User guide
- Troubleshooting docs
- Performance report

---

## Appendix A: Shared Utilities

### common.py

```python
"""Shared utilities for hook system."""

import json
import fcntl
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
from contextlib import contextmanager

# Configuration
LOGS_DIR = Path('.claude-state/logs')
ERROR_LOG = LOGS_DIR / 'hook-errors.log'

class HookError(Exception):
    """Base exception for hook errors."""
    pass

@contextmanager
def file_lock(file_path: Path, timeout: float = 1.0):
    """
    Context manager for file locking with timeout.

    Args:
        file_path: Path to file to lock
        timeout: Maximum time to wait for lock (seconds)

    Yields:
        File handle with exclusive lock

    Raises:
        HookError: If lock cannot be acquired
    """
    file_path.parent.mkdir(parents=True, exist_ok=True)

    lock_acquired = False
    start_time = time.time()

    with open(file_path, 'a+') as f:
        while time.time() - start_time < timeout:
            try:
                fcntl.flock(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                lock_acquired = True
                f.seek(0)
                yield f
                break
            except IOError:
                time.sleep(0.1)

        if lock_acquired:
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)
        else:
            raise HookError(f"Could not acquire lock on {file_path} within {timeout}s")

def log_error(message: str, level: str = "ERROR"):
    """
    Log error to hook error log.

    Args:
        message: Error message
        level: Log level (ERROR, WARNING, INFO)
    """
    try:
        ERROR_LOG.parent.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] [{level}] {message}\n"

        with open(ERROR_LOG, 'a') as f:
            f.write(log_entry)
    except Exception:
        # Can't log errors about logging - fail silently
        pass

def load_json(file_path: Path, default: Any = None) -> Any:
    """
    Safely load JSON file with fallback.

    Args:
        file_path: Path to JSON file
        default: Default value if file doesn't exist or is invalid

    Returns:
        Parsed JSON data or default
    """
    try:
        if not file_path.exists():
            return default

        with open(file_path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        log_error(f"Invalid JSON in {file_path}: {e}", level="WARNING")
        return default
    except Exception as e:
        log_error(f"Error loading {file_path}: {e}", level="ERROR")
        return default

def save_json(file_path: Path, data: Any, indent: int = 2):
    """
    Safely save JSON file with atomic write.

    Args:
        file_path: Path to JSON file
        data: Data to serialize
        indent: JSON indentation
    """
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Atomic write: write to temp file, then rename
        temp_path = file_path.with_suffix('.tmp')
        with open(temp_path, 'w') as f:
            json.dump(data, f, indent=indent)

        temp_path.replace(file_path)

    except Exception as e:
        log_error(f"Error saving {file_path}: {e}", level="ERROR")
        raise HookError(f"Could not save {file_path}")

def get_session_id(hook_input: Dict[str, Any]) -> str:
    """
    Extract session ID from hook input.

    Args:
        hook_input: Hook input data

    Returns:
        Session ID or 'unknown'
    """
    return hook_input.get('session_id') or hook_input.get('sessionId', 'unknown')

def format_timestamp(dt: Optional[datetime] = None) -> str:
    """
    Format timestamp for filenames.

    Args:
        dt: Datetime to format (default: now)

    Returns:
        Formatted timestamp (YYYY-MM-DD_HH-MM-SS)
    """
    if dt is None:
        dt = datetime.now()
    return dt.strftime('%Y-%m-%d_%H-%M-%S')

def get_month_dir(dt: Optional[datetime] = None) -> str:
    """
    Get month directory name.

    Args:
        dt: Datetime to format (default: now)

    Returns:
        Month directory (YYYY-MM)
    """
    if dt is None:
        dt = datetime.now()
    return dt.strftime('%Y-%m')
```

---

## Appendix B: File Permissions

All files and directories MUST have the following permissions:

```bash
# Directories
chmod 700 .claude-state/
chmod 700 .claude-state/logs/
chmod 700 .claude-state/logs/main-session/
chmod 700 .claude-state/logs/subagent/

# Archive files
chmod 600 .claude-state/logs/**/*.jsonl
chmod 600 .claude-state/logs/**/*.meta.json

# Index files
chmod 600 .claude-state/logs/skill-usage.json
chmod 600 .claude-state/logs/*-index.json

# Hook scripts
chmod 700 .claude/hooks/*

# Library files
chmod 600 .claude/hooks/lib/*.py
```

---

## Appendix C: Monitoring & Maintenance

### Health Check Script

**File:** `scripts/check-hook-health.py`

```python
#!/usr/bin/env python3
"""Health check for hook system."""

from pathlib import Path
import json

def check_health():
    """Run health checks on hook system."""
    checks = {
        "directories": check_directories(),
        "skill_usage": check_skill_usage(),
        "archives": check_archives(),
        "indexes": check_indexes(),
        "permissions": check_permissions(),
    }

    all_passed = all(checks.values())

    if all_passed:
        print("✓ All health checks passed")
        return 0
    else:
        print("✗ Some health checks failed")
        for check, passed in checks.items():
            status = "✓" if passed else "✗"
            print(f"  {status} {check}")
        return 1

# Implementation of check functions...
```

### Cleanup Script

**File:** `scripts/cleanup-archives.py`

```python
#!/usr/bin/env python3
"""Cleanup old archives based on retention policy."""

from pathlib import Path
from datetime import datetime, timedelta
import json

RETENTION_MONTHS = 6

def cleanup_old_archives():
    """Remove archives older than retention period."""
    cutoff_date = datetime.now() - timedelta(days=RETENTION_MONTHS * 30)

    logs_dir = Path('.claude-state/logs')

    for archive_dir in [logs_dir / 'main-session', logs_dir / 'subagent']:
        for month_dir in archive_dir.glob('*/*'):
            # Parse YYYY-MM
            try:
                year, month = map(int, month_dir.name.split('-'))
                month_date = datetime(year, month, 1)

                if month_date < cutoff_date:
                    print(f"Removing old archive: {month_dir}")
                    # Archive to compressed storage or delete
                    compress_and_archive(month_dir)

            except (ValueError, IndexError):
                continue

# Implementation...
```

---

## Document Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-01-10 | Initial design document |

---

**Status:** Ready for Engineer Implementation

**Next Steps:**
1. Review design with user
2. Create implementation tickets
3. Begin Phase 1 development
4. Set up CI/CD for testing

**Questions for User:**
1. Retention period preference (6 months OK?)
2. Compression preference (gzip vs bzip2)?
3. Priority for sanitization patterns?
4. Any specific skills to track differently?

---

**Document End**
