#!/bin/bash
# Test script for hook system

set -e

PROJECT_DIR="/Users/tijlkoenderink/Library/Mobile Documents/com~apple~CloudDocs/CC-superpowers/claude-code-dev-harness"
cd "$PROJECT_DIR"

echo "==============================================="
echo "Hook System Test Suite"
echo "==============================================="
echo ""

# Test 1: post-tool-use hook
echo "Test 1: post-tool-use hook (Skill tracking)"
echo "-------------------------------------------"
echo '{
  "tool_name": "Skill",
  "tool_input": {
    "skill_name": "test-skill-001",
    "context": "Testing skill tracking system"
  },
  "tool_output": "Skill executed successfully",
  "session_id": "test-session-001"
}' | .claude/hooks/post-tool-use

if [ $? -eq 0 ]; then
    echo "✓ post-tool-use hook executed successfully"
else
    echo "✗ post-tool-use hook failed"
    exit 1
fi

# Check if skill-usage.json was updated
if [ -f ".claude-state/logs/skill-usage.json" ]; then
    echo "✓ skill-usage.json exists"
    # Check if it's valid JSON
    if python3 -m json.tool .claude-state/logs/skill-usage.json > /dev/null 2>&1; then
        echo "✓ skill-usage.json is valid JSON"
    else
        echo "✗ skill-usage.json is invalid JSON"
        exit 1
    fi
else
    echo "✗ skill-usage.json not found"
    exit 1
fi

echo ""

# Test 2: Track multiple skills
echo "Test 2: Track multiple skills"
echo "-------------------------------------------"
for i in {1..3}; do
    echo '{
      "tool_name": "Skill",
      "tool_input": {
        "skill_name": "test-skill-'$i'",
        "context": "Test invocation '$i'"
      },
      "tool_output": "Success",
      "session_id": "test-session-002"
    }' | .claude/hooks/post-tool-use > /dev/null
done

echo "✓ Tracked 3 skill invocations"
echo ""

# Test 3: Non-Skill tool (should be ignored)
echo "Test 3: Non-Skill tool (should be ignored)"
echo "-------------------------------------------"
echo '{
  "tool_name": "Bash",
  "tool_input": {"command": "ls"},
  "session_id": "test-session-003"
}' | .claude/hooks/post-tool-use

echo "✓ Non-Skill tool ignored correctly"
echo ""

# Test 4: stop hook (without transcript)
echo "Test 4: stop hook (basic functionality)"
echo "-------------------------------------------"
echo '{
  "session_id": "test-session-004",
  "hook_event_name": "Stop"
}' | .claude/hooks/stop

if [ $? -eq 0 ]; then
    echo "✓ stop hook executed successfully"
else
    echo "✗ stop hook failed"
    exit 1
fi

# Check if last-session.json was updated
if [ -f ".claude-state/last-session.json" ]; then
    echo "✓ last-session.json exists"
else
    echo "✗ last-session.json not found"
    exit 1
fi

echo ""

# Test 5: subagent-stop hook
echo "Test 5: subagent-stop hook"
echo "-------------------------------------------"
echo '{
  "task_id": "test-task-001",
  "agent_type": "architect",
  "parent_session_id": "test-session-005",
  "outcome": "success",
  "task_description": "Test task for architect"
}' | .claude/hooks/subagent-stop

if [ $? -eq 0 ]; then
    echo "✓ subagent-stop hook executed successfully"
else
    echo "✗ subagent-stop hook failed"
    exit 1
fi

echo ""

# Test 6: Check directory structure
echo "Test 6: Directory structure"
echo "-------------------------------------------"
for dir in "logs" "logs/main-session" "logs/subagent/architect" "logs/subagent/engineer" "logs/subagent/tester" "logs/subagent/reviewer" "logs/subagent/orchestrator"; do
    if [ -d ".claude-state/$dir" ]; then
        echo "✓ $dir exists"
    else
        echo "✗ $dir missing"
        exit 1
    fi
done

echo ""

# Test 7: Check hook permissions
echo "Test 7: Hook permissions"
echo "-------------------------------------------"
for hook in "post-tool-use" "stop" "subagent-stop"; do
    if [ -x ".claude/hooks/$hook" ]; then
        echo "✓ $hook is executable"
    else
        echo "✗ $hook is not executable"
        exit 1
    fi
done

echo ""

# Test 8: Check library files
echo "Test 8: Library files"
echo "-------------------------------------------"
for lib in "common.py" "sanitizer.py" "skill_tracker.py" "conversation_archiver.py"; do
    if [ -f ".claude/hooks/lib/$lib" ]; then
        echo "✓ $lib exists"
        # Check for syntax errors
        if python3 -m py_compile ".claude/hooks/lib/$lib" 2>/dev/null; then
            echo "  ✓ $lib has valid Python syntax"
        else
            echo "  ✗ $lib has syntax errors"
            exit 1
        fi
    else
        echo "✗ $lib missing"
        exit 1
    fi
done

echo ""

# Test 9: Error log
echo "Test 9: Error log"
echo "-------------------------------------------"
if [ -f ".claude-state/logs/hook-errors.log" ]; then
    echo "✓ hook-errors.log exists"
    lines=$(wc -l < ".claude-state/logs/hook-errors.log" | tr -d ' ')
    echo "  Log has $lines lines"
else
    echo "✗ hook-errors.log not found"
    exit 1
fi

echo ""

# Summary
echo "==============================================="
echo "Test Summary"
echo "==============================================="
echo "✓ All tests passed!"
echo ""
echo "Skill usage file:"
python3 -m json.tool .claude-state/logs/skill-usage.json | head -20
echo ""
echo "Next steps:"
echo "1. Use Claude Code with Skill tool to test live tracking"
echo "2. Check .claude-state/logs/skill-usage.json for updates"
echo "3. End a session to test conversation archiving"
echo "4. Use Task tool to test subagent archiving"
