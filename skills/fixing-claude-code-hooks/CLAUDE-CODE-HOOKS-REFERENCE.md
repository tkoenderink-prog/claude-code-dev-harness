# Claude Code Hooks - Complete Reference Manual

## Table of Contents
1. [Hook Types & Events](#hook-types--events)
2. [Configuration Patterns](#configuration-patterns)
3. [Input/Output Specifications](#inputoutput-specifications)
4. [Example Implementations](#example-implementations)
5. [Testing & Debugging](#testing--debugging)
6. [Common Patterns Library](#common-patterns-library)
7. [Security Best Practices](#security-best-practices)
8. [Performance Optimization](#performance-optimization)

---

## Hook Types & Events

### Lifecycle Hooks

#### SessionStart
**Trigger:** When Claude Code session begins or resumes
**Use cases:** Load context, check version, initialize state
**Special features:** stdout added to context on exit code 0

**Input structure:**
```json
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "permission_mode": "default",
  "hook_event_name": "SessionStart",
  "source": "startup"
}
```

**Environment variables:**
- `CLAUDE_PROJECT_DIR` - Project root directory
- `CLAUDE_ENV_FILE` - File path to persist environment variables for subsequent bash commands

**Output structure:**
```json
{
  "continue": true,
  "output": "Context to inject into session"
}
```

#### SessionEnd
**Trigger:** When Claude Code session terminates
**Use cases:** Save state, cleanup, logging

#### Stop
**Trigger:** When Claude finishes responding
**Use cases:** Save conversation state, trigger notifications, cleanup

**Input structure:**
```json
{
  "session_id": "abc123",
  "hook_event_name": "Stop"
}
```

#### SubagentStop
**Trigger:** When a subagent (Task tool) finishes
**Use cases:** Collect subagent results, aggregate metrics

#### UserPromptSubmit
**Trigger:** Before user prompt is processed by Claude
**Use cases:** Validate input, inject context, log queries

**Input structure:**
```json
{
  "userInput": "The user's prompt text",
  "prompt": "The user's prompt text"
}
```

**Output structure:**
```json
{
  "continue": true,
  "output": "## Relevant Context\nInjected into prompt"
}
```

#### Notification
**Trigger:** When Claude Code shows a notification
**Use cases:** Log notifications, trigger external alerts

### Tool Hooks

#### PreToolUse
**Trigger:** Before Claude executes a tool
**Use cases:** Validation, access control, logging

**Configuration with matcher:**
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "type": "command",
        "command": "./hooks/validate-write"
      }
    ]
  }
}
```

**Input structure:**
```json
{
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file",
    "content": "file content"
  }
}
```

**Output for blocking:**
```json
{
  "permissionDecision": "deny",
  "reason": "Cannot modify .env files"
}
```

**Output for allowing:**
```json
{
  "permissionDecision": "approve"
}
```

#### PostToolUse
**Trigger:** After Claude executes a tool
**Use cases:** Code formatting, linting, post-processing

**Input structure:**
```json
{
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file",
    "content": "file content"
  },
  "tool_output": "Success message or result"
}
```

#### PreCompact
**Trigger:** Before context window is compacted
**Use cases:** Save important context, optimize compaction

---

## Configuration Patterns

### Basic Event Hook (No Matcher)

```json
{
  "hooks": {
    "SessionStart": [
      {
        "type": "command",
        "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/session-start"
      }
    ]
  }
}
```

### Tool Hook with Matcher

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write",
        "type": "command",
        "command": "./hooks/block-env-writes"
      },
      {
        "matcher": "Bash",
        "type": "command",
        "command": "./hooks/audit-bash-commands"
      }
    ]
  }
}
```

### Multiple Hooks for Same Event

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "type": "command",
        "command": "./hooks/format-code"
      },
      {
        "matcher": "Write|Edit",
        "type": "command",
        "command": "./hooks/update-index"
      }
    ]
  }
}
```

### Regex Matcher

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit|NotebookEdit",
        "type": "command",
        "command": "./hooks/validate-write-operations"
      }
    ]
  }
}
```

### Wildcard Matcher (All Tools)

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "*",
        "type": "command",
        "command": "./hooks/log-all-tools"
      }
    ]
  }
}
```

---

## Input/Output Specifications

### Exit Codes

| Code | Meaning | Behavior |
|------|---------|----------|
| 0 | Success | stdout shown in transcript mode; for SessionStart, added to context |
| 2 | Blocking error | stderr fed back to Claude; execution stops |
| Other | Non-blocking error | stderr shown to user; execution continues |

### JSON Output Fields

#### Standard Fields (All Hooks)
```json
{
  "continue": true,              // Required: whether to continue execution
  "output": "string",            // Optional: message to show/inject
  "suppressOutput": false,       // Optional: hide stdout from transcript
  "systemMessage": "string"      // Optional: system-level message
}
```

#### PreToolUse-Specific Fields
```json
{
  "permissionDecision": "approve",  // "approve" or "deny"
  "reason": "Explanation"           // Why decision was made
}
```

#### Stop Hook-Specific Fields
```json
{
  "stopReason": "string"  // Reason for stopping
}
```

### Prompt-Based Hooks (Advanced)

```json
{
  "hooks": {
    "Stop": [
      {
        "type": "prompt",
        "prompt": "Evaluate if the task is complete. Return {\"continue\": false} if complete."
      }
    ]
  }
}
```

---

## Example Implementations

### Example 1: SessionStart with State Loading

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

def main():
    # Read input
    hook_input = json.loads(sys.stdin.read()) if sys.stdin.isatty() == False else {}

    # Get directories
    project_dir = Path(os.environ.get('CLAUDE_PROJECT_DIR', '.')).resolve()
    state_dir = project_dir / '.claude-state'

    # Load state files
    output_sections = []

    # Session info
    session_id = hook_input.get('session_id', 'unknown')
    output_sections.append(f"## Session: {session_id}")
    output_sections.append(f"Started: {datetime.now().isoformat()}")
    output_sections.append("")

    # Load previous state
    if state_dir.exists():
        session_file = state_dir / 'session.yaml'
        if session_file.exists():
            content = session_file.read_text()
            output_sections.append("## Previous Session State")
            output_sections.append(f"```yaml\n{content}\n```")

    # Build response
    response = {
        "continue": True,
        "output": "\n".join(output_sections)
    }

    print(json.dumps(response))
    sys.exit(0)

if __name__ == "__main__":
    main()
```

### Example 2: PreToolUse - Block .env Writes

```python
#!/usr/bin/env python3
import json
import sys

def main():
    hook_input = json.loads(sys.stdin.read())

    tool_name = hook_input.get('tool_name', '')
    tool_input = hook_input.get('tool_input', {})
    file_path = tool_input.get('file_path', '')

    # Block writes to .env files
    if file_path.endswith('.env') or '/.env' in file_path:
        response = {
            "permissionDecision": "deny",
            "reason": "Modifications to .env files are not allowed for security"
        }
        print(json.dumps(response))
        sys.exit(2)

    # Allow
    response = {"permissionDecision": "approve"}
    print(json.dumps(response))
    sys.exit(0)

if __name__ == "__main__":
    main()
```

### Example 3: PostToolUse - Auto-format Python

```python
#!/usr/bin/env python3
import json
import sys
import subprocess
from pathlib import Path

def main():
    hook_input = json.loads(sys.stdin.read())

    tool_name = hook_input.get('tool_name', '')
    tool_input = hook_input.get('tool_input', {})
    file_path = tool_input.get('file_path', '')

    # Only format Python files
    if not file_path.endswith('.py'):
        response = {"continue": True}
        print(json.dumps(response))
        sys.exit(0)

    # Run black formatter
    try:
        result = subprocess.run(
            ['black', '--quiet', file_path],
            capture_output=True,
            timeout=5
        )

        if result.returncode == 0:
            response = {
                "continue": True,
                "output": f"✓ Formatted {Path(file_path).name} with black"
            }
        else:
            response = {
                "continue": True,
                "output": f"⚠ Could not format {Path(file_path).name}"
            }
    except Exception as e:
        response = {
            "continue": True,
            "output": f"⚠ Formatting error: {str(e)}"
        }

    print(json.dumps(response))
    sys.exit(0)

if __name__ == "__main__":
    main()
```

### Example 4: UserPromptSubmit - Context Injection

```python
#!/usr/bin/env python3
import json
import sys
import os
from pathlib import Path

def main():
    hook_input = json.loads(sys.stdin.read())
    user_input = hook_input.get('userInput', '') or hook_input.get('prompt', '')

    project_dir = Path(os.environ.get('CLAUDE_PROJECT_DIR', '.')).resolve()
    state_dir = project_dir / '.claude-state'

    # Detect keywords
    keywords = {
        'status': ['status', 'progress', 'what have', 'where are we'],
        'last': ['last time', 'previously', 'before', 'earlier'],
    }

    user_lower = user_input.lower()
    relevant_files = []

    for category, triggers in keywords.items():
        if any(trigger in user_lower for trigger in triggers):
            state_file = state_dir / f'{category}.yaml'
            if state_file.exists():
                content = state_file.read_text().strip()
                if content:
                    relevant_files.append((category, content))

    # Inject context if relevant
    if relevant_files:
        output = "## Relevant Context\n\n"
        for name, content in relevant_files:
            output += f"### {name.title()}\n```yaml\n{content}\n```\n\n"

        response = {"continue": True, "output": output}
    else:
        response = {"continue": True}

    print(json.dumps(response))
    sys.exit(0)

if __name__ == "__main__":
    main()
```

### Example 5: Stop Hook - Save Session Summary

```python
#!/usr/bin/env python3
import json
import sys
import os
from pathlib import Path
from datetime import datetime

def main():
    hook_input = json.loads(sys.stdin.read())

    project_dir = Path(os.environ.get('CLAUDE_PROJECT_DIR', '.')).resolve()
    state_dir = project_dir / '.claude-state'
    state_dir.mkdir(parents=True, exist_ok=True)

    # Save session end time
    session_file = state_dir / 'session.yaml'
    timestamp = datetime.now().isoformat()

    if session_file.exists():
        content = session_file.read_text()
        content += f"\nended_at: \"{timestamp}\"\n"
        session_file.write_text(content)

    response = {"continue": True}
    print(json.dumps(response))
    sys.exit(0)

if __name__ == "__main__":
    main()
```

---

## Testing & Debugging

### Manual Testing Template

```bash
#!/bin/bash
# test-hooks.sh - Test all hooks manually

PROJECT_DIR="/path/to/your/project"
cd "$PROJECT_DIR"
export CLAUDE_PROJECT_DIR="$PROJECT_DIR"

echo "Testing SessionStart hook..."
echo '{"session_id":"test-123","source":"startup"}' | \
  .claude/hooks/session-start | python3 -m json.tool
echo ""

echo "Testing Stop hook..."
echo '{}' | .claude/hooks/stop | python3 -m json.tool
echo ""

echo "Testing UserPromptSubmit hook..."
echo '{"userInput":"show status"}' | \
  .claude/hooks/user-prompt-submit | python3 -m json.tool
echo ""

echo "Testing PreToolUse hook (if exists)..."
echo '{"tool_name":"Write","tool_input":{"file_path":".env"}}' | \
  .claude/hooks/pre-tool-use | python3 -m json.tool
echo ""

echo "All tests complete!"
```

### Debug Logging Pattern

Add this to your hooks for debugging:

```python
import json
import sys
from pathlib import Path

# Debug logging
def debug_log(message):
    debug_file = Path('/tmp/claude-hook-debug.log')
    with open(debug_file, 'a') as f:
        from datetime import datetime
        timestamp = datetime.now().isoformat()
        f.write(f"[{timestamp}] {message}\n")

def main():
    try:
        hook_input = json.loads(sys.stdin.read())
        debug_log(f"Input: {json.dumps(hook_input)}")

        # Your hook logic
        result = {"continue": True}

        debug_log(f"Output: {json.dumps(result)}")
        print(json.dumps(result))
        sys.exit(0)

    except Exception as e:
        debug_log(f"ERROR: {str(e)}")
        import traceback
        debug_log(traceback.format_exc())
        sys.exit(1)
```

### Validation Script

```python
#!/usr/bin/env python3
"""Validate hook configuration and scripts."""

import json
import subprocess
from pathlib import Path
import sys

def validate_settings_json(settings_path):
    """Validate settings.json syntax and structure."""
    print("Checking settings.json...")

    # Check JSON syntax
    try:
        with open(settings_path) as f:
            settings = json.load(f)
        print("  ✓ Valid JSON syntax")
    except json.JSONDecodeError as e:
        print(f"  ✗ Invalid JSON: {e}")
        return False

    # Check hooks structure
    if 'hooks' not in settings:
        print("  ⚠ No hooks configured")
        return True

    hooks = settings['hooks']
    for event_name, hook_list in hooks.items():
        print(f"  Checking {event_name}...")

        if not isinstance(hook_list, list):
            print(f"    ✗ {event_name} should be a list")
            return False

        for i, hook_config in enumerate(hook_list):
            # Check for incorrect nesting
            if 'hooks' in hook_config and 'type' not in hook_config:
                print(f"    ✗ Hook {i}: Extra 'hooks' wrapper detected")
                print(f"       Remove nested 'hooks' array")
                return False

            if 'type' not in hook_config:
                print(f"    ✗ Hook {i}: Missing 'type' field")
                return False

            if 'command' not in hook_config and 'prompt' not in hook_config:
                print(f"    ✗ Hook {i}: Missing 'command' or 'prompt' field")
                return False

    print("  ✓ Hook structure valid")
    return True

def validate_hook_files(project_dir):
    """Validate hook script files."""
    print("\nChecking hook files...")
    hooks_dir = project_dir / '.claude' / 'hooks'

    if not hooks_dir.exists():
        print("  ⚠ No hooks directory found")
        return True

    for hook_file in hooks_dir.iterdir():
        if hook_file.name.startswith('.') or hook_file.name == '__pycache__':
            continue

        if not hook_file.is_file():
            continue

        print(f"  Checking {hook_file.name}...")

        # Check executable
        if not hook_file.stat().st_mode & 0o111:
            print(f"    ✗ Not executable")
            print(f"       Run: chmod +x {hook_file}")
            return False
        else:
            print(f"    ✓ Executable")

        # Check shebang
        with open(hook_file, 'rb') as f:
            first_line = f.readline().decode('utf-8', errors='ignore')
            if first_line.startswith('#!'):
                print(f"    ✓ Shebang: {first_line.strip()}")
            else:
                print(f"    ✗ Missing shebang")
                return False

        # Test execution
        try:
            result = subprocess.run(
                ['echo', '{}'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            test_result = subprocess.run(
                [str(hook_file)],
                input=result.stdout,
                capture_output=True,
                timeout=5
            )

            if test_result.returncode == 0:
                # Validate JSON output
                try:
                    output = json.loads(test_result.stdout)
                    if 'continue' in output:
                        print(f"    ✓ Executes successfully")
                    else:
                        print(f"    ⚠ Missing 'continue' field in output")
                except json.JSONDecodeError:
                    print(f"    ✗ Output is not valid JSON")
                    return False
            else:
                print(f"    ✗ Execution failed: {test_result.stderr.decode()}")
                return False

        except subprocess.TimeoutExpired:
            print(f"    ✗ Timeout (>5s)")
            return False
        except Exception as e:
            print(f"    ✗ Error: {e}")
            return False

    return True

def main():
    project_dir = Path.cwd()
    settings_path = project_dir / '.claude' / 'settings.json'

    print(f"Validating hooks in: {project_dir}\n")

    if not settings_path.exists():
        print("✗ No .claude/settings.json found")
        sys.exit(1)

    success = True
    success = validate_settings_json(settings_path) and success
    success = validate_hook_files(project_dir) and success

    if success:
        print("\n✓ All validations passed!")
        sys.exit(0)
    else:
        print("\n✗ Validation failed")
        sys.exit(1)

if __name__ == '__main__':
    main()
```

Save as `validate-hooks.py` and run:
```bash
chmod +x validate-hooks.py
./validate-hooks.py
```

---

## Common Patterns Library

### Pattern: Conditional Context Injection

```python
def inject_context_if_relevant(user_input, context_files):
    """Inject context only if user input contains relevant keywords."""
    user_lower = user_input.lower()

    for context_name, keywords, file_path in context_files:
        if any(kw in user_lower for kw in keywords):
            if Path(file_path).exists():
                content = Path(file_path).read_text()
                return f"## {context_name}\n```\n{content}\n```\n"

    return None
```

### Pattern: Safe File Operations

```python
def safe_file_read(file_path, default=''):
    """Safely read file with fallback."""
    try:
        path = Path(file_path)
        if path.exists() and path.is_file():
            return path.read_text()
        return default
    except Exception:
        return default

def safe_file_write(file_path, content):
    """Safely write file with error handling."""
    try:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return True
    except Exception as e:
        debug_log(f"Write error: {e}")
        return False
```

### Pattern: Environment Variable Validation

```python
def get_project_dir():
    """Get project directory with validation."""
    project_dir = os.environ.get('CLAUDE_PROJECT_DIR')

    if not project_dir:
        # Fallback to current directory
        project_dir = os.getcwd()

    path = Path(project_dir).resolve()

    if not path.exists():
        raise ValueError(f"Project directory does not exist: {path}")

    return path
```

### Pattern: Timeout Protection

```python
import signal

def timeout_handler(signum, frame):
    raise TimeoutError("Hook execution timeout")

def with_timeout(seconds):
    """Decorator for timeout protection."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Set the signal handler
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(seconds)

            try:
                result = func(*args, **kwargs)
            finally:
                # Disable the alarm
                signal.alarm(0)

            return result
        return wrapper
    return decorator

@with_timeout(5)
def slow_operation():
    # Your code here
    pass
```

### Pattern: Structured Error Responses

```python
def error_response(message, blocking=False):
    """Create standardized error response."""
    response = {
        "continue": not blocking,
        "output": f"⚠️ Hook Error: {message}"
    }

    exit_code = 2 if blocking else 1
    print(json.dumps(response), file=sys.stdout)
    sys.exit(exit_code)

def success_response(output=None):
    """Create standardized success response."""
    response = {"continue": True}
    if output:
        response["output"] = output

    print(json.dumps(response))
    sys.exit(0)
```

---

## Security Best Practices

### 1. Input Validation

```python
def validate_file_path(file_path):
    """Validate file path for security."""
    path = Path(file_path).resolve()

    # Check for path traversal
    if '..' in str(file_path):
        return False, "Path traversal detected"

    # Check for absolute path escaping project
    project_dir = get_project_dir()
    try:
        path.relative_to(project_dir)
    except ValueError:
        return False, "Path outside project directory"

    # Check for sensitive files
    sensitive_patterns = ['.env', '.git/', '*.key', '*.pem', 'secrets/']
    for pattern in sensitive_patterns:
        if fnmatch.fnmatch(str(path), f"*{pattern}*"):
            return False, f"Access to sensitive files denied"

    return True, None
```

### 2. Command Injection Prevention

```python
import shlex

def safe_shell_command(command, args):
    """Build safe shell command."""
    # Use list format, not string concatenation
    cmd = [command] + [shlex.quote(arg) for arg in args]

    result = subprocess.run(
        cmd,
        capture_output=True,
        timeout=5,
        check=False
    )

    return result
```

### 3. Secrets Detection

```python
import re

def contains_secrets(content):
    """Check if content contains potential secrets."""
    patterns = [
        r'api[_-]?key.*[=:]\s*["\']?[\w-]{20,}',
        r'password.*[=:]\s*["\']?[\w-]{8,}',
        r'secret.*[=:]\s*["\']?[\w-]{20,}',
        r'token.*[=:]\s*["\']?[\w-]{20,}',
    ]

    for pattern in patterns:
        if re.search(pattern, content, re.IGNORECASE):
            return True

    return False
```

### 4. Rate Limiting

```python
from datetime import datetime, timedelta
from pathlib import Path
import json

def check_rate_limit(max_calls=10, window_minutes=1):
    """Implement rate limiting for hooks."""
    rate_limit_file = Path('/tmp/claude-hook-rate-limit.json')

    now = datetime.now()

    if rate_limit_file.exists():
        data = json.loads(rate_limit_file.read_text())
        calls = [
            datetime.fromisoformat(ts)
            for ts in data.get('calls', [])
            if datetime.fromisoformat(ts) > now - timedelta(minutes=window_minutes)
        ]
    else:
        calls = []

    if len(calls) >= max_calls:
        return False, f"Rate limit exceeded: {len(calls)} calls in {window_minutes}min"

    calls.append(now)
    rate_limit_file.write_text(json.dumps({
        'calls': [c.isoformat() for c in calls]
    }))

    return True, None
```

---

## Performance Optimization

### 1. Caching Pattern

```python
from datetime import datetime, timedelta
import hashlib

def cached_operation(cache_file, ttl_minutes, operation):
    """Cache expensive operations."""
    cache_path = Path(cache_file)

    # Check cache validity
    if cache_path.exists():
        age = datetime.now() - datetime.fromtimestamp(cache_path.stat().st_mtime)
        if age < timedelta(minutes=ttl_minutes):
            return json.loads(cache_path.read_text())

    # Perform operation
    result = operation()

    # Cache result
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(json.dumps(result))

    return result
```

### 2. Lazy Loading

```python
class LazyState:
    """Lazy load state files only when accessed."""

    def __init__(self, state_dir):
        self.state_dir = Path(state_dir)
        self._cache = {}

    def get(self, state_name):
        """Get state file, loading if necessary."""
        if state_name not in self._cache:
            file_path = self.state_dir / f"{state_name}.yaml"
            if file_path.exists():
                self._cache[state_name] = file_path.read_text()
            else:
                self._cache[state_name] = None

        return self._cache[state_name]
```

### 3. Async Operations (for Python 3.7+)

```python
import asyncio

async def async_hook_operation():
    """Run multiple operations concurrently."""
    tasks = [
        asyncio.create_task(load_state_file('session')),
        asyncio.create_task(load_state_file('progress')),
        asyncio.create_task(check_git_status()),
    ]

    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results

def main():
    results = asyncio.run(async_hook_operation())
    # Process results
```

---

## Real-World Complete Examples

### Complete Example: Smart SessionStart Hook

```python
#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""
Smart SessionStart Hook
- Loads relevant state
- Shows git status
- Checks for updates
- Provides session context
"""

import json
import sys
import os
import subprocess
from pathlib import Path
from datetime import datetime, timezone

def get_git_status(project_dir):
    """Get brief git status."""
    try:
        result = subprocess.run(
            ['git', 'status', '--short'],
            cwd=project_dir,
            capture_output=True,
            text=True,
            timeout=2
        )
        if result.returncode == 0 and result.stdout.strip():
            return f"Git status:\n```\n{result.stdout.strip()}\n```"
        return None
    except:
        return None

def get_recent_files(project_dir, limit=5):
    """Get recently modified files."""
    try:
        result = subprocess.run(
            ['find', '.', '-type', 'f', '-not', '-path', '*/.*', '-mtime', '-1'],
            cwd=project_dir,
            capture_output=True,
            text=True,
            timeout=2
        )
        if result.returncode == 0:
            files = [f for f in result.stdout.split('\n') if f.strip()][:limit]
            if files:
                return "Recently modified:\n" + "\n".join(f"  - {f}" for f in files)
        return None
    except:
        return None

def load_state_files(state_dir):
    """Load and return relevant state."""
    states = {}

    for state_file in ['session.yaml', 'progress.yaml', 'context.json']:
        file_path = state_dir / state_file
        if file_path.exists():
            content = file_path.read_text().strip()
            if content:
                states[state_file] = content

    return states

def main():
    # Read input
    try:
        hook_input = json.loads(sys.stdin.read())
    except:
        hook_input = {}

    # Get directories
    project_dir = Path(os.environ.get('CLAUDE_PROJECT_DIR', '.')).resolve()
    state_dir = project_dir / '.claude-state'

    # Build output
    output_sections = []

    # Header
    session_id = hook_input.get('session_id', 'unknown')[:8]
    output_sections.append(f"# Session Started")
    output_sections.append(f"**Session ID:** {session_id}")
    output_sections.append(f"**Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    output_sections.append("")

    # Git status
    git_status = get_git_status(project_dir)
    if git_status:
        output_sections.append(git_status)
        output_sections.append("")

    # Recent files
    recent = get_recent_files(project_dir)
    if recent:
        output_sections.append(recent)
        output_sections.append("")

    # Load state
    states = load_state_files(state_dir)
    if states:
        output_sections.append("## Loaded State")
        for name, content in states.items():
            output_sections.append(f"### {name}")
            ext = 'json' if name.endswith('.json') else 'yaml'
            output_sections.append(f"```{ext}\n{content}\n```")
            output_sections.append("")

    # Instructions
    output_sections.append("---")
    output_sections.append("Ready to assist with development tasks.")

    # Return response
    response = {
        "continue": True,
        "output": "\n".join(output_sections)
    }

    print(json.dumps(response))
    sys.exit(0)

if __name__ == "__main__":
    main()
```

---

## Additional Resources

### Official Documentation
- **Claude Code Hooks Reference**: https://code.claude.com/docs/en/hooks
- **Hooks Getting Started Guide**: https://code.claude.com/docs/en/hooks-guide
- **Settings.json Schema**: https://json.schemastore.org/claude-code-settings.json

### Community Resources
- **Hooks Mastery Repository**: https://github.com/disler/claude-code-hooks-mastery
- **Complete Hooks Guide**: https://www.eesel.ai/blog/hooks-in-claude-code
- **Claude Code Cheat Sheet**: https://shipyard.build/blog/claude-code-cheat-sheet

### GitHub Issues & Discussions
- **Issue Tracker**: https://github.com/anthropics/claude-code/issues
- **Hook-related Issues**: Search for "hooks" label
- **Feature Requests**: Discussions section

### Example Repositories
- Search GitHub for: `topic:claude-code-hooks`
- Example configs: `path:.claude/settings.json hooks`

---

## Troubleshooting Quick Reference

| Error | Quick Fix |
|-------|-----------|
| Hook error (generic) | Run: `echo '{}' \| .claude/hooks/HOOKNAME` |
| Permission denied | Run: `chmod +x .claude/hooks/*` |
| JSON parse error | Validate: `cat .claude/settings.json \| python3 -m json.tool` |
| File not found | Check path in settings.json, use `$CLAUDE_PROJECT_DIR` |
| Python not found | Install Python 3.9+, check shebang |
| Hook not executing | Check settings.json structure (no nested "hooks") |
| Output not appearing | Check exit code is 0, ensure JSON format |
| Intermittent failures | Add debug logging to `/tmp/hook-debug.log` |

---

**Last Updated:** November 2025
**Version:** 1.0
**Compatibility:** Claude Code v2.x
