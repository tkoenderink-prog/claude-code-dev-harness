---
name: fixing-claude-code-hooks
description: Use when encountering Claude Code hook execution errors (SessionStart, Stop, UserPromptSubmit), hooks not executing at all, JSON parsing errors from hooks, permission denied errors, path issues with spaces in filenames, or hook configuration problems - provides systematic 10-step diagnostic workflow with quick-fix checklist resolving 90% of common hook configuration, permission, environment, and path issues
---

# Fixing Claude Code Hooks

## When to Use This Skill

Use this skill when you encounter:
- Hook execution errors in Claude Code
- "SessionStart:startup hook error"
- "Stop hook error"
- "UserPromptSubmit hook error"
- Hooks not executing at all
- Hook output not appearing
- JSON parsing errors in hooks

## Overview

Claude Code hooks are shell commands or Python scripts that execute at specific lifecycle events. When they fail, it's usually due to:

1. **Configuration errors** - Incorrect settings.json structure
2. **Permission errors** - Scripts not executable
3. **Path errors** - Incorrect file paths or working directory
4. **Environment errors** - Missing environment variables
5. **Script errors** - Bugs in the hook script itself
6. **JSON errors** - Invalid JSON output from hooks

## Diagnostic Process

Follow this checklist systematically:

**⚡ QUICK CHECK (Updated 2025):** If your error shows `hooks: Expected array, but received undefined`, skip to Step 1 - you're using the old hook format and need to add the required "hooks" array wrapper. This fixes 80% of hook errors.

### Step 1: Verify Hook Configuration Structure

**Check:** Is your `.claude/settings.json` hook configuration correct?

**IMPORTANT: Claude Code hook format changed in 2025** - All hooks now require the nested "hooks" array structure with optional matchers.

**INCORRECT (OLD FORMAT):**
```json
{
  "hooks": {
    "SessionStart": [
      {
        "type": "command",  // ❌ WRONG - missing "hooks" wrapper
        "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/session-start"
      }
    ]
  }
}
```

**CORRECT (NEW FORMAT as of 2025):**
```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [  // ✓ REQUIRED - "hooks" array wrapper
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/session-start"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/stop"
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/user-prompt-submit"
          }
        ]
      }
    ]
  }
}
```

**CRITICAL: Quote $CLAUDE_PROJECT_DIR to handle spaces in paths!**

The format requires TWO elements:
1. ✓ "hooks" array wrapper (for validation)
2. ✓ Quote the variable: `"\"$CLAUDE_PROJECT_DIR\""` (prevents path splitting on spaces)

**How to fix:**
1. Open `.claude/settings.json`
2. For ALL hooks (SessionStart, Stop, UserPromptSubmit, PreToolUse, PostToolUse), wrap the hook definition in a "hooks" array
3. Quote the `$CLAUDE_PROJECT_DIR` variable to prevent path splitting when your project path contains spaces
4. Optionally add a "matcher" field for tool-specific hooks:

```json
"PreToolUse": [
  {
    "matcher": "Write|Edit",  // Optional: only trigger for Write or Edit tools
    "hooks": [                // Required: wrap in hooks array
      {
        "type": "command",
        "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/your-hook-script"
      }
    ]
  }
]
```

### Step 2: Validate JSON Syntax

**Check:** Is your settings.json valid JSON?

**How to check:**
```bash
cat .claude/settings.json | python3 -m json.tool
```

If this fails, you have syntax errors (missing commas, quotes, brackets, etc.)

**Common JSON errors:**
- Trailing commas in arrays or objects
- Missing quotes around strings
- Unescaped quotes in strings
- Missing closing brackets

### Step 3: Verify File Permissions

**Check:** Are your hook scripts executable?

**How to check:**
```bash
ls -la .claude/hooks/
```

**Expected output:**
```
-rwxr-xr-x  session-start      # Note the 'x' permissions
-rwxr-xr-x  stop
-rwxr-xr-x  user-prompt-submit
```

**How to fix:**
```bash
chmod +x .claude/hooks/session-start
chmod +x .claude/hooks/stop
chmod +x .claude/hooks/user-prompt-submit
```

### Step 4: Verify Python Shebang

**Check:** Does your Python hook have the correct shebang?

**How to check:**
```bash
head -n 1 .claude/hooks/session-start
```

**Expected output:**
```
#!/usr/bin/env python3
```

**Common mistakes:**
- `#!/usr/bin/python` (wrong - should use python3)
- `#!/usr/bin/python3` (less portable than `env python3`)
- Missing shebang entirely

**How to fix:**
Ensure first line is exactly: `#!/usr/bin/env python3`

### Step 5: Verify Python Availability

**Check:** Is Python 3.9+ available?

**How to check:**
```bash
python3 --version
which python3
```

**Expected:** Python 3.9 or higher

**How to fix:** Install Python 3.9+ via homebrew (macOS) or package manager

### Step 6: Test Hook Manually

**Check:** Does the hook work when run manually?

**How to test SessionStart hook:**
```bash
cd /path/to/your/project
export CLAUDE_PROJECT_DIR="$PWD"
echo '{}' | .claude/hooks/session-start
```

**Expected:** Valid JSON output with `"continue": true`

**How to test Stop hook:**
```bash
echo '{}' | .claude/hooks/stop
```

**How to test UserPromptSubmit hook:**
```bash
echo '{"userInput":"test message"}' | .claude/hooks/user-prompt-submit
```

**If manual test fails:**
- Check Python syntax errors in the script
- Check for missing imports
- Check for file path issues
- Look at error messages in stderr

### Step 7: Check Hook Output Format

**Check:** Does your hook return valid JSON?

**Required format:**
```json
{
  "continue": true
}
```

**Extended format with output:**
```json
{
  "continue": true,
  "output": "Additional context or messages"
}
```

**Common mistakes:**
- Not printing JSON to stdout
- Printing extra debug messages before/after JSON
- Invalid JSON syntax
- Missing `"continue"` field

### Step 8: Verify Environment Variables

**Check:** Does your hook rely on environment variables?

**Available environment variables:**
- `CLAUDE_PROJECT_DIR` - The project directory path
- `CLAUDE_ENV_FILE` - Path to file for persisting env vars (SessionStart only)
- Standard shell variables (`HOME`, `PATH`, etc.)

**Common mistake:**
Using `os.getcwd()` instead of `os.environ.get('CLAUDE_PROJECT_DIR', '.')`

**Correct approach:**
```python
import os
from pathlib import Path

# Always use CLAUDE_PROJECT_DIR
project_dir = Path(os.environ.get('CLAUDE_PROJECT_DIR', '.')).resolve()
```

### Step 9: Check for Path Issues

**Check:** Are file paths in your hook script correct?

**Common mistakes:**
- Using relative paths without proper context
- Hardcoding paths instead of using CLAUDE_PROJECT_DIR
- Path with spaces not properly handled

**Best practice:**
```python
from pathlib import Path
import os

# Get project directory
project_dir = Path(os.environ.get('CLAUDE_PROJECT_DIR', '.')).resolve()

# Build paths relative to project
state_dir = project_dir / '.claude-state'
config_file = project_dir / '.claude' / 'settings.json'
```

### Step 10: Enable Debug Mode

**Check:** What does Claude Code debug output show?

**How to enable:**
```bash
claude --debug
```

This shows detailed hook execution information including:
- Hook registration
- Hook matching
- Hook execution
- Hook output and errors

## Quick Fix Checklist

Use this rapid-fire checklist to fix 90% of hook issues:

```bash
# 1. Validate JSON syntax
cat .claude/settings.json | python3 -m json.tool > /tmp/test.json && mv /tmp/test.json .claude/settings.json

# 2. Fix permissions
chmod +x .claude/hooks/*

# 3. Test hooks manually
cd /path/to/project
export CLAUDE_PROJECT_DIR="$PWD"
echo '{}' | .claude/hooks/session-start
echo '{}' | .claude/hooks/stop
echo '{"userInput":"test"}' | .claude/hooks/user-prompt-submit

# 4. Check Python version
python3 --version  # Should be 3.9+

# 5. Verify shebang
head -n 1 .claude/hooks/session-start  # Should be #!/usr/bin/env python3
```

## Common Error Messages & Solutions

### "hooks: Expected array, but received undefined"

**Symptom:** Hook validation error showing `hooks: Expected array, but received undefined` for SessionStart, Stop, or UserPromptSubmit hooks

**Cause:** Missing required `"hooks": [...]` array wrapper in `.claude/settings.json` - This is the #1 most common hook configuration error since the 2025 format change

**Quick diagnostic:** If you see "Expected array, but received undefined" for hooks, you're using the old format

**Solution:**
1. Open `.claude/settings.json`
2. Look for this INCORRECT (old) pattern:
```json
"SessionStart": [
  {
    "type": "command",  // ❌ Missing required "hooks" wrapper
    "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/session-start"
  }
]
```

3. Fix to this CORRECT (new 2025) pattern:
```json
"SessionStart": [
  {
    "hooks": [  // ✓ Required "hooks" array wrapper
      {
        "type": "command",
        "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/session-start"  // ✓ Quote variable
      }
    ]
  }
]
```

4. Apply the same fix to `Stop`, `UserPromptSubmit`, and any other hooks
5. **IMPORTANT:** Quote `$CLAUDE_PROJECT_DIR` if your path contains spaces (e.g., "Library/Mobile Documents")
6. Validate JSON: `cat .claude/settings.json | python3 -m json.tool`
7. Restart Claude Code

**Why this happens:** Claude Code changed the hook format in 2025 to support matchers. All hooks now require the nested "hooks" array structure.

### "Failed with non-blocking status code: /bin/sh: .../Library/Mobile: No such file or directory"

**Symptom:** Hook error shows a path with spaces being split incorrectly (e.g., `/Users/tijlkoenderink/Library/Mobile Documents/...` becomes `/Library/Mobile: No such file or directory`)

**Cause:** The `$CLAUDE_PROJECT_DIR` variable is not quoted in the command, causing the shell to split the path on spaces.

**Solution:**
Quote the `$CLAUDE_PROJECT_DIR` variable in your command:

**INCORRECT:**
```json
"command": "$CLAUDE_PROJECT_DIR/.claude/hooks/stop"
```

**CORRECT:**
```json
"command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/stop"
```

**Why this works:** Quoting the variable prevents the shell from splitting the expanded path on spaces, treating the entire path as a single token.

### "SessionStart:startup hook error"

**Cause:** Hook script failed or returned non-zero exit code

**Solutions:**
1. Test hook manually (see Step 6)
2. Check for Python errors in the script
3. Verify JSON output format
4. Check file permissions

### "Stop hook error"

**Cause:** Stop hook failed during session cleanup

**Solutions:**
1. Check if `.claude-state/` directory is writable
2. Test hook manually
3. Verify script doesn't depend on session-specific data

### "UserPromptSubmit hook error"

**Cause:** Hook failed during prompt submission

**Solutions:**
1. Check if hook can read from stdin
2. Verify JSON parsing of input
3. Test with sample input: `echo '{"userInput":"test"}' | .claude/hooks/user-prompt-submit`

### "ENOENT: no such file or directory"

**Cause:** Hook file not found at specified path

**Solutions:**
1. Verify path in settings.json matches actual file location
2. Use `$CLAUDE_PROJECT_DIR` variable for project-relative paths
3. Check for typos in filename

### "Permission denied"

**Cause:** Hook script not executable

**Solution:**
```bash
chmod +x .claude/hooks/session-start
chmod +x .claude/hooks/stop
chmod +x .claude/hooks/user-prompt-submit
```

### JSON parse error

**Cause:** Hook output is not valid JSON

**Solutions:**
1. Ensure hook only prints JSON to stdout
2. Remove debug print statements
3. Validate JSON structure
4. Test with: `echo '{}' | your-hook | python3 -m json.tool`

## Reference Implementation

Here's a minimal working hook template:

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

def main():
    """Main hook execution."""
    # Read hook input from stdin
    try:
        hook_input = json.loads(sys.stdin.read())
    except:
        hook_input = {}

    # Get project directory
    project_dir = Path(os.environ.get('CLAUDE_PROJECT_DIR', '.')).resolve()

    # Your hook logic here
    # ...

    # Return success response
    response = {
        "continue": True
        # Optional: "output": "Additional context"
    }

    print(json.dumps(response))
    sys.exit(0)

if __name__ == "__main__":
    main()
```

## Advanced Troubleshooting

### Issue: Hooks work manually but fail in Claude Code

**Diagnosis:** Environment difference between manual test and Claude Code execution

**Solutions:**
1. Check if Claude Code runs from different directory
2. Verify environment variables are set by Claude Code
3. Use absolute paths or `CLAUDE_PROJECT_DIR`
4. Add logging to hook to compare environments:

```python
import json
import os

with open('/tmp/hook-debug.log', 'w') as f:
    f.write(f"CWD: {os.getcwd()}\n")
    f.write(f"PROJECT_DIR: {os.environ.get('CLAUDE_PROJECT_DIR')}\n")
    f.write(f"PATH: {os.environ.get('PATH')}\n")
```

### Issue: Hook intermittently fails

**Diagnosis:** Race condition or timing issue

**Solutions:**
1. Add timeout protection
2. Check for file locking issues
3. Add retry logic for network operations
4. Use proper exception handling

### Issue: Hook output not appearing

**Diagnosis:** Output suppression or wrong exit code

**Solutions:**
1. Verify exit code is 0 for success
2. Check you're printing to stdout (not stderr)
3. Ensure JSON is properly formatted
4. Don't set `"suppressOutput": true` unless intended

## Testing Strategy

### Unit Test Your Hooks

Create test inputs for each hook type:

```bash
# Test SessionStart
echo '{
  "session_id": "test-123",
  "hook_event_name": "SessionStart",
  "source": "startup"
}' | .claude/hooks/session-start | python3 -m json.tool

# Test Stop
echo '{
  "session_id": "test-123",
  "hook_event_name": "Stop"
}' | .claude/hooks/stop | python3 -m json.tool

# Test UserPromptSubmit with various inputs
echo '{"userInput":"test message"}' | .claude/hooks/user-prompt-submit | python3 -m json.tool
echo '{"userInput":"progress status"}' | .claude/hooks/user-prompt-submit | python3 -m json.tool
```

### Integration Test

1. Start Claude Code with hooks enabled
2. Watch for hook execution messages
3. Verify expected behavior
4. Check `.claude-state/` for state file updates

## Resources

### Official Documentation
- [Claude Code Hooks Reference](https://code.claude.com/docs/en/hooks) - Complete hook types and API
- [Hooks Guide](https://code.claude.com/docs/en/hooks-guide) - Getting started tutorial
- [Settings.json Schema](https://json.schemastore.org/claude-code-settings.json) - JSON schema

### Community Resources
- [Claude Code Hooks Mastery](https://github.com/disler/claude-code-hooks-mastery) - Example hooks repository
- [eesel.ai Hooks Guide](https://www.eesel.ai/blog/hooks-in-claude-code) - Complete guide with examples
- [Claude Code Issue Tracker](https://github.com/anthropics/claude-code/issues) - Known issues and workarounds

### Common Patterns
- [Logging hooks](https://www.eesel.ai/blog/hooks-in-claude-code#logging-operations)
- [Code formatting hooks](https://www.eesel.ai/blog/hooks-in-claude-code#post-execution-automation)
- [Access control hooks](https://www.eesel.ai/blog/hooks-in-claude-code#access-control)

## Workflow

When using this skill, follow this order:

1. **Run Quick Fix Checklist** (5 min)
   - Fixes 90% of common issues

2. **If still failing, run Diagnostic Process** (10 min)
   - Systematic step-by-step diagnosis

3. **If still failing, Advanced Troubleshooting** (15 min)
   - Environment-specific issues

4. **If still failing, create minimal reproduction** (20 min)
   - Test with minimal hook
   - Report issue with details

## Success Criteria

Your hooks are fixed when:
- ✅ `claude` starts without hook errors
- ✅ Manual hook tests succeed
- ✅ JSON syntax validates
- ✅ File permissions are correct
- ✅ Hook output appears in Claude Code
- ✅ Expected behavior occurs (state loaded, etc.)

## Prevention

To avoid future hook issues:

1. **Use version control** - Track hook changes in git
2. **Test before committing** - Run manual tests
3. **Use templates** - Start from working examples
4. **Document customizations** - Note why you changed hooks
5. **Regular validation** - Run `cat .claude/settings.json | python3 -m json.tool`
6. **Keep it simple** - Complex hooks = more failure modes

## Emergency Bypass

If you need to disable hooks temporarily:

1. **Rename hooks directory:**
   ```bash
   mv .claude/hooks .claude/hooks.disabled
   ```

2. **Remove from settings.json:**
   - Comment out or remove the entire "hooks" section

3. **Use command flag:**
   ```bash
   claude --no-hooks  # If this flag exists
   ```

4. **Fix hooks offline**, then re-enable

---

**Remember:** Hooks execute with your environment's credentials and permissions. Always review hook code for security before enabling.
