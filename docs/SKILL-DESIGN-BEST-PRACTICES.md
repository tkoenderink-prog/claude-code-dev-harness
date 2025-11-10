# Skill Design Best Practices

**Purpose:** Research-backed guidelines for creating high-quality AI agent skills
**Audience:** Skill authors, meta-skill developers, harness maintainers
**Last Updated:** 2025-11-10
**Version:** 1.0

---

## Quick Reference

### The 10 Core Principles

| # | Principle | Guideline | Measurement |
|---|-----------|-----------|-------------|
| 1 | **Cognitive Load** | ≤7 chunks per section | Miller's Law (7±2) |
| 2 | **Progressive Disclosure** | Quick ref → Details → Appendix | 3 tiers minimum |
| 3 | **Scanability** | Tables > Prose for comparisons | <30 sec to find info |
| 4 | **Concrete Examples** | ≥3 examples per key concept | Real, not hypothetical |
| 5 | **Session Awareness** | Cache instructions for batches | 1 read per session |
| 6 | **Tool Efficiency** | ≤3.3 tools per skill invocation | Minimize re-reads |
| 7 | **Bias Prevention** | Explicit guardrails | Halo, anchor, fatigue |
| 8 | **HITL Checkpoints** | Strategic decisions only | Not tactical details |
| 9 | **Clear Triggers** | "When to use" in first 20 lines | No ambiguity |
| 10 | **Quality Gates** | Checklist before completion | Prevent common errors |

### Tier-Based Structure Template

```markdown
[1] QUICK START (50-100 lines)
    ├─ Purpose & when to use (10 lines)
    ├─ 30-second overview (10 lines)
    ├─ Key steps table (20 lines)
    └─ Decision tree (20 lines)

[2] DETAILED PROCESS (150-300 lines)
    ├─ Phase-by-phase walkthrough
    ├─ Checklists for each phase
    ├─ Examples integrated with steps
    └─ Error prevention at each stage

[3] APPENDICES (100-200 lines)
    ├─ Research foundation
    ├─ Extended examples
    ├─ Troubleshooting guide
    └─ Related skills
```

---

## 1. Cognitive Load Management

### The Science

**Miller's Law (1956):** Working memory holds 7±2 chunks simultaneously
**Sweller's Cognitive Load Theory (1988):** Three types of load to manage:
- **Intrinsic:** Inherent complexity of content (unavoidable)
- **Extraneous:** Poor presentation adds unnecessary load (minimize this)
- **Germane:** Mental effort building understanding (optimize this)

### Application to Skills

#### Rule: Maximum 7 Chunks Per Section

**Bad Example (12 chunks):**
```markdown
To evaluate a skill, consider: purpose clarity, content completeness,
example quality, documentation depth, error handling, edge case coverage,
performance characteristics, cognitive load, modularity, reusability,
integration patterns, and maintenance burden.
```

**Good Example (5 chunks + hierarchy):**
```markdown
To evaluate a skill, score 5 dimensions:
1. **Functional:** Does it work reliably?
2. **Clarity:** Easy to understand?
3. **Modularity:** Focused and reusable?
4. **Performance:** Efficient execution?
5. **Domain:** Right depth/breadth?

Each dimension has 4-6 sub-criteria (see detailed rubric).
```

#### Rule: Progressive Disclosure

**Tier 1 (Quick Start):** 7 chunks max
```
Purpose → Key Steps → Decision Point → Output
```

**Tier 2 (Detailed):** Each step expanded to 7 sub-chunks
```
Step 1 → [A, B, C, D, E, F, G] → Step 2 → [...]
```

**Tier 3 (Appendix):** Full details for edge cases

#### Measurement

| Metric | Target | How to Measure |
|--------|--------|----------------|
| **Chunks per section** | ≤7 | Count top-level items in each section |
| **Nesting depth** | ≤3 levels | Heading levels (##, ###, ####) |
| **Section length** | ≤100 lines | Line count between ## headers |
| **Skill total** | 300-600 lines | Core content before appendices |

### Anti-Patterns

❌ **All-at-once presentation** - 500 lines before first actionable step
❌ **Hidden process** - Buried at line 200 after extensive preamble
❌ **Scattered concepts** - Related ideas in distant sections
❌ **Redundant content** - Same criteria repeated 3× in different formats
❌ **No quick reference** - Must read entire skill every time

---

## 2. Progressive Disclosure

### The Principle

**Expertise Continuum:** Skills serve users from novice to expert
**Information Hiding:** Show only what's needed for current context
**Just-in-Time:** Provide details when user is ready to apply them

### Three-Tier Architecture

#### Tier 1: Quick Start (For Experts)

**Purpose:** Enable experienced users to start in <60 seconds
**Length:** 50-100 lines
**Content:**
- Purpose statement (1 line)
- When to use trigger (2-3 lines)
- 30-second overview
- Key steps (5-7 items max)
- Quick reference table
- Jump links to Tier 2

**Example:**
```markdown
# Skill Name v2.0

**Purpose:** [One sentence]
**When to use:** [Trigger conditions in 2-3 lines]
**Time:** 10-15 min | **Output:** [What you'll produce]

## 30-Second Overview
[Process in 50 words]

## Quick Steps
1. Step A (2 min)
2. Step B (5 min)
3. Step C (3 min)

[→ Detailed walkthrough](#detailed)
```

#### Tier 2: Detailed Process (For Practitioners)

**Purpose:** Enable correct application with understanding
**Length:** 150-300 lines
**Content:**
- Phase-by-phase walkthrough
- Why each step matters
- Common pitfalls per step
- Examples integrated with process
- Checklists to ensure completeness

#### Tier 3: Appendices (For Mastery)

**Purpose:** Reference, research, edge cases
**Length:** 100-200 lines
**Content:**
- Research foundation
- Extended examples
- Troubleshooting guide
- Comparison to alternatives
- Version history

### Navigation

**Required Elements:**
- Table of Contents with jump links
- "Next steps" at end of each section
- Breadcrumbs for deep sections
- Time estimates per tier

---

## 3. Scanability & Visual Hierarchy

### The Problem

**Eye-tracking research:** Users scan in F-pattern, don't read linearly
**Reading speed:** 250 wpm prose, 400+ wpm for tables/lists
**Decision time:** <30 seconds to determine if skill is relevant

### Solution: Tables > Prose

#### When to Use Tables

| Use Case | Format | Example |
|----------|--------|---------|
| **Comparisons** | Table with criteria columns | Comparing options A vs B vs C |
| **Checklists** | Table with checkboxes | Pre-flight checks before running |
| **Scoring rubrics** | Table with tiers and examples | 0-20 point scale per dimension |
| **Step sequences** | Table with step/time/output | Process with time estimates |
| **Decision trees** | Table with if/then | Routing logic |

#### Visual Hierarchy Elements

**Level 1: Headers**
```markdown
# Main Title (h1) - Skill name
## Major Section (h2) - Phases, core concepts
### Subsection (h3) - Steps within phase
#### Detail (h4) - Edge cases, advanced
```

**Level 2: Emphasis**
```markdown
**Bold** - Key terms, actions to take
*Italic* - Emphasis, foreign terms
`Code` - Literal references, commands
```

**Level 3: Lists**
```markdown
- Unordered for arbitrary items
1. Ordered for sequences
   - Nested for subcategories
```

**Level 4: Visual Markers**
```markdown
✅ Success criteria
❌ Anti-patterns
⚠️ Warnings
💡 Tips
🔥 High priority
```

**Level 5: Code Blocks & Quotes**
```markdown
Use ```language blocks for:
- Templates to fill out
- Example code
- Expected outputs
- Decision trees

Use > blockquotes for:
- Important warnings
- Research citations
- User quotes/testimonials
```

### Scanability Checklist

- [ ] Can determine relevance in <30 seconds
- [ ] Can find specific section in <15 seconds
- [ ] Tables for all comparison content
- [ ] Visual markers for priority items
- [ ] Headers every 20-30 lines max
- [ ] White space between sections
- [ ] No "walls of text" >10 lines without break

---

## 4. Concrete Examples

### The Principle

**Abstract vs Concrete Processing:**
- Abstract: "Consider edge cases" (vague, low retention)
- Concrete: "What if input is empty list? Return [] or throw error?" (clear, high retention)

**Example Quality Hierarchy:**
1. **Real examples from production** (highest value)
2. **Realistic hypotheticals based on real patterns** (good)
3. **Simplified teaching examples** (okay for concepts)
4. **Generic placeholder examples** (lowest value)

### Guidelines

#### Rule: ≥3 Examples Per Key Concept

**Key concept:** "Evaluate functional correctness"

**Insufficient (0 examples):**
```markdown
Functional correctness means the skill accomplishes its stated purpose.
Score based on how well content delivers on promise.
```

**Minimal (1 example):**
```markdown
**Example:** `test-driven-development` scores 19/20 because it clearly
states purpose (write tests before code) and delivers comprehensive
RED-GREEN-REFACTOR guidance with edge cases.
```

**Good (3 examples across quality spectrum):**
```markdown
**Exemplary (18-20):** `test-driven-development` - Clear purpose,
comprehensive coverage, handles edge cases, "Iron Law" prevents pitfalls.

**Good (12-14):** `code-organization` - Clear purpose, basic coverage,
some edge cases missing (e.g., monorepo scenarios).

**Poor (0-5):** `api-design` template - Generic purpose statement,
zero actual content, doesn't deliver value.
```

#### Rule: Examples Should Be Self-Contained

**Bad:** "See the earlier example of dimension scoring"
**Good:** Repeat the example in context, or provide clear reference with line number

#### Rule: Use Before/After for Transformations

```markdown
**BEFORE (Current State):**
[Show exact current content]

**AFTER (Improved State):**
[Show exact improved content]

**Why Better:**
- Reason 1 (specific)
- Reason 2 (specific)
```

### Example Templates

#### Decision Example Template
```markdown
**Scenario:** [Describe situation]
**Options:**
- A: [Option with tradeoffs]
- B: [Option with tradeoffs]
**Recommended:** [Choice] because [specific reasoning]
**Example:** [Real case where this applied]
```

#### Process Example Template
```markdown
**Input:** [What you start with]
**Process:**
1. [Step with specific action]
2. [Step with specific action]
3. [Step with specific action]
**Output:** [What you produce]
**Time:** [Actual time this took]
```

---

## 5. Session Awareness

### The Problem

**Discovery:** Analysis of skill-evaluator logs showed agents re-read skills 3× per session
**Root cause:** Skills designed for single-use, not batch operations
**Impact:** 23% efficiency loss, 180K wasted tokens per session

### Solution: Explicit Session Caching

#### For Skills Used in Batches

Add at top of skill (within first 20 lines):

```markdown
## Usage Notes

### For Batch Operations
**Read once per session:** This skill is designed for batch use. Read it
ONCE at the start of your session and refer to cached content for all
subsequent operations. Do NOT re-read for each item in batch.

**For task prompts:** Include full skill content in task prompt to avoid
repeated file reads.
```

#### For Skills Used in Loops

```markdown
## Usage Notes

### For Iterative Operations
**Cache criteria:** If evaluating multiple items (e.g., 10+ files), read
this skill once and cache the criteria. Apply cached criteria to each item
without re-reading.

**Recalibration:** Re-read skill after every 20 items to prevent drift.
```

#### For Skills with High Re-Read Rates

Identify if your skill is being re-read unnecessarily:
- Check logs for multiple Read() calls within single session
- If skill >500 lines and read 3+ times, add session caching note
- If skill has reference tables, consider extracting to separate quick-reference

---

## 6. Tool Call Efficiency

### Baseline Performance

From analysis of 66 elite skills:
- **Average:** 3.3 tools per skill invocation
- **Best:** 1.2 tools (simple lookup skills)
- **Acceptable:** ≤5.0 tools
- **Concerning:** >5.0 tools (needs optimization)

### Common Anti-Patterns

#### Anti-Pattern 1: Multiple Reads of Same File

**Problem:**
```
1. Read skill.md (lines 1-100)
2. Process...
3. Read skill.md (lines 101-200)  # UNNECESSARY
4. Process...
5. Read skill.md (lines 201-300)  # UNNECESSARY
```

**Solution:** Read entire skill once, or use limit/offset efficiently

#### Anti-Pattern 2: Grep Then Read

**Problem:**
```
1. Grep skill.md for "evaluation criteria"  # Find location
2. Read skill.md  # Read whole file anyway
```

**Solution:** If likely to read whole file, skip grep and read directly

#### Anti-Pattern 3: Re-reading Skill Mid-Process

**Problem:** Skill instructions unclear, agent re-reads to clarify

**Solution:**
- Add checklist at each step to prevent re-reading
- Put decision trees inline, not as references
- Include key info at point of use, not "see above"

### Optimization Guidelines

| Skill Length | Expected Tools | Optimization Target |
|--------------|----------------|---------------------|
| <200 lines | 1-2 | Single read, minimal follow-up |
| 200-500 lines | 2-3 | One read, possibly 1 grep for specific section |
| 500+ lines | 3-4 | Quick ref section avoids full read |
| Batch use | 1 read per session | Session caching prevents re-reads |

---

## 7. Bias Prevention

### The Problem

**Cognitive biases affect AI agents** just as they affect humans when:
- Making sequential decisions (evaluation of multiple items)
- Holding multiple criteria in mind (halo effect)
- Operating under time pressure (satisficing)
- Processing information incrementally (anchor bias)

### Common Biases in Skill Usage

#### Halo Effect
**Problem:** High score in first criterion biases toward high scores in subsequent criteria

**Prevention:**
```markdown
### Bias Prevention: Halo Effect

After scoring Dimension A, **cover your score** before evaluating Dimension B.
Each dimension must be scored independently based on its own criteria, not
influenced by previous scores.
```

#### Anchor Bias
**Problem:** First impression during initial read locks all subsequent judgments

**Prevention:**
```markdown
### Step 1: Initial Read

**Goal:** Understand content, NOT judge quality
**Instruction:** Note observations, defer judgment until complete analysis
**Anti-pattern:** "This looks bad, probably 3/10" in first 30 seconds
```

#### Central Tendency Bias
**Problem:** Avoiding extreme scores, clustering around middle (10-15 on 0-20 scale)

**Prevention:**
```markdown
### Scoring Requirement

You MUST use the full 0-20 range. If you find all your scores in 10-15 range,
you are likely exhibiting central tendency bias. Actively use:
- 0-5 for truly poor content
- 18-20 for exemplary content
```

#### Contrast Effect
**Problem:** Comparing to previous item rather than absolute standard

**Prevention:**
```markdown
### Calibration

Before each evaluation, review calibration examples (not previous evaluation).
Compare to rubric standard, NOT to previous item in batch.
```

#### Fatigue/Sequential Bias
**Problem:** Quality of decisions degrades over time in long sessions

**Prevention:**
```markdown
### Mandatory Breaks

- Take 5-minute break after every 5 evaluations
- Re-read calibration examples after break
- If feeling fatigued, stop and resume later
- Consider randomizing evaluation order
```

### Quality Gates Checklist

Before completing any evaluation/analysis:

```markdown
## Quality Gates

### Score Alignment
- [ ] Scores match evidence provided
- [ ] Used full range (not all clustered)
- [ ] Independent dimensions (no halo effect)

### Bias Checks
- [ ] Compared to rubric, not previous item
- [ ] Deferred judgment until complete analysis
- [ ] Not exhibiting fatigue (take break if yes)
```

---

## 8. HITL (Human-In-The-Loop) Patterns

### The Principle

**Strategic vs Tactical Decisions:**
- **Strategic (User decides):** Business priorities, major architectural choices, resource allocation
- **Tactical (Agent decides):** Implementation details, code structure, specific algorithms

**Question Batching:** Accumulate 3-5 questions before interrupting user

### HITL Checkpoint Template

```markdown
## HITL Checkpoint: [Decision Point Name]

**Context:** [Current state in 2-3 sentences]

**Decision Required:** [What needs to be decided]

### Options

**Option A: [Name]** ✓ Recommended
- **Pros:** [Specific benefits]
- **Cons:** [Specific drawbacks]
- **Effort:** [Time estimate]
- **Risk:** [High/Medium/Low]

**Option B: [Name]**
- **Pros:** [Specific benefits]
- **Cons:** [Specific drawbacks]
- **Effort:** [Time estimate]
- **Risk:** [High/Medium/Low]

**Option C: [Name]**
[Same format]

### Recommendation

[Agent's recommendation with specific reasoning based on context]

### Default Action

If no response by [timeframe], will proceed with Option [X] because [reasoning].

---

**[User responds here]**

---
```

### When to Use HITL

| Situation | HITL? | Why |
|-----------|-------|-----|
| Multiple valid approaches (2+ options with tradeoffs) | ✅ Yes | User priorities determine best choice |
| Unclear requirements | ✅ Yes | Need clarification to proceed correctly |
| One clearly correct approach | ❌ No | Agent should decide and proceed |
| Purely technical implementation detail | ❌ No | Agent expertise, user doesn't need to decide |
| Security/legal/data privacy implications | ✅ Yes | User must approve risk |
| Reversible decision with low cost | ❌ No | Try one approach, adjust if needed |
| Irreversible decision with high cost | ✅ Yes | User should approve major changes |

---

## 9. Clear Triggers

### The Problem

**Vague trigger:** "Use when optimizing code"
- When is code "not optimized"?
- Optimize for speed, memory, readability?
- Micro-optimizations or architecture?

**Clear trigger:** "Use when profiler shows >100ms in specific function and you need to reduce latency"

### Trigger Specification Template

```markdown
## When to Use This Skill

**Primary Trigger:**
[One specific, measurable condition]

**Supporting Triggers:**
- [Specific condition 1]
- [Specific condition 2]
- [Specific condition 3]

**Do NOT Use When:**
- [Anti-condition 1]
- [Anti-condition 2]

**Example Scenarios:**
✅ **Use:** [Concrete scenario where skill applies]
❌ **Don't Use:** [Concrete scenario where skill doesn't apply]
```

### Trigger Quality Checklist

- [ ] Trigger appears in first 20 lines of skill
- [ ] Trigger is specific and measurable (not "when code is bad")
- [ ] Clear boundary between when to use vs not use
- [ ] Concrete example scenarios provided
- [ ] Related skills referenced (if X use skill-A, if Y use skill-B)

### Examples

**Bad Triggers:**
- "Use when working with databases" (too broad)
- "Use when code needs improvement" (vague)
- "Use for testing" (which kind of testing?)

**Good Triggers:**
- "Use when encountering N+1 query problem (many queries in loop instead of one optimized query)"
- "Use when test coverage <80% and adding new feature to critical path"
- "Use when integration tests fail inconsistently (pass/fail on same code)"

---

## 10. Quality Gates

### Pre-Launch Quality Checklist

Before publishing a skill, verify:

#### Content Quality
- [ ] Purpose clear in first 10 lines
- [ ] Trigger specified in first 20 lines
- [ ] ≥3 concrete examples for key concepts
- [ ] All steps have checklists or decision criteria
- [ ] No placeholder text ("TODO", "TBD", "example here")

#### Structure Quality
- [ ] Quick reference exists (Tier 1)
- [ ] Detailed process exists (Tier 2)
- [ ] Appendices for research/edge cases (Tier 3)
- [ ] Table of contents with navigation
- [ ] Time estimates for process

#### Cognitive Load
- [ ] ≤7 chunks per major section
- [ ] ≤3 levels of nesting
- [ ] Total length 300-600 lines (core) + appendices
- [ ] No redundant content (same info repeated 3×)

#### Usability
- [ ] Scannable (tables for comparisons)
- [ ] Visual hierarchy (headers, lists, emphasis)
- [ ] Can find key info in <30 seconds
- [ ] Session caching note if used in batches
- [ ] Quality gates checklist at end of process

#### Bias Prevention
- [ ] Explicit instructions for common biases
- [ ] Calibration examples for consistency
- [ ] Break reminders for long processes
- [ ] Validation checklist before completion

#### Examples
- [ ] ≥3 examples across quality spectrum (high/medium/low)
- [ ] Examples are self-contained (not "see above")
- [ ] Real examples > hypothetical > generic
- [ ] Before/after for transformations

#### Tool Efficiency
- [ ] Expected tool calls: ≤5 per invocation
- [ ] No unnecessary re-reads
- [ ] Session caching if applicable
- [ ] Clear when to read vs reference

### Post-Launch Monitoring

After skill is in production:

#### Usage Analysis (After 25 Uses)
- [ ] Parse logs for usage patterns
- [ ] Count tool calls per invocation (target: ≤3.3 avg)
- [ ] Check for re-read patterns (should be 1 per session for batch skills)
- [ ] Identify confusion points (retries, errors, clarification questions)

#### Quality Metrics
- [ ] Consistency check: Same inputs → similar outputs?
- [ ] Error rate: % of invocations with errors or retries
- [ ] User satisfaction: Qualitative feedback
- [ ] Completion rate: % of invocations that reach end state

#### Optimization Triggers

Run **cc-skill-in-practice-optimizer** when:
- Error rate >10%
- Tool calls >5.0 average
- Re-read rate >2 per session
- User reports confusion
- After 100 uses (periodic review)

---

## Research Foundation

### Cognitive Science

**Miller, G. A. (1956).** "The Magical Number Seven, Plus or Minus Two: Some Limits on Our Capacity for Processing Information." *Psychological Review*, 63(2), 81-97.
- Establishes working memory limit of 7±2 chunks

**Sweller, J. (1988).** "Cognitive Load During Problem Solving: Effects on Learning." *Cognitive Science*, 12(2), 257-285.
- Cognitive Load Theory: Intrinsic, extraneous, germane load
- Minimize extraneous load through design

**Cowan, N. (2001).** "The Magical Number 4 in Short-Term Memory: A Reconsideration of Mental Storage Capacity." *Behavioral and Brain Sciences*, 24(1), 87-114.
- Updates Miller's 7±2 to more conservative 4±1 for true capacity

### Information Architecture

**Nielsen, J. (1993).** *Usability Engineering*. Morgan Kaufmann.
- F-pattern eye tracking
- Scanability principles
- Progressive disclosure

**Krug, S. (2000).** *Don't Make Me Think*. New Riders.
- Minimize cognitive load in interfaces
- Self-evident design principles

### Decision Making

**Kahneman, D., & Tversky, A. (1974).** "Judgment under Uncertainty: Heuristics and Biases." *Science*, 185(4157), 1124-1131.
- Systematic biases in human judgment
- Anchor bias, availability heuristic

**Kahneman, D. (2011).** *Thinking, Fast and Slow*. Farrar, Straus and Giroux.
- System 1 (fast, intuitive) vs System 2 (slow, deliberate)
- Halo effect, confirmation bias

### Learning & Pedagogy

**Clark, R. C., & Mayer, R. E. (2016).** *E-Learning and the Science of Instruction*. Wiley.
- Multimedia learning principles
- Worked examples effect
- Coherence principle (remove extraneous material)

**Van Merriënboer, J. J. G., & Sweller, J. (2005).** "Cognitive Load Theory and Complex Learning." *Educational Psychology Review*, 17(2), 147-177.
- Four-component instructional design model
- Sequencing from simple to complex

---

## Skill Quality Benchmarks

Based on analysis of 66 elite skills in this library:

### Exemplary Skills (90-100/100)

**Common characteristics:**
- Clear "Iron Laws" or core principles
- Comprehensive coverage with edge cases
- Concrete examples (5-10+ examples)
- Anti-patterns section ("what NOT to do")
- Quick reference + detailed guide
- Research citations where applicable

**Examples:**
- `dev-test-driven-development` (91) - RED-GREEN-REFACTOR with Iron Law
- `think-quick-recognition` (91) - 4-category diagnostic framework
- `dev-systematic-debugging` (90) - Four-phase debugging framework

### Strong Skills (80-89/100)

**Common characteristics:**
- Clear purpose and trigger
- Good examples (3-5 examples)
- Structured process
- Checklists or decision trees
- Minor gaps in edge case coverage

**Improvement path:** Add 2-3 examples, edge case section, anti-patterns

### Good Skills (70-79/100)

**Common characteristics:**
- Clear purpose
- Basic process description
- Some examples (1-2)
- Needs more depth

**Improvement path:** Add examples, restructure for scanability, add checklists

### Skills to Remove (<60/100)

**Common characteristics:**
- Template structure (77 lines)
- Generic placeholder content
- No concrete examples
- Vague purpose

**Action:** Remove or complete rewrite

---

## Version History

- **v1.0 (2025-11-10):** Initial compilation based on:
  - Analysis of skill-evaluator usage (135 evaluations, 85MB logs)
  - Elite skills library transformation (135 → 66 skills)
  - Research synthesis (40+ academic sources)
  - Production usage patterns

---

## See Also

- `cc-skill-evaluator` - 0-100 scoring framework for skills
- `cc-writing-skills` - TDD approach to creating skills
- `cc-skill-in-practice-optimizer` - Optimize skills based on usage data
- `.claude-state/SKILL-EVALUATOR-ANALYSIS-SYNTHESIS.md` - Detailed usage analysis
