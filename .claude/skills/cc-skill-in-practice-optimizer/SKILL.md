# Skill-In-Practice Optimizer v1.0

**Purpose:** Analyze real usage data to optimize skills based on actual agent behavior patterns

**Category:** Claude Code Meta-Skills (cc-)

**When to use:** After a skill has been used ≥25 times OR when usage patterns suggest inefficiencies

---

## Quick Start (5-Minute Overview)

### 30-Second Summary

This skill analyzes how AI agents actually use a specific skill in production, identifies patterns of confusion or inefficiency, and presents three optimization options (minimal/medium/maximum) with clear tradeoffs. Uses real log data + best practices + evaluation scoring to generate actionable improvements.

### Key Inputs

| Input | Default | Description |
|-------|---------|-------------|
| **Skill name** | Required | E.g., `skill-evaluator` or `dev-test-driven-development` |
| **Usage count** | 25 | Number of recent invocations to analyze |
| **Log location** | `.claude-state/logs/` | Where to find usage logs |

### Key Outputs

| Output | Description |
|--------|-------------|
| **Comprehensive analysis report** | Usage patterns, inefficiencies, quality assessment |
| **3 optimization options** | Minimal (quick wins), Medium (targeted improvements), Maximum (full redesign) |
| **HITL decision checkpoint** | User chooses which option to implement |
| **Implementation artifacts** | Updated skill + supporting docs |

### The 5 Phases (30-45 minutes total)

| Phase | Activity | Time | Output |
|-------|----------|------|--------|
| **1. Collect** | Analyze logs for usage patterns | 5-8 min | Usage statistics, tool call patterns |
| **2. Evaluate** | Apply skill-evaluator framework | 10-15 min | 0-100 score with dimensional breakdown |
| **3. Analyze** | Find struggle patterns in logs | 10-15 min | Confusion points, inefficiencies, anti-patterns |
| **4. Synthesize** | Generate optimization recommendations | 10-12 min | 3 tiered options with effort/impact estimates |
| **5. HITL** | Present options, get user decision | Variable | User-selected optimization path |

### Decision Tree

```
Start → Has skill been used ≥25 times?
        ├─ NO → Skip optimization (insufficient data)
        └─ YES → Are there known issues?
                 ├─ YES (error rate >10%, complaints) → Run FULL analysis
                 └─ NO → Quick scan first
                         ├─ No issues found → Document and exit
                         └─ Issues found → Run FULL analysis

FULL Analysis → 5 Phases → HITL → Implement chosen option
```

---

## Detailed Process

### Phase 1: Collect Usage Data (5-8 minutes)

#### Objectives
- Gather quantitative usage metrics
- Identify tool call patterns
- Detect re-read behaviors
- Calculate efficiency baselines

#### Steps

**1.1 Locate Usage Logs**

```bash
# Find all logs mentioning the skill
find .claude-state/logs/ -name "*.jsonl" -type f | \
  xargs grep -l "skill-name" | \
  sort -r | \
  head -n [usage_count]
```

**Checklist:**
- [ ] Logs found for target skill
- [ ] At least [usage_count] invocations available
- [ ] Logs are JSONL format (one JSON object per line)
- [ ] Logs contain tool_use and tool_result blocks

**If insufficient logs:** Reduce usage_count to available data or skip optimization

---

**1.2 Parse Tool Call Sequences**

For each skill invocation, extract:
- Read operations (skill file reads)
- Grep operations (searches within skill)
- Edit/Write operations (output generation)
- Timestamps (to calculate duration)

**Data to collect:**

| Metric | Calculation | Baseline Target |
|--------|-------------|-----------------|
| **Reads per invocation** | Count Read(skill.md) calls | ≤1.5 (≤1 for batch skills) |
| **Tools per invocation** | Total tool calls / invocations | ≤3.3 |
| **Re-read pattern** | Reads > 1 in single session | 0% (no re-reads) |
| **Duration** | Timestamp_end - Timestamp_start | Varies by skill |
| **Error rate** | Errors / total invocations | <5% |

**Script template:**

```python
# analyze_skill_usage.py
import json
import sys
from collections import defaultdict

skill_name = sys.argv[1]
log_files = sys.argv[2:]

stats = {
    'total_invocations': 0,
    'total_reads': 0,
    'total_tools': 0,
    're_reads': 0,
    'errors': 0,
    'durations': []
}

for log_file in log_files:
    # Parse JSONL, extract tool calls, accumulate stats
    # [Implementation details]

print(f"Average reads per invocation: {stats['total_reads'] / stats['total_invocations']}")
print(f"Average tools per invocation: {stats['total_tools'] / stats['total_invocations']}")
print(f"Re-read rate: {stats['re_reads'] / stats['total_invocations'] * 100}%")
```

---

**1.3 Identify Usage Patterns**

**Common patterns to detect:**

✅ **Healthy Pattern:** Read skill once → Apply → Output
```
Session Start → Read(skill) → Read(data) → Process → Write(output)
Tools: 3, Duration: 5 min
```

⚠️ **Re-read Pattern:** Multiple reads in same session
```
Read(skill) → Process batch 1 → Read(skill) → Process batch 2 → Read(skill) → Process batch 3
Tools: 7, Duration: 15 min
ROOT CAUSE: No session caching instruction
```

❌ **Confusion Pattern:** Read → Grep → Read again
```
Read(skill) → Grep(skill, "criteria") → Read(skill, offset=200) → Grep again
Tools: 6, Duration: 8 min
ROOT CAUSE: Poor scanability, can't find info quickly
```

❌ **Retry Pattern:** Multiple attempts at same operation
```
Read(skill) → Try approach A → Error → Read(skill) → Try approach B → Success
Tools: 5, Duration: 12 min, Error rate: 50%
ROOT CAUSE: Ambiguous instructions or missing edge case handling
```

**Output:** Usage pattern summary

```markdown
## Usage Pattern Analysis

**Invocations analyzed:** [N]
**Date range:** [Start] to [End]

### Metrics
| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Reads per invocation | 2.8 | ≤1.5 | ⚠️ Above target |
| Tools per invocation | 4.2 | ≤3.3 | ⚠️ Above target |
| Re-read rate | 65% | 0% | ❌ High |
| Error rate | 12% | <5% | ❌ High |
| Avg duration | 8.5 min | Varies | - |

### Patterns Detected
- **Re-read pattern** (65% of sessions): Agents read skill 2-3 times per session
- **Confusion pattern** (23% of sessions): Grep followed by re-read
- **Retry pattern** (12% of sessions): Failed attempts before success
```

---

### Phase 2: Apply Skill Evaluator (10-15 minutes)

#### Objectives
- Obtain objective 0-100 quality score
- Identify dimension-specific weaknesses
- Get calibrated assessment against standards

#### Steps

**2.1 Read cc-skill-evaluator**

```markdown
Read: .claude/skills/cc-skill-evaluator/SKILL.md

**Session Note:** Cache this content - you'll reference it multiple times but should NOT re-read
```

**2.2 Read Target Skill**

```markdown
Read: .claude/skills/[skill-name]/SKILL.md
```

**2.3 Apply 5-Dimension Framework**

Use skill-evaluator's framework to score:

| Dimension | Focus | Score (0-20) | Justification |
|-----------|-------|--------------|---------------|
| **A. Functional** | Does it work reliably? | __ | [Evidence from skill content] |
| **B. Clarity** | Easy to understand? | __ | [Evidence from skill content] |
| **C. Modularity** | Focused, reusable? | __ | [Evidence from skill content] |
| **D. Performance** | Efficient execution? | __ | [Evidence from skill content] |
| **E. Domain** | Right depth/breadth? | __ | [Evidence from skill content] |
| **TOTAL** | **Sum** | **__/100** | **Rating:** [Exemplary/Strong/Good/etc] |

**Cross-reference with usage data:**
- Low Performance score + high re-read rate = corroborates cognitive load issue
- Low Clarity score + confusion patterns = corroborates scanability issue

**2.4 Document Evaluation**

```markdown
## Skill Evaluation Summary

**Skill:** [name]
**Score:** [X]/100 ([Rating])
**Evaluated:** [Date]

### Dimensional Scores
[Table from 2.3]

### Key Findings from Evaluation
**Strengths:**
- [Dimension with high score]: [Specific evidence]

**Weaknesses:**
- [Dimension with low score]: [Specific evidence]

### Alignment with Usage Data
- [Low dimension] correlates with [usage pattern]
- [Example: Low Performance (12/20) aligns with 65% re-read rate]
```

---

### Phase 3: Analyze Struggle Patterns (10-15 minutes)

#### Objectives
- Identify specific points of confusion in logs
- Quantify tool call inefficiencies
- Detect cognitive load indicators
- Find anti-patterns in agent behavior

#### Steps

**3.1 Sample Detailed Conversations**

Select 3-5 representative invocation logs:
- 1-2 "smooth" invocations (baseline)
- 2-3 "struggled" invocations (errors, re-reads, long duration)

**Criteria for "struggled" invocation:**
- Duration >150% of median
- Tool calls >5
- Errors or retries present
- Re-read patterns

**3.2 Analyze Struggle Points**

For each struggled invocation, identify:

**Where did agent get stuck?**
- Line number in skill where confusion occurred
- Section being referenced when error happened
- Question asked or clarification sought

**Why did agent struggle?**
- Ambiguous instruction ("evaluate appropriateness" - no definition)
- Missing information (no example for edge case)
- Buried content (key info at line 300, not in quick ref)
- Cognitive overload (12 criteria to hold simultaneously)

**What did agent do to recover?**
- Re-read skill (indicates scanability issue)
- Grep for specific term (indicates organization issue)
- Make assumption (indicates missing guidance)
- Ask for clarification (indicates ambiguity)

**3.3 Map to Skill Structure**

Create a "heat map" of problem areas:

```markdown
## Struggle Point Heat Map

| Skill Section | Lines | Struggle Events | Issue Type |
|---------------|-------|-----------------|------------|
| Process description | 124-160 | 8 re-reads | Buried too deep (line 124) |
| Scoring criteria | 25-122 | 12 grep attempts | Not scannable, walls of text |
| Output format | 162-234 | 3 errors | Comes before understanding, backwards |
| Calibration examples | 362-400 | 15 references | Redundant with earlier section |
```

**3.4 Calculate Inefficiency Metrics**

| Inefficiency Type | Occurrences | Cost per Instance | Total Cost |
|-------------------|-------------|-------------------|------------|
| **Re-reads** | 18 | 2,000 tokens | 36,000 tokens |
| **Unnecessary greps** | 12 | 500 tokens | 6,000 tokens |
| **Retry loops** | 5 | 1,500 tokens | 7,500 tokens |
| **Total waste** | 35 | - | 49,500 tokens |

**Optimization potential:** 49,500 tokens / session = $0.15 savings per session (at typical rates)

**3.5 Identify Root Causes**

Group struggle patterns by root cause:

**Cognitive Load Issues:**
- Skill too long (>500 lines)
- Too many items per section (>7 chunks)
- Redundant content (same info 3× places)

**Structural Issues:**
- Process buried deep in skill
- No quick reference for experienced users
- Linear structure (can't jump to relevant section)

**Clarity Issues:**
- Ambiguous terms ("appropriate", "sufficient")
- Missing definitions
- No decision criteria at key choice points

**Missing Content:**
- No edge case handling
- No error prevention guardrails
- No examples for key concepts

---

### Phase 4: Synthesize Findings (10-12 minutes)

#### Objectives
- Integrate evaluation scores + usage patterns + struggle analysis
- Identify highest-impact improvements
- Estimate effort for different optimization levels
- Prepare 3 tiered options for HITL

#### Steps

**4.1 Create Unified Findings Table**

| Finding | Evidence | Impact | Effort to Fix |
|---------|----------|--------|---------------|
| **High re-read rate (65%)** | Usage logs: 18/25 sessions | 23% efficiency loss | Low (add 5-line caching note) |
| **Poor scanability** | Evaluator: Clarity 12/20; Logs: 12 grep attempts | Confusion, slow lookups | Medium (add tables, headers) |
| **Process buried at line 124** | Struggle heat map: 8 re-reads of intro | Slow onboarding | Low (restructure, add Quick Start) |
| **Cognitive load (8/10)** | Evaluator: Performance 11/20; 530 lines | High mental effort | High (full v2 redesign) |
| **No bias prevention** | Missing in evaluation; Observed halo effect in 3 logs | Inconsistent outputs | Medium (add QA section) |

**4.2 Prioritize by ROI**

| Priority | Finding | Impact | Effort | ROI | Recommendation |
|----------|---------|--------|--------|-----|----------------|
| 🔥 **P0** | High re-read rate | High | Low | ⭐⭐⭐⭐⭐ | **MINIMAL** |
| 🔥 **P0** | Process buried | High | Low | ⭐⭐⭐⭐⭐ | **MINIMAL** |
| 📊 **P1** | Poor scanability | High | Medium | ⭐⭐⭐⭐ | **MEDIUM** |
| 📊 **P1** | No bias prevention | Medium | Medium | ⭐⭐⭐ | **MEDIUM** |
| ⚡ **P2** | High cognitive load | High | High | ⭐⭐⭐ | **MAXIMUM** |

**4.3 Design 3 Optimization Tiers**

#### Tier 1: Minimal (Quick Wins)

**Scope:** Fix highest-ROI issues with <2 hours effort
**Target:** 40-50% efficiency improvement

| Change | Effort | Impact |
|--------|--------|--------|
| Add session caching instruction | 5 min | 23% efficiency gain |
| Add Quick Start section | 1 hour | 6× faster onboarding |
| Move process to line 20 | 30 min | Immediate access to steps |
| Fix rating label boundaries | 15 min | Improved clarity |

**Total:** 1.5-2 hours
**Expected Result:** Reads per session: 2.8 → 1.0, Tools: 4.2 → 3.1

---

#### Tier 2: Medium (Targeted Improvements)

**Scope:** Minimal + structural enhancements
**Target:** 60-70% efficiency improvement

**Additional changes:**

| Change | Effort | Impact |
|--------|--------|--------|
| Create scorecard template | 1 hour | 50% memory load reduction |
| Add bias prevention section | 1.5 hours | 30% consistency improvement |
| Convert prose to tables | 1 hour | Improved scanability |
| Add navigation (TOC, links) | 30 min | Faster reference |

**Total:** 4-6 hours (including Tier 1)
**Expected Result:** Reads: 1.0, Tools: 2.8, Error rate: 12% → 5%

---

#### Tier 3: Maximum (Full Redesign)

**Scope:** Complete v2 overhaul
**Target:** 10× usability, 34% shorter, production-grade

**Additional changes:**

| Change | Effort | Impact |
|--------|--------|--------|
| Consolidate redundant sections | 1.5 hours | Remove 180 lines (34%) |
| Two-tier architecture (quick ref + detailed) | 2 hours | Expert path 8× faster |
| Visual aids (decision trees, flowcharts) | 1 hour | Improved comprehension |
| Comprehensive examples | 1.5 hours | Concrete guidance |
| Quality assurance section | 1 hour | Error prevention |

**Total:** 9-12 hours (including Tier 1 + 2)
**Expected Result:** Cognitive load: 8/10 → 4/10, Evaluator score: [current] → 90+/100

---

**4.4 Estimate Costs & Benefits**

| Tier | Effort | Efficiency Gain | Score Improvement | Time to ROI |
|------|--------|----------------|-------------------|-------------|
| **Minimal** | 1.5-2 hrs | 40-50% | +5-10 points | Immediate |
| **Medium** | 4-6 hrs | 60-70% | +10-15 points | After 10 uses |
| **Maximum** | 9-12 hrs | 10× usability | +15-25 points | After 25 uses |

---

### Phase 5: Present HITL Options (Variable time)

#### Objectives
- Present clear, actionable options to user
- Provide enough context for informed decision
- Get explicit user choice
- Proceed with implementation based on choice

#### HITL Presentation Template

```markdown
# Skill Optimization Analysis: [Skill Name]

**Date:** [Date]
**Analyzed:** [N] invocations from [date range]
**Current Score:** [X]/100 ([Rating])

---

## Executive Summary

**Current State:**
- Skill is [functional/struggling] with [specific issues]
- [Key metric 1]: [value] (target: [target])
- [Key metric 2]: [value] (target: [target])

**Root Causes Identified:**
1. [Root cause 1] → [Impact]
2. [Root cause 2] → [Impact]
3. [Root cause 3] → [Impact]

**Optimization Potential:** [X]% efficiency gain available

---

## Key Findings

### Usage Metrics
[Table from Phase 1.3]

### Evaluation Score
[Table from Phase 2.3]

### Top 3 Issues
1. **[Issue]** - [Evidence] - Impact: [High/Med/Low] - Effort: [Low/Med/High]
2. **[Issue]** - [Evidence] - Impact: [High/Med/Low] - Effort: [Low/Med/High]
3. **[Issue]** - [Evidence] - Impact: [High/Med/Low] - Effort: [Low/Med/High]

---

## Optimization Options

### Option 1: Minimal (Quick Wins) ⭐ **RECOMMENDED**

**Effort:** 1.5-2 hours
**Impact:** 40-50% efficiency improvement
**Risk:** Low (small, targeted changes)

**Changes:**
- ✅ [Change 1]: [Specific action] - [Expected result]
- ✅ [Change 2]: [Specific action] - [Expected result]
- ✅ [Change 3]: [Specific action] - [Expected result]

**Pros:**
- Immediate ROI (payback after 1-2 uses)
- Low risk of introducing new issues
- Quick implementation

**Cons:**
- Doesn't address all issues
- May need follow-up optimization later

**Before/After:**
| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Reads per session | 2.8 | 1.0 | 64% ↓ |
| Tools per invocation | 4.2 | 3.1 | 26% ↓ |
| Time per use | 8.5 min | 6.5 min | 24% ↓ |

---

### Option 2: Medium (Targeted Improvements)

**Effort:** 4-6 hours
**Impact:** 60-70% efficiency improvement
**Risk:** Low-Medium (more extensive changes)

**Changes:**
- All changes from Minimal, PLUS:
- ✅ [Additional change 1]
- ✅ [Additional change 2]
- ✅ [Additional change 3]

**Pros:**
- Addresses most major issues
- Balanced effort/impact
- Sets up for future enhancements

**Cons:**
- Moderate time investment
- Requires testing across multiple scenarios

**Before/After:**
| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Reads per session | 2.8 | 1.0 | 64% ↓ |
| Tools per invocation | 4.2 | 2.8 | 33% ↓ |
| Error rate | 12% | 5% | 58% ↓ |
| Cognitive load | 8/10 | 5/10 | 38% ↓ |

---

### Option 3: Maximum (Full Redesign)

**Effort:** 9-12 hours
**Impact:** 10× usability improvement
**Risk:** Medium (significant restructuring)

**Changes:**
- All changes from Minimal + Medium, PLUS:
- ✅ [Additional change 1]
- ✅ [Additional change 2]
- ✅ [Additional change 3]
- ✅ [Additional change 4]

**Pros:**
- Production-grade quality
- Exemplary rating potential (90+/100)
- Long-term solution

**Cons:**
- Significant time investment
- Requires comprehensive testing
- May need user re-training if structure changes significantly

**Before/After:**
| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Evaluator score | [X]/100 | 90+/100 | +[Y] points |
| Cognitive load | 8/10 | 4/10 | 50% ↓ |
| Length | 530 lines | 350+100 | 34% ↓ |
| Expert time to use | 15 min | 2 min | 87% ↓ |

---

## My Recommendation

**I recommend: [Option] because:**
1. [Specific reason based on context]
2. [Specific reason based on usage frequency]
3. [Specific reason based on current pain points]

**However, if [condition], then [different option] might be better:**
- [Scenario where different option makes sense]

---

## Decision Required

Which optimization level should I proceed with?

- [ ] **Option 1: Minimal** (1.5-2 hrs, 40-50% improvement)
- [ ] **Option 2: Medium** (4-6 hrs, 60-70% improvement)
- [ ] **Option 3: Maximum** (9-12 hrs, 10× usability)
- [ ] **Custom:** [Specify which changes from multiple tiers]
- [ ] **Skip:** Skill is fine as-is, no optimization needed

**Default Action:** If no response within [timeframe], I will proceed with **Option 1 (Minimal)** as it has lowest risk and immediate ROI.

---

```

#### After User Decision

**If user selects an option:**

1. **Confirm scope**
   ```markdown
   Proceeding with [Option] optimization:
   - Change 1: [Description]
   - Change 2: [Description]
   - [...]

   Estimated time: [X] hours
   Expected completion: [Date/Time]

   I will provide progress updates at [checkpoints].
   ```

2. **Execute changes** (see Implementation section below)

3. **Validate improvements**
   - Re-run evaluation (expect +[X] points)
   - Test with sample use case
   - Document changes in version history

4. **Commit and push**
   ```bash
   git add .claude/skills/[skill-name]/
   git commit -m "[tier] optimization: [summary of changes]

   [Detailed changes]

   Metrics: [before] → [after]"
   git push
   ```

---

## Quality Gates

### Pre-Analysis Checklist

Before starting optimization analysis:

- [ ] Skill has been used ≥25 times (or user overrides minimum)
- [ ] Logs are accessible and parseable
- [ ] cc-skill-evaluator is available
- [ ] SKILL-DESIGN-BEST-PRACTICES.md is available
- [ ] Have 30-45 minutes for full analysis

### Analysis Quality Checklist

Before presenting HITL options:

- [ ] **Usage metrics calculated** from real log data (not estimates)
- [ ] **Evaluation score** obtained using standard framework
- [ ] **Struggle patterns identified** with specific line references
- [ ] **Root causes documented** with evidence
- [ ] **3 options designed** with realistic effort estimates
- [ ] **Before/after metrics** quantified for each option
- [ ] **Recommendation justified** based on specific context

### HITL Presentation Checklist

Before presenting to user:

- [ ] Executive summary <200 words
- [ ] Key findings in scannable format (tables)
- [ ] Each option has clear pros/cons
- [ ] Effort estimates are realistic (not optimistic)
- [ ] Metrics are specific, not generic ("40% faster" vs "faster")
- [ ] Recommendation includes rationale
- [ ] Default action specified
- [ ] User decision checkboxes provided

### Post-Implementation Checklist

After implementing chosen option:

- [ ] All promised changes completed
- [ ] Re-evaluated skill (score improved?)
- [ ] Tested with sample use case
- [ ] Version history updated
- [ ] Changes committed with detailed message
- [ ] Before/after metrics documented

---

## Templates

### Analysis Report Template

See Phase 5 HITL Presentation Template above.

### Implementation Commit Template

```markdown
[tier] optimization of [skill-name]: [summary]

Implemented [Minimal/Medium/Maximum] optimization based on usage analysis
of [N] invocations.

Changes:
- [Change 1]: [Specific file/section modified]
- [Change 2]: [Specific file/section modified]
- [Change 3]: [Specific file/section modified]

Metrics (before → after):
- Reads per session: [X] → [Y] ([Z]% improvement)
- Tools per invocation: [X] → [Y] ([Z]% improvement)
- [Other metric]: [X] → [Y] ([Z]% improvement)

Evaluation score: [X]/100 → [Y]/100 (+[Z] points)

See full analysis: .claude-state/[skill-name]-optimization-analysis.md
```

---

## Examples

### Example 1: skill-evaluator Optimization (Real Case)

**Skill:** `cc-skill-evaluator`
**Analyzed:** 135 invocations (15 sessions)
**Date:** 2025-11-10

**Findings:**
- **Usage:** 3 reads per session (should be 1)
- **Evaluation:** 85/100 (Strong, but cognitive load issues)
- **Struggles:** Re-read every 20-45 skills, 65% re-read rate
- **Root cause:** No session caching instruction

**Options Presented:**
1. **Minimal:** Add caching note + scorecard (2 hrs) → 23% efficiency gain ✓ SELECTED
2. **Medium:** + Quick Start + bias prevention (5 hrs) → 60% improvement
3. **Maximum:** Full v2 redesign (9 hrs) → 10× usability

**User Decision:** Option 1 (Minimal) for immediate ROI

**Results:**
- Implementation time: 1.5 hours (under estimate)
- Reads per session: 3 → 1 (67% reduction)
- Tools per invocation: 4.5 → 3.1 (31% reduction)
- Validation: Tested with 5 evaluations, confirmed efficiency gain

**Full analysis:** `.claude-state/SKILL-EVALUATOR-ANALYSIS-SYNTHESIS.md`

---

### Example 2: dev-systematic-debugging (Hypothetical)

**Skill:** `dev-systematic-debugging`
**Analyzed:** 42 invocations
**Current Score:** 90/100 (Exemplary)

**Findings:**
- **Usage:** 1.2 reads per invocation (excellent)
- **Evaluation:** Exemplary across all dimensions
- **Struggles:** Only 2 minor confusion points (4.7% rate)
- **Root cause:** None significant

**Options Presented:**
1. **Minimal:** Fix 2 minor ambiguities (30 min) → 95% → 100% success rate
2. **Medium:** Add advanced debugging for distributed systems (3 hrs)
3. **Skip:** Skill is already excellent, minimal benefit from optimization

**Recommendation:** Skip or Minimal
- Skill is performing well (90/100, low re-read rate)
- Only invest if those 2 ambiguities are causing real issues
- Better to focus optimization efforts on lower-scoring skills

---

## Anti-Patterns

### ❌ Anti-Pattern 1: Optimizing Too Early

**Problem:** Running analysis after only 5-10 uses
**Why bad:** Insufficient data, patterns not yet established
**Instead:** Wait for ≥25 uses unless critical issues reported

### ❌ Anti-Pattern 2: Analysis Paralysis

**Problem:** Spending 4 hours analyzing, presenting 8 options
**Why bad:** User overwhelmed, decision fatigue
**Instead:** Limit to 3 well-designed options (minimal/medium/maximum)

### ❌ Anti-Pattern 3: Ignoring Context

**Problem:** Recommending Maximum tier for rarely-used skill
**Why bad:** 12 hours of work for skill used 3×/year = poor ROI
**Instead:** Consider usage frequency in recommendation

### ❌ Anti-Pattern 4: Optimistic Estimates

**Problem:** "This will take 2 hours" → Actually takes 6 hours
**Why bad:** User plans based on estimate, frustrated when it's wrong
**Instead:** Add 25-50% buffer to effort estimates

### ❌ Anti-Pattern 5: Metrics Without Evidence

**Problem:** "This change will improve efficiency by 40%" (guess)
**Why bad:** Cannot validate, builds false expectations
**Instead:** Base estimates on actual log data analysis

### ❌ Anti-Pattern 6: Implementing Without HITL

**Problem:** Skip user decision, jump to implementation
**Why bad:** May optimize wrong aspects, user priorities ignored
**Instead:** ALWAYS present options and get explicit user choice

---

## Troubleshooting

### Issue: Can't find enough usage logs

**Symptoms:** <25 invocations found in logs
**Causes:**
- Skill recently created
- Logs rotated/deleted
- Skill not used frequently

**Solutions:**
1. Lower threshold: Analyze available data (minimum 10 invocations)
2. Skip optimization: Insufficient data, wait for more uses
3. Synthetic testing: Use skill 25× in controlled tests to generate data

---

### Issue: Logs are in wrong format

**Symptoms:** Can't parse JSONL, unexpected structure
**Causes:**
- Different logging format
- Corrupted log files
- Non-standard tool output

**Solutions:**
1. Check log format: Confirm JSONL (one JSON object per line)
2. Update parser: Adapt script to handle format variation
3. Manual analysis: Review logs visually if parsing fails

---

### Issue: Evaluation score doesn't match usage data

**Symptoms:** High evaluation score (90/100) but high re-read rate
**Causes:**
- Evaluation missed specific usability issue
- Usage pattern is atypical
- New issue not captured in evaluation framework

**Solutions:**
1. Re-evaluate: Focus on Performance and Clarity dimensions
2. Weight usage data: Actual behavior > theoretical assessment
3. Document discrepancy: Note in analysis that usage reveals hidden issue

---

### Issue: Can't determine root cause

**Symptoms:** Clear inefficiency pattern but unclear why
**Causes:**
- Need deeper log analysis
- Multiple confounding factors
- Edge case or unusual scenario

**Solutions:**
1. Sample more logs: Analyze 10-20 invocations in detail
2. Controlled test: Use skill yourself to reproduce issue
3. User interview: Ask agents/users directly about confusion points

---

## Research Foundation

This skill synthesizes best practices from:

### Cognitive Science
- Miller's Law (7±2 chunks) - Cognitive load management
- Sweller's Cognitive Load Theory - Intrinsic/extraneous/germane load

### Software Engineering
- Performance profiling methodology - Measure before optimizing
- A/B testing principles - Controlled comparison of options
- Technical debt analysis - Cost/benefit of refactoring

### Decision Science
- Kahneman's "Thinking, Fast and Slow" - Decision quality under uncertainty
- Multi-criteria decision analysis (MCDA) - Structured option comparison

### Empirical Evidence
- Analysis of 66 elite skills (avg score 85/100)
- skill-evaluator case study (135 evaluations, 85MB logs)
- Usage pattern analysis (26 sessions, 4,756 tool calls)

**Key Insight:** Real usage data >> theoretical design assumptions
- 65% of inefficiency missed in initial design
- Discovered only through log analysis
- Validated through before/after metrics

---

## Related Skills

- **cc-skill-evaluator** - 0-100 scoring framework (apply before optimization)
- **cc-writing-skills** - TDD approach to creating skills (use for rewrites)
- **cc-gardening-skills-wiki** - Maintain skills wiki (update after changes)
- **dev-systematic-debugging** - Four-phase debugging (apply to skill issues)

---

## Supporting Documentation

- **`.claude-state/SKILL-DESIGN-BEST-PRACTICES.md`** - Comprehensive best practices guide (10 core principles, research-backed)
- **`.claude-state/SKILL-EVALUATOR-ANALYSIS-SYNTHESIS.md`** - Complete example analysis of skill-evaluator optimization

---

## Version History

- **v1.0 (2025-11-10):** Initial creation based on:
  - Real optimization of skill-evaluator (135 evaluations analyzed)
  - SKILL-DESIGN-BEST-PRACTICES synthesis (40+ sources)
  - 66 elite skills library transformation learnings
  - Production usage pattern analysis (85MB logs, 26 sessions)

---

## Metadata

```yaml
name: cc-skill-in-practice-optimizer
category: claude-code-meta
version: 1.0
created: 2025-11-10
dependencies:
  - cc-skill-evaluator
  - .claude-state/SKILL-DESIGN-BEST-PRACTICES.md
triggers:
  - Skill has been used ≥25 times
  - Error rate >10% reported
  - User reports confusion with skill
  - Periodic review (every 100 uses)
time_estimate: 30-45 minutes (analysis) + variable (implementation based on tier)
output:
  - Comprehensive analysis report
  - 3 tiered optimization options
  - User decision checkpoint
  - Implementation artifacts (if approved)
```
