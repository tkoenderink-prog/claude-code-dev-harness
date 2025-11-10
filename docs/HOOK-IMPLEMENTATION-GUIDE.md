# Hook System Implementation Guide

**Quick Reference for Engineer**

This is a condensed implementation guide. See `HOOK-SYSTEM-ARCHITECTURE.md` for complete specifications.

---

## Implementation Order

### Phase 1: Foundation (Day 1-2)

1. **Create directory structure:**
```bash
mkdir -p .claude-state/logs/{main-session,subagent/{architect,engineer,tester,reviewer,orchestrator}}
mkdir -p .claude/hooks/lib
touch .claude-state/logs/skill-usage.json
touch .claude-state/logs/hook-errors.log
```

2. **Create `lib/common.py`** - See Appendix A in architecture doc
   - `file_lock()` context manager
   - `log_error()` function
   - `load_json()` / `save_json()` utilities
   - `get_session_id()` helper

3. **Create `lib/sanitizer.py`:**
```python
import re

SENSITIVE_PATTERNS = {
    'api_key': r'(api[_-]?key|apikey)\s*[:=]\s*[\'"]?([a-zA-Z0-9_-]+)[\'"]?',
    'password': r'(password|passwd|pwd)\s*[:=]\s*[\'"]?([^\'"\\s]+)[\'"]?',
    'token': r'(token|auth|bearer)\s*[:=]\s*[\'"]?([a-zA-Z0-9._-]+)[\'"]?',
    'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
    'ssh_key': r'-----BEGIN (RSA|DSA|EC|OPENSSH) PRIVATE KEY-----[\s\S]+?-----END \1 PRIVATE KEY-----',
    'aws_key': r'AKIA[0-9A-Z]{16}',
}

def sanitize_content(content: str) -> str:
    """Remove sensitive data from content."""
    sanitized = content
    for name, pattern in SENSITIVE_PATTERNS.items():
        sanitized = re.sub(pattern, '***REDACTED***', sanitized, flags=re.IGNORECASE)
    return sanitized
```

### Phase 2: Skill Tracking (Day 3-4)

1. **Create `lib/skill_tracker.py`:**

```python
from pathlib import Path
from datetime import datetime
from typing import Dict, List
import json
from .common import file_lock, log_error, load_json, save_json

SKILL_USAGE_FILE = Path('.claude-state/logs/skill-usage.json')
MAX_INVOCATIONS = 100
BATCH_SIZE = 10

class SkillTracker:
    def __init__(self):
        self.batch = []
        self.batch_size = BATCH_SIZE

    def track(self, skill_name: str, session_id: str, context: str = "", success: bool = True):
        """Track a skill invocation."""
        invocation = {
            "timestamp": datetime.now().isoformat(),
            "session_id": session_id,
            "context": context,
            "success": success
        }

        self.batch.append((skill_name, invocation))

        if len(self.batch) >= self.batch_size:
            self.flush()

    def flush(self):
        """Flush batch to disk."""
        if not self.batch:
            return

        try:
            with file_lock(SKILL_USAGE_FILE):
                usage = load_json(SKILL_USAGE_FILE, default={
                    "schema_version": "1.0",
                    "last_updated": "",
                    "total_invocations": 0,
                    "skills": {},
                    "sessions": {},
                    "daily_stats": {}
                })

                for skill_name, invocation in self.batch:
                    self._update_usage(usage, skill_name, invocation)

                usage["last_updated"] = datetime.now().isoformat()
                save_json(SKILL_USAGE_FILE, usage)

            self.batch = []

        except Exception as e:
            log_error(f"Failed to flush skill tracking batch: {e}")

    def _update_usage(self, usage: Dict, skill_name: str, invocation: Dict):
        """Update usage data with new invocation."""
        if skill_name not in usage["skills"]:
            usage["skills"][skill_name] = {
                "count": 0,
                "first_used": invocation["timestamp"],
                "last_used": invocation["timestamp"],
                "invocations": [],
                "sessions": [],
                "success_rate": 1.0
            }

        skill = usage["skills"][skill_name]
        skill["count"] += 1
        skill["last_used"] = invocation["timestamp"]

        # Keep last MAX_INVOCATIONS invocations
        skill["invocations"].append(invocation)
        if len(skill["invocations"]) > MAX_INVOCATIONS:
            skill["invocations"] = skill["invocations"][-MAX_INVOCATIONS:]

        # Track session
        session_id = invocation["session_id"]
        if session_id not in skill["sessions"]:
            skill["sessions"].append(session_id)

        # Update total
        usage["total_invocations"] += 1

        # Update daily stats
        date = invocation["timestamp"][:10]  # YYYY-MM-DD
        if date not in usage["daily_stats"]:
            usage["daily_stats"][date] = {
                "invocations": 0,
                "unique_skills": set(),
                "sessions": set()
            }

        usage["daily_stats"][date]["invocations"] += 1
        usage["daily_stats"][date]["unique_skills"].add(skill_name)
        usage["daily_stats"][date]["sessions"].add(session_id)

        # Convert sets to lists for JSON serialization
        usage["daily_stats"][date]["unique_skills"] = list(usage["daily_stats"][date]["unique_skills"])
        usage["daily_stats"][date]["sessions"] = list(usage["daily_stats"][date]["sessions"])
```

2. **Create `.claude/hooks/post-tool-use`:**

```python
#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///

import json
import sys
import os
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent / 'lib'))

from skill_tracker import SkillTracker
from common import log_error, get_session_id

def main():
    try:
        # Read hook input
        hook_input = json.loads(sys.stdin.read())

        # Only track Skill tool
        tool_name = hook_input.get('tool_name', '')
        if tool_name != 'Skill':
            response = {"continue": True, "suppressOutput": True}
            print(json.dumps(response))
            sys.exit(0)

        # Extract skill information
        tool_input = hook_input.get('tool_input', {})
        skill_name = tool_input.get('skill_name', '')
        context = tool_input.get('context', '')
        session_id = get_session_id(hook_input)

        # Check if skill execution was successful
        tool_output = hook_input.get('tool_output', '')
        success = 'error' not in tool_output.lower()

        # Track the invocation
        tracker = SkillTracker()
        tracker.track(skill_name, session_id, context, success)
        tracker.flush()  # Force flush for now (can optimize later)

        # Always continue
        response = {"continue": True, "suppressOutput": True}
        print(json.dumps(response))
        sys.exit(0)

    except Exception as e:
        log_error(f"post-tool-use hook failed: {e}")
        response = {"continue": True, "suppressOutput": True}
        print(json.dumps(response))
        sys.exit(0)

if __name__ == "__main__":
    main()
```

3. **Make executable:**
```bash
chmod +x .claude/hooks/post-tool-use
```

### Phase 3: Conversation Archiving (Day 5-6)

1. **Create `lib/conversation_archiver.py`:**

```python
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional
import shutil
from .common import log_error, save_json, get_month_dir, format_timestamp

LOGS_DIR = Path('.claude-state/logs')

class ConversationArchiver:
    def __init__(self, archive_type: str = "main_session"):
        """
        Args:
            archive_type: "main_session" or "subagent"
        """
        self.archive_type = archive_type
        self.base_dir = LOGS_DIR / archive_type

    def archive_session(self, session_id: str, transcript_path: str, metadata: Dict):
        """
        Archive a conversation session.

        Args:
            session_id: Session identifier
            transcript_path: Path to transcript file
            metadata: Session metadata
        """
        try:
            # Create month directory
            month_dir = self.base_dir / get_month_dir()
            month_dir.mkdir(parents=True, exist_ok=True)

            # Generate filename
            timestamp = format_timestamp()
            base_name = f"{timestamp}_{session_id}"

            # Copy transcript
            transcript_src = Path(transcript_path)
            if transcript_src.exists():
                transcript_dst = month_dir / f"{base_name}.jsonl"
                shutil.copy2(transcript_src, transcript_dst)

                # Set permissions
                transcript_dst.chmod(0o600)

                # Save metadata
                meta_path = month_dir / f"{base_name}.meta.json"
                metadata.update({
                    "archive_path": str(transcript_dst.relative_to(LOGS_DIR)),
                    "archived_at": datetime.now().isoformat()
                })
                save_json(meta_path, metadata)
                meta_path.chmod(0o600)

                log_error(f"Archived session {session_id} to {transcript_dst}", level="INFO")

        except Exception as e:
            log_error(f"Failed to archive session {session_id}: {e}")

    def generate_metadata(self, session_id: str, transcript_path: str) -> Dict:
        """
        Generate metadata for a session.

        Args:
            session_id: Session identifier
            transcript_path: Path to transcript file

        Returns:
            Metadata dictionary
        """
        metadata = {
            "schema_version": "1.0",
            "session_id": session_id,
            "type": self.archive_type,
            "archived_at": datetime.now().isoformat()
        }

        # Parse transcript for additional metadata
        try:
            transcript = Path(transcript_path)
            if transcript.exists():
                # Count messages, tool calls, etc.
                with open(transcript, 'r') as f:
                    lines = f.readlines()
                    metadata["message_count"] = len(lines)
                    metadata["size_bytes"] = transcript.stat().st_size

        except Exception as e:
            log_error(f"Error generating metadata: {e}")

        return metadata
```

2. **Update `.claude/hooks/stop`:**

```python
#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///

import json
import sys
import os
from pathlib import Path
from datetime import datetime

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent / 'lib'))

from conversation_archiver import ConversationArchiver
from common import log_error, get_session_id

def main():
    try:
        hook_input = json.loads(sys.stdin.read())
        session_id = get_session_id(hook_input)

        # Get project directory
        project_dir = Path(os.environ.get('CLAUDE_PROJECT_DIR', '.')).resolve()
        state_dir = project_dir / '.claude-state'

        # Update session.yaml with end timestamp
        session_file = state_dir / 'session.yaml'
        timestamp = datetime.now().isoformat()

        if session_file.exists():
            content = session_file.read_text()
            if 'ended_at:' not in content:
                content += f"\nended_at: \"{timestamp}\"\n"
                session_file.write_text(content)

        # Archive transcript if available
        transcript_path = hook_input.get('transcript_path', '')
        if transcript_path:
            archiver = ConversationArchiver("main_session")
            metadata = archiver.generate_metadata(session_id, transcript_path)
            archiver.archive_session(session_id, transcript_path, metadata)

        # Log stop event
        stop_log = state_dir / 'last-session.json'
        stop_log.write_text(json.dumps({
            "ended_at": timestamp,
            "session_id": session_id
        }, indent=2))

        response = {"continue": True}
        print(json.dumps(response))
        sys.exit(0)

    except Exception as e:
        log_error(f"stop hook failed: {e}")
        response = {"continue": True}
        print(json.dumps(response))
        sys.exit(0)

if __name__ == "__main__":
    main()
```

### Phase 4: Subagent Archiving (Day 7)

1. **Create `.claude/hooks/subagent-stop`:**

```python
#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///

import json
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'lib'))

from conversation_archiver import ConversationArchiver
from common import log_error

def main():
    try:
        hook_input = json.loads(sys.stdin.read())

        task_id = hook_input.get('task_id', 'unknown')
        agent_type = hook_input.get('agent_type', 'unknown')
        parent_session_id = hook_input.get('parent_session_id', 'unknown')
        transcript_path = hook_input.get('transcript_path', '')
        outcome = hook_input.get('outcome', 'unknown')

        # Archive subagent conversation
        if transcript_path:
            archiver = ConversationArchiver(f"subagent/{agent_type}")

            metadata = {
                "task_id": task_id,
                "agent_type": agent_type,
                "parent_session_id": parent_session_id,
                "outcome": outcome
            }

            metadata.update(archiver.generate_metadata(task_id, transcript_path))
            archiver.archive_session(task_id, transcript_path, metadata)

        response = {"continue": True}
        print(json.dumps(response))
        sys.exit(0)

    except Exception as e:
        log_error(f"subagent-stop hook failed: {e}")
        response = {"continue": True}
        print(json.dumps(response))
        sys.exit(0)

if __name__ == "__main__":
    main()
```

2. **Make executable:**
```bash
chmod +x .claude/hooks/subagent-stop
```

### Phase 5: Update Settings (Day 8)

Update `.claude/settings.json` to add new hooks:

```json
{
  "hooks": {
    "SessionStart": [...],
    "UserPromptSubmit": [...],
    "PostToolUse": [
      {
        "matcher": "Skill",
        "type": "command",
        "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/post-tool-use"
      }
    ],
    "Stop": [...],
    "SubagentStop": [
      {
        "type": "command",
        "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/subagent-stop"
      }
    ]
  }
}
```

---

## Testing Checklist

```bash
# Test post-tool-use hook
echo '{
  "tool_name": "Skill",
  "tool_input": {"skill_name": "test-skill"},
  "session_id": "test123"
}' | .claude/hooks/post-tool-use | jq

# Verify skill-usage.json was created
cat .claude-state/logs/skill-usage.json | jq

# Test stop hook with transcript
echo '{
  "session_id": "test456",
  "transcript_path": "/path/to/transcript.jsonl"
}' | .claude/hooks/stop | jq

# Test subagent-stop hook
echo '{
  "task_id": "task-xyz",
  "agent_type": "architect",
  "parent_session_id": "test456",
  "transcript_path": "/path/to/subagent.jsonl"
}' | .claude/hooks/subagent-stop | jq

# Check error log
cat .claude-state/logs/hook-errors.log
```

---

## Performance Checklist

- [ ] File locking timeout set to 1 second
- [ ] Skill tracking batches at 10 invocations
- [ ] All hooks exit in <5 seconds
- [ ] No blocking I/O operations
- [ ] Error logs don't grow unbounded
- [ ] Archive files have correct permissions (0600)

---

## Security Checklist

- [ ] Sanitizer removes API keys
- [ ] Sanitizer removes passwords
- [ ] Sanitizer removes tokens
- [ ] Sanitizer removes email addresses
- [ ] All archive files chmod 0600
- [ ] All log directories chmod 0700
- [ ] No sensitive data in error logs

---

## Common Issues

### Issue: "Permission denied" on hook execution

**Solution:**
```bash
chmod +x .claude/hooks/post-tool-use
chmod +x .claude/hooks/subagent-stop
```

### Issue: "Module not found: skill_tracker"

**Solution:**
```bash
# Ensure lib directory exists
mkdir -p .claude/hooks/lib
touch .claude/hooks/lib/__init__.py
```

### Issue: File lock timeout

**Solution:**
- Check for zombie processes holding locks
- Increase timeout in `file_lock()` function
- Clear stale lock files

### Issue: Skill tracking not working

**Debug:**
```bash
# Check hook is configured
cat .claude/settings.json | jq .hooks.PostToolUse

# Test hook manually
echo '{"tool_name":"Skill","tool_input":{"skill_name":"test"}}' | \
  .claude/hooks/post-tool-use | jq

# Check error log
tail -f .claude-state/logs/hook-errors.log
```

---

## Next Steps After Implementation

1. Run full test suite
2. Performance profiling
3. Security audit
4. Write user documentation
5. Create migration guide for existing users

---

**Implementation Time Estimate:** 8 days
**Priority:** High
**Dependencies:** None
