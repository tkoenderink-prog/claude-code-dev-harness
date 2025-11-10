# Skills Transformation Implementation Plan

**Date:** 2025-11-10
**User Decisions:**
- Q1: Build comprehensive security skills with subagent research (A+)
- Q2: 2-3 focused architecture skills (B)
- Q3: Complete all phases (A - 28 hours)
- Q4: No subcategories, flat structure (A)
- Q5: Rename "personal" → "physical" (B)

---

## Phase 1: Cleanup (4-6 hours)

### Task 1.1: Remove 78 Template Skills
Extract list from evaluation JSONs and remove directories.

### Task 1.2: Fix 9 Miscategorizations
Move skills to correct logical categories:
1. vault-weekly-review: Code Review → Obsidian/PKM
2. brainstorming: Database → Thinking/Planning
3. context-aware-reasoning: Deployment → Thinking/Planning
4. collision-zone-thinking: Deployment → Thinking/Planning
5. domain-specific-application: Deployment → Thinking/Planning
6. inversion-exercise: Deployment → Thinking/Planning
7. meta-pattern-recognition: Deployment → Thinking/Planning
8. (2 more from analysis)

### Task 1.3: Add 16 Missing Triggers
Add "when_to_use" sections to:
- brainstorming
- defense-in-depth
- dispatching-parallel-agents
- executing-plans
- finishing-a-development-branch
- fixing-claude-code-hooks
- receiving-code-review
- requesting-code-review
- vault-operations
- (7 more from evaluations)

### Task 1.4: Update CLAUDE.md
Reflect new 56-skill structure and organization.

---

## Phase 2: Critical Expansions (8-12 hours)

### Task 2.1: Security Skills (8-12h) - WITH SUBAGENT RESEARCH
**Research Topics:**
- OWASP Top 10 (2024 edition)
- Secure coding standards (CERT, CWE)
- Modern security practices (Zero Trust, defense in depth)
- Practical implementation patterns

**Skills to Create:**
1. `dev-security-fundamentals` - OWASP Top 10, auth/authz, input validation
2. `dev-secrets-management` - API keys, credentials, encryption at rest/transit
3. `dev-secure-coding` - XSS, SQL injection, CSRF prevention, common vulnerabilities

**Approach:** Launch 3 parallel research agents, each builds one comprehensive skill.

### Task 2.2: Architecture Skills (4-6h)
**Skills to Expand:**
1. `dev-system-design` - From template to comprehensive (scalability, patterns, tradeoffs)
2. `dev-scalability-patterns` - Horizontal/vertical scaling, caching, load balancing

### Task 2.3: Database Skills (2-3h)
**Skills to Expand:**
1. `dev-query-optimization` - Indexes, execution plans, N+1 queries

### Task 2.4: Testing Skills (2-3h)
**Skills to Expand:**
1. `dev-integration-testing` - Test strategies, mocking, fixtures
2. `dev-test-strategy` - When to use which test type

### Task 2.5: Claude Code Skills (2-3h)
**Skills to Create:**
1. `cc-agent-patterns` - Multi-agent coordination
2. `cc-workflow-optimization` - Autonomous operation patterns

---

## Phase 3: Prefix Implementation (3-4 hours)

### Task 3.1: Rename All Skills
Apply prefix scheme:
- Software Dev: `dev-` (28 skills)
- Thinking/Planning: `think-` (12 skills)
- Claude Code: `cc-` (10 skills after expansions)
- Obsidian/PKM: `vault-` (10 skills)
- Physical Training: `physical-` (5 skills)

### Task 3.2: Update Cross-References
Find and update all skill references in:
- Skill files (See Also sections)
- CLAUDE.md
- Agent prompts
- Hook files

### Task 3.3: Test Invocations
Verify skills can be invoked with new names.

---

## Phase 4: Polish & Optimization (4-6 hours)

### Task 4.1: Improve 8 Good/Adequate Skills
Add examples, reduce verbosity, clarify:
- brainstorming
- defense-in-depth
- dispatching-parallel-agents
- finishing-a-development-branch
- collision-zone-thinking
- remembering-conversations
- requesting-code-review
- pulling-updates-from-skills-repository

### Task 4.2: Create Quick-Reference Guides
For 3 longest skills (1000+ lines):
- understanding-with-frameworks (1,084 lines)
- fixing-claude-code-hooks (649 lines)
- writing-skills (623 lines)

### Task 4.3: Final Documentation
- Update skills README
- Document category boundaries
- Create category-level README files

---

## Success Metrics

**Before:**
- 135 skills (58% templates)
- Average score: 40.2/100
- Cognitive load: High

**After:**
- 70-75 skills (100% quality)
- Average score: 85+/100
- Cognitive load: Reduced 58%
- Perfect 5-category organization

---

## Execution Order

1. ✅ Get user decisions (DONE)
2. Phase 1: Cleanup (execute now)
3. Phase 2: Expansions (security with subagents, then others)
4. Phase 3: Prefixes
5. Phase 4: Polish
6. Commit incrementally
7. Final review

---

**Status:** Ready to execute
**Next:** Begin Phase 1 - Cleanup
