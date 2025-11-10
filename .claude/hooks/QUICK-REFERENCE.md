# Hook System - Quick Reference Card

## Quick Start

### Run Tests
```bash
./.claude/hooks/test-hooks.sh
```

### View Skill Usage
```bash
cat .claude-state/logs/skill-usage.json | python3 -m json.tool
```

### View Archives
```bash
ls -lh .claude-state/logs/main-session/
ls -lh .claude-state/logs/subagent/*/
```

### Check Errors
```bash
tail -f .claude-state/logs/hook-errors.log
```

---

## File Locations

| File | Purpose |
|------|---------|
| `.claude/hooks/post-tool-use` | Skill tracking hook |
| `.claude/hooks/stop` | Main session archiving |
| `.claude/hooks/subagent-stop` | Subagent archiving |
| `.claude-state/logs/skill-usage.json` | Skill usage data |
| `.claude-state/logs/hook-errors.log` | Error log |
| `.claude-state/logs/main-session/` | Main archives |
| `.claude-state/logs/subagent/` | Subagent archives |

---

## Common Commands

### View Top Skills
```bash
cat .claude-state/logs/skill-usage.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
skills = sorted(data['skills'].items(), key=lambda x: x[1]['count'], reverse=True)
for skill, stats in skills[:10]:
    print(f\"{skill}: {stats['count']} times (success rate: {stats['success_rate']:.0%})\")
"
```

### View Today's Stats
```bash
cat .claude-state/logs/skill-usage.json | python3 -c "
import json, sys
from datetime import date
data = json.load(sys.stdin)
today = str(date.today())
if today in data['daily_stats']:
    stats = data['daily_stats'][today]
    print(f\"Invocations: {stats['invocations']}\")
    print(f\"Unique skills: {len(stats['unique_skills'])}\")
    print(f\"Sessions: {len(stats['unique_sessions'])}\")
"
```

### Count Archives
```bash
echo "Main sessions: $(find .claude-state/logs/main-session -name '*.jsonl' | wc -l)"
echo "Subagent tasks: $(find .claude-state/logs/subagent -name '*.jsonl' | wc -l)"
```

### Clean Old Archives (>6 months)
```bash
find .claude-state/logs/main-session -name "*.jsonl" -mtime +180 -delete
find .claude-state/logs/subagent -name "*.jsonl" -mtime +180 -delete
```

---

## Troubleshooting

### Hook Not Executing
```bash
# Check if executable
ls -la .claude/hooks/post-tool-use

# Make executable
chmod +x .claude/hooks/post-tool-use
```

### Import Errors
```bash
# Check Python syntax
python3 -m py_compile .claude/hooks/lib/skill_tracker.py

# Test import
python3 -c "import sys; sys.path.insert(0, '.claude/hooks/lib'); import skill_tracker"
```

### File Lock Issues
```bash
# Find stale locks
find .claude-state/logs -name "*.lock"

# Remove (only if no Claude Code running!)
find .claude-state/logs -name "*.lock" -delete
```

---

## Data Schemas

### Skill Usage
```json
{
  "skills": {
    "skill-name": {
      "count": 5,
      "success_rate": 0.8,
      "avg_duration_ms": 1234,
      "sessions": ["session-id"]
    }
  }
}
```

### Archive Metadata
```json
{
  "session_id": "abc123",
  "message_count": 47,
  "tool_calls": 23,
  "skills_used": ["skill1", "skill2"],
  "files_modified": ["/path/to/file.py"]
}
```

---

## Performance Targets

- PostToolUse: <1s ✅
- Stop: <5s ✅
- SubagentStop: <3s ✅
- Total: <10s ✅

---

## Documentation

- **README.md** - Complete user guide
- **HOOK-IMPLEMENTATION-SUMMARY.md** - Implementation details
- **docs/HOOK-SYSTEM-ARCHITECTURE.md** - Technical spec

---

**Version:** 1.0.0
**Date:** 2025-11-10
