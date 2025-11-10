# Hook System - Design Decisions & Trade-offs

This document outlines key architectural decisions and their trade-offs for review.

---

## Decision 1: Storage Location

### Options

| Option | Pros | Cons | Recommendation |
|--------|------|------|----------------|
| **A: `.claude-state/logs/`** | ✓ Already used for state<br>✓ Consistent with harness<br>✓ Easy to find | ✗ Not in `.gitignore` yet | **✓ RECOMMENDED** |
| B: `~/.claude/logs/` | ✓ Global across projects<br>✓ Automatic cleanup | ✗ Harder to access<br>✗ Lost project context | |
| C: `.claude/logs/` | ✓ Close to hooks<br>✓ Project-local | ✗ Inconsistent with state<br>✗ May be committed | |

**Decision:** Option A - `.claude-state/logs/`

**Rationale:**
- Consistency with existing state management
- Project-local for context preservation
- Easy to back up with project
- Already in `.gitignore` pattern

**Action Required:** Add `.claude-state/` to `.gitignore` if not present

---

## Decision 2: File Locking Strategy

### Options

| Option | Pros | Cons | Recommendation |
|--------|------|------|----------------|
| **A: fcntl with timeout** | ✓ POSIX standard<br>✓ Fast<br>✓ Reliable | ✗ Unix/Linux only | **✓ RECOMMENDED** |
| B: File-based locks | ✓ Cross-platform<br>✓ Simple | ✗ Stale locks possible<br>✗ Race conditions | |
| C: No locking | ✓ Fastest<br>✓ Simple | ✗ Corruption risk<br>✗ Data loss | |

**Decision:** Option A - fcntl with 1-second timeout

**Rationale:**
- Claude Code targets Unix/Linux/macOS
- Proven reliability
- Fast performance
- Built-in timeout prevents deadlocks

**Fallback:** If lock fails after 3 retries, skip write and log error

---

## Decision 3: Skill Tracking Granularity

### Options

| Option | Pros | Cons | Recommendation |
|--------|------|------|----------------|
| **A: Last 100 invocations** | ✓ Detailed history<br>✓ Trend analysis<br>✓ ~100KB max | ✗ Larger file size | **✓ RECOMMENDED** |
| B: Aggregate counts only | ✓ Tiny file size<br>✓ Fast writes | ✗ No history<br>✗ Limited insights | |
| C: All invocations | ✓ Complete history | ✗ Unbounded growth<br>✗ Performance issues | |

**Decision:** Option A - Last 100 invocations per skill with aggregate stats

**Rationale:**
- Provides detailed recent history
- Bounded storage (100 * 50 skills * 200 bytes = ~1MB)
- Enables trend analysis
- Fast enough (<1s to process)

**Circular Buffer:** Old invocations dropped when limit reached

---

## Decision 4: Conversation Archive Format

### Options

| Option | Pros | Cons | Recommendation |
|--------|------|------|----------------|
| **A: JSONL + metadata** | ✓ Native format<br>✓ Parseable<br>✓ Metadata separate | ✗ Two files per session | **✓ RECOMMENDED** |
| B: Single JSON file | ✓ One file<br>✓ Simple | ✗ Large files<br>✗ Slow to parse | |
| C: Compressed archive | ✓ Small size | ✗ Can't append<br>✗ Slow access | |

**Decision:** Option A - JSONL transcript + separate metadata JSON

**Rationale:**
- Native format from Claude Code (no conversion)
- Metadata enables fast search without parsing transcript
- Can append incrementally (future enhancement)
- Compression can be added later for old archives

**Future Enhancement:** Gzip archives older than 1 month

---

## Decision 5: Sensitive Data Handling

### Options

| Option | Pros | Cons | Recommendation |
|--------|------|------|----------------|
| **A: Sanitize before archive** | ✓ Safe storage<br>✓ Automatic<br>✓ No user action needed | ✗ Data loss<br>✗ False positives possible | **✓ RECOMMENDED** |
| B: Separate sanitized copies | ✓ Original preserved<br>✓ Reversible | ✗ 2x storage<br>✗ Complexity | |
| C: Encrypt instead | ✓ Data preserved<br>✓ Secure | ✗ Key management<br>✗ Complexity | |
| D: No sanitization | ✓ Simple<br>✓ Fast | ✗ Security risk<br>✗ Compliance issues | |

**Decision:** Option A - Sanitize before archiving with opt-out

**Rationale:**
- Security by default
- No key management burden
- Acceptable data loss (logged values, not code)
- Can opt-out via settings.json

**Configuration:**
```json
{
  "logging": {
    "conversation_archiving": {
      "sanitize_sensitive_data": true  // Set to false to disable
    }
  }
}
```

**Patterns Detected:**
- API keys (multiple formats)
- Passwords
- Bearer tokens
- Email addresses
- SSH private keys
- AWS access keys

---

## Decision 6: Index Generation Strategy

### Options

| Option | Pros | Cons | Recommendation |
|--------|------|------|----------------|
| **A: Incremental on-write** | ✓ Always current<br>✓ Fast reads | ✗ Slower writes<br>✗ Lock contention | **✓ RECOMMENDED** |
| B: Periodic rebuild | ✓ Fast writes<br>✓ No lock contention | ✗ Stale indexes<br>✗ Scheduled task needed | |
| C: On-demand generation | ✓ Zero overhead<br>✓ Always accurate | ✗ Slow searches<br>✗ User-initiated | |

**Decision:** Option A - Incremental update on every write

**Rationale:**
- Indexes always current
- Fast search queries
- Write overhead acceptable (<2s)
- No background tasks needed

**Optimization:** Batch index updates with skill tracking flushes

---

## Decision 7: Error Handling Philosophy

### Options

| Option | Pros | Cons | Recommendation |
|--------|------|------|----------------|
| **A: Always continue (exit 0)** | ✓ Never blocks Claude<br>✓ Graceful degradation<br>✓ Reliable | ✗ Silent failures possible | **✓ RECOMMENDED** |
| B: Fail on critical errors | ✓ Alerts user<br>✓ Prevents corruption | ✗ Interrupts workflow<br>✗ User intervention | |
| C: Retry indefinitely | ✓ Eventually succeeds | ✗ Hangs/timeouts<br>✗ Poor UX | |

**Decision:** Option A - Always return success, log errors

**Rationale:**
- Hook system is observability, not critical path
- User workflow more important than logging
- Errors logged for debugging
- Next invocation can recover

**Error Log Location:** `.claude-state/logs/hook-errors.log`

---

## Decision 8: Performance Budget Allocation

### Options

| Option | Total Budget | Per Hook Max | Trade-off |
|--------|--------------|--------------|-----------|
| **A: 10 seconds total** | 10s | PostToolUse: 1s<br>Stop: 5s<br>SubagentStop: 3s | ✓ Responsive<br>✗ Less processing | **✓ RECOMMENDED** |
| B: 30 seconds total | 30s | 10s each | ✓ More processing<br>✗ Slower UX | |
| C: 5 seconds total | 5s | 2s each | ✓ Very fast<br>✗ Limited features | |

**Decision:** Option A - 10 seconds total budget

**Rationale:**
- User barely notices <10s overhead
- Enough time for comprehensive logging
- Room for future enhancements
- Conservative estimate (actual ~3-5s)

**Breakdown:**
- Skill tracking: <1s (batched, async)
- Incremental prompt log: <0.5s (append-only)
- Session finalization: <5s (copy + metadata + index)
- Subagent archiving: <3s (copy + metadata)

---

## Decision 9: Subagent Log Organization

### Options

| Option | Structure | Pros | Cons | Recommendation |
|--------|-----------|------|------|----------------|
| **A: By agent type + date** | `subagent/{type}/YYYY-MM/` | ✓ Organized by role<br>✓ Easy to analyze<br>✓ Clear hierarchy | ✗ More directories | **✓ RECOMMENDED** |
| B: Flat date structure | `subagent/YYYY-MM/` | ✓ Simple<br>✓ Chronological | ✗ Mixed agent types<br>✗ Hard to filter | |
| C: By parent session | `subagent/{session_id}/` | ✓ Clear parent-child<br>✓ Co-located | ✗ Hard to browse<br>✗ Deep nesting | |

**Decision:** Option A - Organize by agent type, then date

**Rationale:**
- Easy to analyze agent-specific patterns
- Clear separation of concerns
- Metadata links to parent session
- Matches agent architecture

**Structure:**
```
subagent/
├── architect/2025-01/
├── engineer/2025-01/
├── tester/2025-01/
├── reviewer/2025-01/
└── orchestrator/2025-01/
```

**Linking:** Each subagent metadata includes `parent_session_id` field

---

## Decision 10: Batch Size for Skill Tracking

### Options

| Option | Batch Size | Flush Frequency | Pros | Cons | Recommendation |
|--------|-----------|-----------------|------|------|----------------|
| **A: 10 invocations** | 10 | ~2 min (typical) | ✓ Balanced<br>✓ Low overhead<br>✓ Recent data | ✗ Small lag | **✓ RECOMMENDED** |
| B: 1 invocation | 1 | Immediate | ✓ Real-time<br>✓ No data loss | ✗ High overhead<br>✗ Lock contention | |
| C: 50 invocations | 50 | ~10 min | ✓ Lowest overhead<br>✓ Best performance | ✗ Stale data<br>✗ Data loss risk | |

**Decision:** Option A - Batch size of 10

**Rationale:**
- Good balance between performance and freshness
- Typical session: 20-50 skill invocations
- 2-3 flushes per session
- Data loss risk: max 10 invocations if crash
- Low lock contention

**Force Flush:** On Stop hook to ensure no data loss

---

## Decision 11: Test Coverage Requirements

### Options

| Option | Coverage | Test Types | Effort | Recommendation |
|--------|----------|------------|--------|----------------|
| **A: >90% with integration** | >90% | Unit + Integration + Performance + Security | High | **✓ RECOMMENDED** |
| B: >70% unit only | >70% | Unit tests only | Medium | |
| C: >50% basic | >50% | Basic unit tests | Low | |

**Decision:** Option A - >90% coverage with comprehensive testing

**Rationale:**
- Critical infrastructure component
- Error resilience requires thorough testing
- Performance guarantees need validation
- Security must be verified

**Test Categories:**
- Unit tests: All library functions
- Integration tests: Full hook workflows
- Performance tests: Timing requirements
- Security tests: Sanitization patterns
- Manual tests: Real-world scenarios

---

## Decision 12: Retention Policy

### Options

| Option | Main Sessions | Subagent | Skill Usage | Total Size (6mo) |
|--------|---------------|----------|-------------|------------------|
| **A: 6 months** | 6 months | 6 months | Forever | ~6MB | **✓ RECOMMENDED** |
| B: 3 months | 3 months | 3 months | Forever | ~3MB | |
| C: Forever | Forever | Forever | Forever | ~50MB/year | |
| D: 1 month | 1 month | 1 month | Forever | ~1MB | |

**Decision:** Option A - 6 months for conversations, forever for skill usage

**Rationale:**
- 6 months covers most review/audit needs
- Skill usage data small enough to keep forever
- ~6MB total is negligible
- Easy to extend if needed

**Cleanup:** Automatic monthly job to remove old archives

**Configuration:**
```json
{
  "logging": {
    "conversation_archiving": {
      "retention_months": 6  // Configurable
    }
  }
}
```

---

## Summary of Recommendations

| Decision | Recommended Option | Impact | Risk |
|----------|-------------------|--------|------|
| 1. Storage Location | `.claude-state/logs/` | Low | Low |
| 2. File Locking | fcntl with timeout | Medium | Low |
| 3. Skill Granularity | Last 100 invocations | Low | Low |
| 4. Archive Format | JSONL + metadata | Low | Low |
| 5. Sensitive Data | Sanitize before archive | Medium | Low |
| 6. Index Strategy | Incremental on-write | Medium | Low |
| 7. Error Handling | Always continue | Low | Low |
| 8. Performance Budget | 10 seconds total | Medium | Low |
| 9. Subagent Organization | By agent type + date | Low | Low |
| 10. Batch Size | 10 invocations | Low | Low |
| 11. Test Coverage | >90% comprehensive | High | Low |
| 12. Retention Policy | 6 months | Low | Low |

**Overall Risk Level:** LOW
**Implementation Complexity:** MEDIUM
**Expected Value:** HIGH

---

## Open Questions for User

Please review and approve or modify:

### 1. Retention Period
- **Recommended:** 6 months for conversations
- **Alternatives:** 3 months (smaller), 12 months (longer history)
- **Your preference:** ___________

### 2. Sanitization
- **Recommended:** Enabled by default with opt-out
- **Alternatives:** Disabled by default, Manual trigger only
- **Your preference:** ___________

### 3. Performance Budget
- **Recommended:** <10 seconds per hook
- **Alternatives:** <5 seconds (less features), <30 seconds (more processing)
- **Your preference:** ___________

### 4. Compression
- **Recommended:** Not initially, add later for old archives
- **Alternatives:** Compress immediately, Never compress
- **Your preference:** ___________

### 5. Batch Size
- **Recommended:** 10 invocations
- **Alternatives:** 1 (real-time), 5 (more frequent), 20 (less frequent)
- **Your preference:** ___________

---

## Approval Checklist

- [ ] Storage location approved
- [ ] File locking strategy acceptable
- [ ] Skill tracking granularity OK
- [ ] Archive format acceptable
- [ ] Sensitive data handling approved
- [ ] Index strategy OK
- [ ] Error handling philosophy acceptable
- [ ] Performance budget reasonable
- [ ] Subagent organization clear
- [ ] Batch size appropriate
- [ ] Test coverage adequate
- [ ] Retention policy acceptable

**Approved by:** ___________
**Date:** ___________
**Notes:** ___________

---

## Next Steps After Approval

1. Confirm all design decisions
2. Begin Phase 1 implementation (Foundation)
3. Regular progress updates
4. Demo after Phase 2 (Skill Tracking working)
5. Full review after Phase 3 (Conversation Archiving)
6. Final testing and deployment

---

**Created:** 2025-01-10
**Status:** Awaiting Approval
**Version:** 1.0
