# Hook System for Claude Code - Complete Package

## Overview

This package contains the complete technical design for a comprehensive hook system that adds **skill usage tracking** and **conversation archiving** to Claude Code.

## What's Included

### 1. Architecture Document
**File:** `HOOK-SYSTEM-ARCHITECTURE.md` (60+ pages)

Complete technical specification including:
- System architecture and component design
- Complete directory structure
- Data schemas for all JSON files
- Hook specifications (PostToolUse, SubagentStop, etc.)
- Settings.json configuration
- Error handling strategy
- Performance optimization techniques
- Security considerations
- Testing strategy (unit, integration, performance)
- 3-week implementation plan

**Status:** Ready for implementation

### 2. Implementation Guide
**File:** `HOOK-IMPLEMENTATION-GUIDE.md`

Quick reference for engineers with:
- Step-by-step implementation order
- Code examples for all components
- Testing checklist
- Performance checklist
- Security checklist
- Common issues and solutions
- Estimated 8-day implementation timeline

**Status:** Ready to use

### 3. Visual Diagrams
**File:** `HOOK-SYSTEM-DIAGRAMS.md`

ASCII diagrams showing:
- System overview with all layers
- Skill tracking flow
- Conversation archiving flow
- Subagent archiving flow
- File locking mechanism
- Error handling flow
- Data flow summary
- Performance optimization layers
- Security layers

**Status:** Ready for reference

## Features

### Skill Usage Tracking
- Track every Skill tool invocation via PostToolUse hook
- Store in `.claude-state/logs/skill-usage.json`
- Includes: skill name, count, timestamps, session correlation
- Batch writes for performance (10x batching)
- Searchable index generation

### Conversation Archiving
- Main session logs in `.claude-state/logs/main-session/YYYY-MM/`
- Subagent logs in `.claude-state/logs/subagent/{agent-type}/YYYY-MM/`
- Triggered by SessionEnd, UserPromptSubmit, SubagentStop hooks
- Organized by date with metadata files
- Searchable global index

### Performance
- <1s for skill tracking
- <5s for session archiving
- <3s for subagent archiving
- <10s total for any hook
- Non-blocking operations
- Batch writes and caching

### Error Resilience
- Never crashes Claude Code (always exit 0)
- Graceful degradation on errors
- Silent error logging
- Auto-recovery on next invocation
- File locking with timeout and retry

### Security
- Sanitizes sensitive data (API keys, passwords, tokens, emails)
- File permissions: 0700 for directories, 0600 for data files
- Audit logging for security events
- No network access from hooks

## Quick Start

### For Engineers

1. **Read the implementation guide first:**
   ```bash
   cat docs/HOOK-IMPLEMENTATION-GUIDE.md
   ```

2. **Follow the phase-by-phase implementation:**
   - Phase 1: Foundation (Day 1-2)
   - Phase 2: Skill Tracking (Day 3-4)
   - Phase 3: Conversation Archiving (Day 5-6)
   - Phase 4: Subagent Archiving (Day 7)
   - Phase 5: Update Settings (Day 8)

3. **Refer to diagrams for visual understanding:**
   ```bash
   cat docs/HOOK-SYSTEM-DIAGRAMS.md
   ```

4. **Use architecture doc for detailed specifications:**
   ```bash
   cat docs/HOOK-SYSTEM-ARCHITECTURE.md
   ```

### For Architects/Reviewers

1. **Review the architecture document:**
   - System design and trade-offs
   - Data schemas and formats
   - Performance budgets
   - Security considerations

2. **Validate the design:**
   - Check against requirements
   - Verify performance targets
   - Review security measures
   - Assess implementation complexity

3. **Provide feedback:**
   - Identify missing requirements
   - Suggest improvements
   - Highlight risks

## Directory Structure Preview

```
.claude-state/logs/
├── skill-usage.json              # Aggregate skill tracking
├── skill-usage-index.json        # Search index
├── archive-index.json            # Global archive index
├── hook-errors.log               # Error logging
├── main-session/
│   └── 2025-01/
│       ├── 2025-01-10_14-30-00_abc123.jsonl
│       └── 2025-01-10_14-30-00_abc123.meta.json
└── subagent/
    ├── architect/2025-01/
    ├── engineer/2025-01/
    ├── tester/2025-01/
    └── reviewer/2025-01/

.claude/hooks/
├── lib/
│   ├── skill_tracker.py
│   ├── conversation_archiver.py
│   ├── sanitizer.py
│   ├── indexer.py
│   └── common.py
├── session-start                 # Existing (unchanged)
├── user-prompt-submit            # Existing (minor update)
├── stop                          # Existing (major update)
├── post-tool-use                 # NEW
└── subagent-stop                 # NEW
```

## Key Metrics

### Performance Budget
| Operation | Max Time | Strategy |
|-----------|----------|----------|
| Skill tracking | 1s | Batch + async |
| Session archiving | 5s | Copy + index |
| Subagent archiving | 3s | Copy + metadata |
| Total hook time | <10s | Non-blocking |

### Storage Budget
| Component | Size Estimate | Retention |
|-----------|---------------|-----------|
| skill-usage.json | ~100KB | Forever |
| main-session/ | ~1MB/month | 6 months |
| subagent/ | ~500KB/month | 6 months |
| indexes | ~50KB | Forever |

### Quality Metrics
- Error resilience: 100% (never crash)
- Test coverage: >90%
- Security audit: Pass
- Performance: <10s per hook
- Documentation: Complete

## Technology Stack

- **Language:** Python 3.9+
- **Dependencies:** None (standard library only)
- **File Locking:** fcntl (POSIX)
- **JSON:** Standard json module
- **Permissions:** chmod/stat (POSIX)
- **Compression:** gzip (future enhancement)

## Configuration

### settings.json Changes

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
    "SubagentStop": [
      {
        "type": "command",
        "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/subagent-stop"
      }
    ]
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
      "sanitize_sensitive_data": true
    }
  }
}
```

## Testing

### Unit Tests
```bash
pytest tests/test_skill_tracker.py -v
pytest tests/test_conversation_archiver.py -v
pytest tests/test_sanitizer.py -v
pytest tests/test_common.py -v
```

### Integration Tests
```bash
pytest tests/test_hooks_integration.py -v
```

### Performance Tests
```bash
pytest tests/test_performance.py -v
```

### Manual Testing
```bash
./tests/manual/test-hooks-manually.sh
```

## Security

### Sensitive Data Patterns Detected
- API keys (various formats)
- Passwords and credentials
- Bearer tokens and auth tokens
- Email addresses
- SSH private keys
- AWS access keys

### Sanitization Strategy
All detected patterns replaced with `***REDACTED***` or `***EMAIL***` etc.

### File Permissions
- Directories: `0700` (owner only)
- Data files: `0600` (owner read/write only)
- Hook scripts: `0700` (owner execute only)

### Audit Trail
All security events logged to `security-audit.log` with 90-day retention.

## Troubleshooting

### Common Issues

**Issue:** "Permission denied" on hook execution
**Solution:** `chmod +x .claude/hooks/post-tool-use`

**Issue:** "Module not found: skill_tracker"
**Solution:** Ensure `.claude/hooks/lib/` exists and contains `__init__.py`

**Issue:** File lock timeout
**Solution:** Check for zombie processes, increase timeout

**Issue:** Skill tracking not working
**Debug:**
```bash
# Check configuration
cat .claude/settings.json | jq .hooks.PostToolUse

# Test hook manually
echo '{"tool_name":"Skill","tool_input":{"skill_name":"test"}}' | \
  .claude/hooks/post-tool-use | jq

# Check error log
tail -f .claude-state/logs/hook-errors.log
```

## Implementation Timeline

| Phase | Duration | Deliverables |
|-------|----------|--------------|
| Phase 1: Foundation | 2 days | Directory structure, lib/common.py, lib/sanitizer.py |
| Phase 2: Skill Tracking | 2 days | lib/skill_tracker.py, post-tool-use hook |
| Phase 3: Conversation Archiving | 2 days | lib/conversation_archiver.py, updated stop hook |
| Phase 4: Subagent Archiving | 1 day | subagent-stop hook |
| Phase 5: Settings Update | 1 day | Updated settings.json, documentation |
| **Total** | **8 days** | Complete working system |

## Next Steps

### For Immediate Implementation

1. **Day 1-2:** Implement foundation
   - Create directory structure
   - Implement `lib/common.py` with file locking
   - Implement `lib/sanitizer.py`
   - Write unit tests

2. **Day 3-4:** Implement skill tracking
   - Implement `lib/skill_tracker.py`
   - Create `post-tool-use` hook
   - Add to settings.json
   - Test thoroughly

3. **Day 5-6:** Implement conversation archiving
   - Implement `lib/conversation_archiver.py`
   - Update `stop` hook
   - Test archiving workflow

4. **Day 7:** Implement subagent archiving
   - Create `subagent-stop` hook
   - Test with Task tool
   - Verify parent-child linking

5. **Day 8:** Finalize and document
   - Update settings.json
   - Write user documentation
   - Create migration guide
   - Final testing

### For Future Enhancements

- **Compression:** Gzip archives older than 1 month
- **Search UI:** Web interface for searching archives
- **Analytics:** Dashboards for skill usage trends
- **Notifications:** Slack/email on session completion
- **Cleanup:** Automated archive pruning
- **Export:** Export to external systems (S3, etc.)

## Questions for User

Before starting implementation, please confirm:

1. **Retention Period:** 6 months OK for conversation archives?
2. **Compression:** Should we compress old archives (gzip)?
3. **Sanitization:** Are the sensitive patterns comprehensive enough?
4. **Skill Priority:** Any specific skills to track differently?
5. **Storage Location:** `.claude-state/logs/` acceptable?

## Support

For questions or issues:
1. Check troubleshooting section above
2. Review architecture document for detailed specs
3. Consult diagrams for visual understanding
4. Check error logs for debugging

## License

Part of Claude Code v2 Professional Autonomy Harness

---

## Document Status

- **Architecture:** Complete and ready for implementation
- **Implementation Guide:** Complete with code examples
- **Diagrams:** Complete with all flows documented
- **Testing Strategy:** Complete with test cases
- **Security Review:** Complete with measures defined

**Next Action:** Begin Phase 1 implementation

---

**Created:** 2025-01-10
**Last Updated:** 2025-01-10
**Version:** 1.0
**Status:** Ready for Implementation
