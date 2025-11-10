# Hook System Architecture - Visual Diagrams

## 1. System Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                         Claude Code                               │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐ │
│  │   Main     │  │ Subagent:  │  │ Subagent:  │  │ Subagent:  │ │
│  │  Session   │  │ Architect  │  │ Engineer   │  │  Tester    │ │
│  └──────┬─────┘  └──────┬─────┘  └──────┬─────┘  └──────┬─────┘ │
│         │               │                │                │        │
└─────────┼───────────────┼────────────────┼────────────────┼────────┘
          │               │                │                │
          │ SessionStart  │ SubagentStop   │ SubagentStop   │ SubagentStop
          │ UserPrompt    │                │                │
          │ PostToolUse   │                │                │
          │ Stop          │                │                │
          │               │                │                │
          ▼               ▼                ▼                ▼
┌─────────────────────────────────────────────────────────────────┐
│                          Hook Layer                              │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ session-     │  │ post-tool-   │  │ subagent-    │          │
│  │ start        │  │ use          │  │ stop         │          │
│  │              │  │              │  │              │          │
│  │ • Load state │  │ • Track Skill│  │ • Archive    │          │
│  │ • Inject ctx │  │   invocations│  │   subagent   │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐                            │
│  │ user-prompt- │  │ stop         │                            │
│  │ submit       │  │              │                            │
│  │              │  │ • Archive    │                            │
│  │ • Inject ctx │  │   main       │                            │
│  │ • Log prompt │  │   session    │                            │
│  └──────────────┘  └──────────────┘                            │
└─────────────────────────────────────────────────────────────────┘
          │               │                │                │
          ▼               ▼                ▼                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Library Layer                               │
├─────────────────────────────────────────────────────────────────┤
│  ┌───────────────────┐  ┌───────────────────┐                  │
│  │ skill_tracker.py  │  │ conversation_     │                  │
│  │                   │  │ archiver.py       │                  │
│  │ • Batch writes    │  │                   │                  │
│  │ • Usage stats     │  │ • Copy transcripts│                  │
│  │ • Index generation│  │ • Generate metadata                  │
│  └───────────────────┘  └───────────────────┘                  │
│                                                                  │
│  ┌───────────────────┐  ┌───────────────────┐                  │
│  │ sanitizer.py      │  │ common.py         │                  │
│  │                   │  │                   │                  │
│  │ • Remove API keys │  │ • File locking    │                  │
│  │ • Remove passwords│  │ • Error logging   │                  │
│  │ • Remove tokens   │  │ • JSON I/O        │                  │
│  └───────────────────┘  └───────────────────┘                  │
└─────────────────────────────────────────────────────────────────┘
          │               │                │                │
          ▼               ▼                ▼                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Storage Layer                               │
├─────────────────────────────────────────────────────────────────┤
│  .claude-state/logs/                                             │
│  ├── skill-usage.json           ← Aggregate skill tracking      │
│  ├── skill-usage-index.json     ← Search index                  │
│  ├── archive-index.json         ← Global archive index          │
│  ├── hook-errors.log            ← Error logging                 │
│  │                                                               │
│  ├── main-session/                                              │
│  │   ├── 2025-01/                                               │
│  │   │   ├── 2025-01-10_14-30-00_abc123.jsonl                  │
│  │   │   └── 2025-01-10_14-30-00_abc123.meta.json              │
│  │   └── 2025-02/ ...                                           │
│  │                                                               │
│  └── subagent/                                                  │
│      ├── architect/2025-01/ ...                                 │
│      ├── engineer/2025-01/ ...                                  │
│      ├── tester/2025-01/ ...                                    │
│      └── reviewer/2025-01/ ...                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Skill Tracking Flow

```
┌─────────────────────────────────────────────────────────────────┐
│ User: "Use systematic-debugging skill to fix auth bug"          │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│ Claude executes: Skill(systematic-debugging)                     │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                │ PostToolUse event fired
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│ PostToolUse Hook (.claude/hooks/post-tool-use)                   │
│                                                                  │
│ 1. Read input:                                                   │
│    {                                                             │
│      "tool_name": "Skill",                                       │
│      "tool_input": {                                             │
│        "skill_name": "systematic-debugging",                     │
│        "context": "Fix auth bug"                                 │
│      },                                                          │
│      "session_id": "abc123"                                      │
│    }                                                             │
│                                                                  │
│ 2. Filter: tool_name == "Skill"? ✓                              │
│                                                                  │
│ 3. Create SkillTracker instance                                 │
│                                                                  │
│ 4. Call tracker.track():                                         │
│    - skill_name: "systematic-debugging"                          │
│    - session_id: "abc123"                                        │
│    - context: "Fix auth bug"                                     │
│    - success: true                                               │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│ SkillTracker (lib/skill_tracker.py)                             │
│                                                                  │
│ 1. Add to batch buffer:                                          │
│    batch = [("systematic-debugging", invocation_data)]           │
│                                                                  │
│ 2. Check batch size:                                             │
│    if len(batch) >= 10:                                          │
│        flush()                                                   │
│                                                                  │
│ 3. If flushing:                                                  │
│    a. Acquire file lock (1s timeout)                             │
│    b. Load skill-usage.json                                      │
│    c. Update skill entry:                                        │
│       - Increment count                                          │
│       - Append invocation (keep last 100)                        │
│       - Update sessions list                                     │
│       - Update daily stats                                       │
│    d. Save skill-usage.json                                      │
│    e. Release lock                                               │
│    f. Clear batch                                                │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│ skill-usage.json (.claude-state/logs/)                           │
│                                                                  │
│ {                                                                │
│   "skills": {                                                    │
│     "systematic-debugging": {                                    │
│       "count": 42,                                               │
│       "last_used": "2025-01-10T14:30:00Z",                       │
│       "invocations": [                                           │
│         {                                                        │
│           "timestamp": "2025-01-10T14:30:00Z",                   │
│           "session_id": "abc123",                                │
│           "context": "Fix auth bug",                             │
│           "success": true                                        │
│         }                                                        │
│       ],                                                         │
│       "sessions": ["abc123", ...],                               │
│       "success_rate": 0.95                                       │
│     }                                                            │
│   }                                                              │
│ }                                                                │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Conversation Archiving Flow

```
┌─────────────────────────────────────────────────────────────────┐
│ Session starts: session-start hook runs                          │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│ User: "Design authentication system"                             │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                │ UserPromptSubmit event
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│ UserPromptSubmit Hook (updated)                                  │
│                                                                  │
│ 1. Log prompt (future enhancement)                               │
│ 2. Inject context if keywords match                              │
│ 3. Return {"continue": true}                                     │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│ Claude responds, uses tools, etc.                                │
│ Transcript written to: ~/.claude/projects/.../abc123.jsonl       │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                │ Stop event
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│ Stop Hook (.claude/hooks/stop)                                   │
│                                                                  │
│ 1. Read input:                                                   │
│    {                                                             │
│      "session_id": "abc123",                                     │
│      "transcript_path": "~/.claude/.../abc123.jsonl"             │
│    }                                                             │
│                                                                  │
│ 2. Update session.yaml with end timestamp                        │
│                                                                  │
│ 3. Create ConversationArchiver("main_session")                   │
│                                                                  │
│ 4. Generate metadata:                                            │
│    - Count messages in transcript                                │
│    - Calculate session duration                                  │
│    - List skills used (from skill-usage.json)                    │
│    - List files modified                                         │
│                                                                  │
│ 5. Archive session:                                              │
│    - Copy transcript to archive                                  │
│    - Save metadata                                               │
│    - Update index                                                │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│ ConversationArchiver (lib/conversation_archiver.py)             │
│                                                                  │
│ 1. Determine month directory:                                    │
│    month_dir = .claude-state/logs/main-session/2025-01/          │
│                                                                  │
│ 2. Generate filename:                                            │
│    base = "2025-01-10_14-30-00_abc123"                           │
│                                                                  │
│ 3. Copy transcript:                                              │
│    src: ~/.claude/projects/.../abc123.jsonl                      │
│    dst: .../main-session/2025-01/2025-01-10_14-30-00_abc123.jsonl│
│                                                                  │
│ 4. Set permissions: chmod 0600                                   │
│                                                                  │
│ 5. Save metadata:                                                │
│    .../2025-01-10_14-30-00_abc123.meta.json                      │
│                                                                  │
│ 6. Update global index:                                          │
│    .claude-state/logs/archive-index.json                         │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. Subagent Archiving Flow

```
┌─────────────────────────────────────────────────────────────────┐
│ Main Session (orchestrator)                                      │
│                                                                  │
│ User: "Design authentication API"                                │
│                                                                  │
│ Claude: Task(architect, "Design authentication API endpoints")   │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                │ Task starts subagent
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│ Subagent Session (architect)                                     │
│                                                                  │
│ - Analyzes requirements                                          │
│ - Designs API endpoints                                          │
│ - Creates data models                                            │
│ - Returns deliverables                                           │
│                                                                  │
│ Transcript: ~/.claude/tasks/task-xyz.jsonl                       │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                │ SubagentStop event
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│ SubagentStop Hook (.claude/hooks/subagent-stop)                  │
│                                                                  │
│ 1. Read input:                                                   │
│    {                                                             │
│      "task_id": "task-xyz",                                      │
│      "agent_type": "architect",                                  │
│      "parent_session_id": "abc123",                              │
│      "transcript_path": "~/.claude/tasks/task-xyz.jsonl",        │
│      "outcome": "success"                                        │
│    }                                                             │
│                                                                  │
│ 2. Create ConversationArchiver("subagent/architect")             │
│                                                                  │
│ 3. Generate metadata:                                            │
│    - task_id, agent_type, parent_session_id                      │
│    - Message count, duration                                     │
│    - Outcome, deliverables                                       │
│                                                                  │
│ 4. Archive subagent session                                      │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│ Archive Structure                                                │
│                                                                  │
│ .claude-state/logs/subagent/architect/2025-01/                   │
│ ├── 2025-01-10_14-35-00_task-xyz.jsonl                           │
│ └── 2025-01-10_14-35-00_task-xyz.meta.json                       │
│                                                                  │
│ Metadata:                                                        │
│ {                                                                │
│   "task_id": "task-xyz",                                         │
│   "agent_type": "architect",                                     │
│   "parent_session_id": "abc123",  ← Link to main session         │
│   "outcome": "success",                                          │
│   "message_count": 12,                                           │
│   "duration_seconds": 420                                        │
│ }                                                                │
└─────────────────────────────────────────────────────────────────┘
```

---

## 5. File Locking Mechanism

```
┌─────────────────────────────────────────────────────────────────┐
│ Hook A wants to write skill-usage.json                           │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│ with file_lock(skill-usage.json, timeout=1.0):                   │
│                                                                  │
│     Try to acquire exclusive lock (fcntl.LOCK_EX)                │
│                                                                  │
│     ┌─────────────────────────────────────────────────┐         │
│     │ Is lock available?                              │         │
│     └───────────┬──────────────────────┬──────────────┘         │
│                 │                      │                        │
│           YES   ▼                NO    ▼                        │
│     ┌───────────────────┐  ┌───────────────────┐               │
│     │ Acquire lock      │  │ Wait 100ms        │               │
│     │ immediately       │  │ Retry...          │               │
│     └─────────┬─────────┘  └─────────┬─────────┘               │
│               │                      │                          │
│               │                      │ Timeout after 1s?        │
│               │                      │                          │
│               │                YES   ▼                          │
│               │            ┌────────────────────┐               │
│               │            │ Raise HookError    │               │
│               │            └────────────────────┘               │
│               │                                                  │
│               ▼                                                  │
│     ┌─────────────────────────────────────────────────┐         │
│     │ Lock acquired!                                  │         │
│     │                                                 │         │
│     │ Read file → Modify → Write → Release lock      │         │
│     └─────────────────────────────────────────────────┘         │
└─────────────────────────────────────────────────────────────────┘

Timeline view:

Hook A          Hook B          Hook C
  |               |               |
  | Try lock      |               |
  | ✓ Acquired    |               |
  |               |               |
  | Reading...    | Try lock      |
  |               | ⏳ Waiting... | Try lock
  |               |               | ⏳ Waiting...
  | Modifying...  |               |
  |               |               |
  | Writing...    |               |
  |               |               |
  | ✓ Release     |               |
  |               | ✓ Acquired    |
  |               |               | ⏳ Still waiting...
  |               | Reading...    |
  |               | Modifying...  |
  |               | ✓ Release     |
  |               |               | ✓ Acquired
  |               |               | Reading...
  |               |               | ✓ Release
  ▼               ▼               ▼
```

---

## 6. Error Handling Flow

```
┌─────────────────────────────────────────────────────────────────┐
│ Hook execution starts                                            │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│ try:                                                             │
│     # Hook logic                                                 │
│     result = perform_operation()                                 │
│                                                                  │
│     ┌───────────────────────────────────────┐                   │
│     │ Success?                              │                   │
│     └───────────┬──────────────┬────────────┘                   │
│                 │              │                                 │
│           YES   ▼        NO    ▼                                 │
│     ┌───────────────┐  ┌──────────────────────┐                 │
│     │ Return        │  │ Exception raised     │                 │
│     │ success JSON  │  │ Go to except block   │                 │
│     └───────┬───────┘  └──────────┬───────────┘                 │
│             │                     │                              │
│             │                     ▼                              │
│             │         ┌───────────────────────────────┐          │
│             │         │ except Exception as e:        │          │
│             │         │                               │          │
│             │         │   Classify error:             │          │
│             │         │   ├─ File lock? → Log warning│          │
│             │         │   ├─ Disk full? → Log error  │          │
│             │         │   ├─ Permission? → Log error │          │
│             │         │   └─ Other? → Log error      │          │
│             │         │                               │          │
│             │         │   Write to hook-errors.log   │          │
│             │         │                               │          │
│             │         │   Return success JSON anyway │          │
│             │         └───────────┬───────────────────┘          │
│             │                     │                              │
│             ▼                     ▼                              │
│     ┌─────────────────────────────────────────┐                 │
│     │ print(json.dumps({"continue": true}))   │                 │
│     │ sys.exit(0)  ← ALWAYS EXIT 0            │                 │
│     └─────────────────────────────────────────┘                 │
└─────────────────────────────────────────────────────────────────┘

Error Log Format:

[2025-01-10T14:30:00Z] [post-tool-use] [ERROR] File lock timeout
[2025-01-10T14:30:05Z] [stop] [WARNING] Transcript not found
[2025-01-10T14:30:10Z] [subagent-stop] [INFO] Recovered successfully

Result: Claude Code continues execution without interruption
```

---

## 7. Data Flow Summary

```
┌───────────────┐
│     User      │
│   Prompts     │
└───────┬───────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Claude Code                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │SessionStart │  │PostToolUse  │  │     Stop    │             │
│  │   Hook      │  │   Hook      │  │    Hook     │             │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘             │
└─────────┼─────────────────┼─────────────────┼────────────────────┘
          │                 │                 │
          │                 │                 │
          ▼                 ▼                 ▼
  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
  │ Load State   │  │ Track Skills │  │Archive Session│
  │ Inject Ctx   │  │              │  │ Generate Meta │
  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘
         │                 │                  │
         │                 ▼                  │
         │         ┌──────────────┐           │
         │         │skill-usage   │           │
         │         │    .json     │           │
         │         └──────────────┘           │
         │                                    │
         ▼                                    ▼
┌──────────────┐                    ┌──────────────┐
│ State Files  │                    │   Archive    │
│  session.yaml│                    │   Files      │
│  preferences │                    │   .jsonl     │
│  progress    │                    │   .meta.json │
└──────────────┘                    └──────────────┘
         │                                    │
         │                                    │
         └──────────────┬─────────────────────┘
                        │
                        ▼
                ┌──────────────┐
                │   Indexes    │
                │              │
                │ skill-usage- │
                │  index.json  │
                │              │
                │ archive-     │
                │  index.json  │
                └──────────────┘
                        │
                        ▼
                ┌──────────────┐
                │   Search &   │
                │   Analytics  │
                └──────────────┘
```

---

## 8. Performance Optimization Layers

```
┌─────────────────────────────────────────────────────────────────┐
│ Level 1: In-Memory Caching                                       │
├─────────────────────────────────────────────────────────────────┤
│ • Skill metadata cached in SkillTracker                          │
│ • Session metadata cached during lifecycle                       │
│ • Index data cached (LRU eviction)                               │
│                                                                  │
│ Cache hit: ~1ms                                                  │
│ Cache miss: Read from Level 2                                    │
└─────────────────────────────────┬───────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│ Level 2: Batching Layer                                          │
├─────────────────────────────────────────────────────────────────┤
│ • Skill invocations batched (10x)                                │
│ • Write buffer (2MB max)                                         │
│ • Flush on threshold or timeout (30s)                            │
│                                                                  │
│ Batch write: ~100ms for 10 items                                 │
│ Individual write: ~50ms per item                                 │
│ Savings: 80% reduction in I/O                                    │
└─────────────────────────────────┬───────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│ Level 3: File Locking (Concurrency Control)                      │
├─────────────────────────────────────────────────────────────────┤
│ • Exclusive locks (fcntl.LOCK_EX)                                │
│ • Timeout: 1 second max wait                                     │
│ • Retry with exponential backoff                                 │
│                                                                  │
│ Lock acquisition: ~1ms (uncontended)                             │
│ Lock wait: up to 1000ms (contended)                              │
└─────────────────────────────────┬───────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│ Level 4: Disk Storage                                            │
├─────────────────────────────────────────────────────────────────┤
│ • JSON files with atomic writes                                  │
│ • Append-only logs for transcripts                               │
│ • Compression for old archives (gzip)                            │
│                                                                  │
│ JSON write: ~50ms (5KB file)                                     │
│ Transcript copy: ~200ms (500KB file)                             │
│ Compression: ~500ms (1MB → 100KB)                                │
└─────────────────────────────────────────────────────────────────┘

Total typical operation time:
- Skill tracking: 1ms (cached batch) to 100ms (flush)
- Session archiving: 200ms (copy) + 50ms (metadata) = 250ms
- Index generation: 50ms (incremental update)
```

---

## 9. Security Layers

```
┌─────────────────────────────────────────────────────────────────┐
│ Layer 1: Input Validation                                        │
├─────────────────────────────────────────────────────────────────┤
│ • Validate JSON structure                                        │
│ • Sanitize file paths (no ../.. attacks)                         │
│ • Check session ID format                                        │
│ • Validate tool names                                            │
└─────────────────────────────────┬───────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│ Layer 2: Content Sanitization                                    │
├─────────────────────────────────────────────────────────────────┤
│ Sensitive pattern detection:                                     │
│ • API keys:      "api_key=sk_test_..." → "***REDACTED***"      │
│ • Passwords:     "password=secret123" → "***REDACTED***"        │
│ • Tokens:        "bearer eyJ..." → "***REDACTED***"             │
│ • Emails:        "user@example.com" → "***EMAIL***"             │
│ • SSH keys:      "-----BEGIN RSA..." → "***SSH_KEY***"          │
│ • AWS keys:      "AKIA..." → "***AWS_KEY***"                    │
└─────────────────────────────────┬───────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│ Layer 3: File Permissions                                        │
├─────────────────────────────────────────────────────────────────┤
│ Directories: 0700 (owner only, rwx------)                        │
│   .claude-state/logs/                                            │
│   .claude-state/logs/main-session/                               │
│   .claude-state/logs/subagent/                                   │
│                                                                  │
│ Data files: 0600 (owner only, rw-------)                         │
│   skill-usage.json                                               │
│   *.jsonl (transcripts)                                          │
│   *.meta.json (metadata)                                         │
│   *-index.json (indexes)                                         │
│                                                                  │
│ Hook scripts: 0700 (owner only, executable)                      │
│   post-tool-use                                                  │
│   subagent-stop                                                  │
│   stop                                                           │
└─────────────────────────────────┬───────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│ Layer 4: Audit Logging                                           │
├─────────────────────────────────────────────────────────────────┤
│ security-audit.log:                                              │
│ [2025-01-10T14:30:00Z] Redacted 3 API keys from session abc123  │
│ [2025-01-10T14:30:05Z] Created archive with permissions 0600    │
│ [2025-01-10T14:30:10Z] No sensitive data in session def456      │
│                                                                  │
│ Retention: 90 days                                               │
│ Rotation: Daily                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

**End of Diagrams**
