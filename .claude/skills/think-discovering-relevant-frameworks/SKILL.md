---
name: Discovering Relevant Frameworks
description: Knowledge-graph-aware search finds mental models, books, people for current problem/domain using structural navigation
when_to_use: when starting to solve problem, make decision, design solution, or user asks "what do I know about X?"
version: 1.0.0
languages: all
---

# Discovering Relevant Frameworks

## Overview

**Your knowledge graph has structure. Search it structurally.**

Different from generic file search - this leverages:
- Mental Models MoC as central hub
- Books organized by domain
- People linked to their frameworks
- Cross-references between all three types

**Core principle:** Start with hubs (MoCs), follow links, search multiple entry points. The knowledge graph IS your edge.

## When to Use

**Trigger phrases (automatic):**
- "How should I approach X?"
- "What's the best way to Y?"
- "I'm stuck on Z"
- "Help me understand [domain]"
- Before creating implementation plan
- Before making strategic decision
- User asks: "What do I know about X?"

**Proactive triggers (consider):**
- About to solve complex problem
- Designing new system
- Making trade-off decision
- Evaluating multiple approaches
- Entering unfamiliar domain

## Multi-Entry-Point Search Strategy

**Why multiple entry points?**
- Mental Models MoC → Fast, curated, 200+ frameworks
- Books → Deep domain knowledge, comprehensive teaching
- People → Philosophical context, understand the thinker
- Cross-reference → Catch what hubs miss

**Use ALL entry points. They reveal different things.**

## Entry Point 1: Mental Models MoC (Start Here)

**ALWAYS start here - fastest path to frameworks**

```bash
# Step 1: Read the MoC
Read: 03-RESOURCES/Mental Models/MoC Mental Models.md
```

**What to scan:**

1. **Featured Mental Models** (12 extracted, most detailed)
   - Scan for obvious matches to your problem domain
   - These are the deep-dive notes

2. **Comprehensive Table** (200+ catalogued)
   - Organized by domain (Business, Psychology, Philosophy, etc.)
   - Each row has: Model | Creator | Description | Power | Weakness
   - Scan YOUR domain section thoroughly
   - Check related domains (problems often span multiple)

3. **Mental Models from Books** (organized by book)
   - If you know relevant book, check what models it contains
   - Example: "Principles" → 5-Step Process, Radical Transparency, etc.

**Quick scan time: 30-60 seconds to find 2-5 candidate frameworks**

**Example:**
```
Problem: "Team underperforming, missed deadlines"
→ Read MoC Mental Models
→ Scan: Leadership & Business section
→ Find:
  - [[Extreme Ownership]] - Complete accountability
  - [[Decentralized Command]] - Empowered sub-leaders
  - [[Prioritize and Execute]] - Focus on highest priority
  - [[Circle of Influence]] - Focus on controllables
→ Read those 3-4 notes (2-3 minutes)
```

## Entry Point 2: Books by Domain

**Use when:** Need deep domain knowledge, comprehensive treatment

```bash
# Step 1: Identify domain
# Leadership, Psychology, Technology, Business, Health, etc.

# Step 2: Search books in that domain
Grep pattern: "domain-keyword" -i
path: 03-RESOURCES/Books/
output_mode: files_with_matches
head_limit: 10
```

**What to look for:**
- Book titles matching your domain
- Books by known experts in the field
- Books that extracted mental models you need

**Then:**
- Read book summaries (2-3 most relevant)
- Follow links to mental models extracted from books
- Note author - check their person profile for broader context

**Example:**
```
Problem: "Need personal productivity system"
→ Domain: Productivity, Time Management
→ Grep "productivity|time|GTD|deep work" in Books/
→ Find:
  - [[Getting Things Done]] - Capture-clarify-organize system
  - [[Deep Work]] - Focus vs shallow work distinction
  - [[Digital Minimalism]] - Technology relationship
  - [[Four Thousand Weeks]] - Finite time philosophy
→ Read summaries → Extract mental models
```

## Entry Point 3: Influential People

**Use when:**
- Know relevant thought leader
- Want philosophical context
- Need to understand the thinker behind framework

```bash
# Step 1: Search by name or domain
Grep pattern: "thought-leader-name|domain" -i
path: 03-RESOURCES/Influential People/
output_mode: files_with_matches
```

**What to read:**
- Philosophy section (how they think)
- Key concepts they created
- Links to their books
- Links to mental models they popularized

**Value:** Understanding the THINKER helps understand when/how to apply their frameworks

**Example:**
```
Context: "Heard Ray Dalio's principles mentioned"
→ Read [[Ray Dalio]] in Influential People
→ Philosophy: Pain+reflection, radical transparency, systematic thinking
→ Books: [[Principles]], [[Big Debt Crises]]
→ Mental Models: [[5-Step Process]], [[Radical Transparency]], [[Idea Meritocracy]]
→ Now understand Dalio's worldview → Apply frameworks in context
```

## Entry Point 4: Cross-Reference Search

**Use when:** MoC scan didn't find obvious match

```bash
# Search across all three directories
# Mental Models
Grep pattern: "keyword1|keyword2|keyword3" -i
path: 03-RESOURCES/Mental Models/
output_mode: files_with_matches

# Books
Grep pattern: "keyword1|keyword2" -i
path: 03-RESOURCES/Books/
output_mode: files_with_matches
head_limit: 10

# People
Grep pattern: "keyword1|keyword2" -i
path: 03-RESOURCES/Influential People/
output_mode: files_with_matches
```

**Why this works:**
- Catches frameworks mentioned in descriptions but not in featured list
- Finds books that don't have keyword in title
- Discovers thought leaders working in this space

## Discovery Output Format

**ALWAYS structure findings for user:**

```markdown
## Relevant Knowledge Found: [Topic]

**Mental Models** ([count] found):
- [[Model 1]] - [One-line: what this framework reveals]
- [[Model 2]] - [One-line: what this framework reveals]
- [[Model 3]] - [One-line: what this framework reveals]

**Books** ([count] found):
- [[Book 1]] by [[Author]] - [What it teaches about this problem]
- [[Book 2]] by [[Author]] - [What it teaches about this problem]

**Influential People** ([count] found):
- [[Person 1]] - [Their perspective on this]
- [[Person 2]] - [Their perspective on this]

**Recommendation:**
[Which to read first based on current context - 1-2 sentences]
```

**Why this format?**
- User sees WHAT was found (not just titles)
- User sees WHY each is relevant (context-specific)
- User gets prioritization (where to start)
- Links enable immediate navigation

## Discovery Workflow Checklist

**IMPORTANT: Use TodoWrite for multi-step discoveries**

### Quick Discovery (3-5 min) - For acute problems

- [ ] **Read MoC Mental Models** (start here ALWAYS)
- [ ] **Scan relevant domain sections**
- [ ] **Identify 2-3 candidate frameworks**
- [ ] **Quick grep if needed** (supplementary search)
- [ ] **Report findings** (structured format)

### Comprehensive Discovery (10-15 min) - For strategic problems

- [ ] **Read MoC Mental Models** (featured + table)
- [ ] **Identify 4-6 candidate frameworks**
- [ ] **Search Books by domain**
- [ ] **Check relevant Influential People**
- [ ] **Cross-reference grep** (all three directories)
- [ ] **Read book summaries** (2-3 most relevant)
- [ ] **Read person philosophies** (1-2 most relevant)
- [ ] **Synthesize findings** (what each adds)
- [ ] **Report findings** (comprehensive format with recommendations)

## Common Mistakes

| Mistake | Impact | Fix |
|---------|--------|-----|
| **Generic grep only** | Overwhelming results, miss hub structure | ALWAYS start with MoC Mental Models |
| **Stopped after first find** | Missed complementary frameworks | Check all entry points |
| **Didn't follow cross-references** | Isolated finding from graph | Follow links: Model → Book → Person |
| **Read titles only** | Misjudged relevance | Read overviews/summaries completely |
| **No recommendation** | User overwhelmed by results | Prioritize 2-3 to read first |
| **Skipped MoC** | Reinvented search of organized knowledge | MoC is your index - use it |
| **Only searched one domain** | Missed cross-domain insights | Problems often span multiple domains |

## Example Walkthroughs

### Example 1: Acute Leadership Problem

**Problem:** "Team missed Q4 deadline. Stakeholders upset. What framework applies?"

**Quick Discovery (3 min):**

```bash
# Step 1: Read MoC (60s)
Read: 03-RESOURCES/Mental Models/MoC Mental Models.md
# → Scan Leadership section

# Step 2: Found (30s)
- [[Extreme Ownership]] - Leader owns ALL outcomes
- [[Prioritize and Execute]] - Focus highest priority
- [[Circle of Influence]] - Control what you can

# Step 3: Supplementary search (60s)
Grep pattern: "deadline|accountability|leadership" -i
path: 03-RESOURCES/Mental Models/
# → Confirms top 3, adds [[Decentralized Command]]

# Step 4: Report (30s)
```

**Output:**
```markdown
## Relevant Knowledge: Team Deadline Miss

**Mental Models** (3 found):
- [[Extreme Ownership]] - Take complete responsibility, no blame
- [[Prioritize and Execute]] - Clear highest priority for recovery
- [[Circle of Influence]] - Focus on what you control (your response)

**Recommendation:**
Start with Extreme Ownership (perfect match for accountability). Then apply Prioritize and Execute for recovery plan.
```

**Total time: 3 minutes, actionable frameworks found**

### Example 2: Strategic Organizational Challenge

**Problem:** "Organization struggling to innovate. Ideas die in committees. Need deep understanding."

**Comprehensive Discovery (12 min):**

```bash
# Step 1: MoC comprehensive scan (3 min)
Read: 03-RESOURCES/Mental Models/MoC Mental Models.md
# → Scan: Leadership, Business, Systems Thinking, Psychology

# Found in MoC:
- [[Reinventing Organizations]] (Teal) - Self-management
- [[AQAL]] - Four quadrants (I, It, We, Its)
- [[Radical Transparency]] - Idea meritocracy
- [[Antifragile]] - Systems that benefit from disorder
- [[First Principles Thinking]] - Challenge assumptions

# Step 2: Search Books (3 min)
Grep pattern: "innovation|organizational|culture|bureaucracy" -i
path: 03-RESOURCES/Books/

# Found books:
- [[Reinventing Organizations]] - Laloux
- [[Principles - Life and Work]] - Dalio
- [[The Lean Startup]] - Ries
- [[Life 3.0]] - Tegmark

# Step 3: Check People (2 min)
Grep pattern: "innovation|organizational" -i
path: 03-RESOURCES/Influential People/

# Found people:
- [[Frédéric Laloux]] - Teal organizations
- [[Ray Dalio]] - Radical transparency
- [[Nassim Nicholas Taleb]] - Antifragile systems
- [[Ken Wilber]] - AQAL framework

# Step 4: Read summaries (3 min)
Read: [[Reinventing Organizations]] summary
Read: [[Ray Dalio]] philosophy section

# Step 5: Synthesize (1 min)
```

**Output:**
```markdown
## Relevant Knowledge: Innovation Stagnation

**Mental Models** (5 found):
- [[Reinventing Organizations]] (Teal) - Self-management vs hierarchy
- [[AQAL Four Quadrants]] - Individual/Collective, Interior/Exterior perspective
- [[Radical Transparency]] - Truth-seeking vs politics in decisions
- [[Antifragile]] - Decentralize experiments, embrace controlled failures
- [[First Principles Thinking]] - Challenge "we need committees" assumption

**Books** (4 found):
- [[Reinventing Organizations]] by [[Frédéric Laloux]] - Teal breakthrough: self-management + wholeness + evolutionary purpose
- [[Principles - Life and Work]] by [[Ray Dalio]] - Idea meritocracy through radical transparency
- [[The Lean Startup]] by Eric Ries - Build-measure-learn experimentation
- [[Life 3.0]] by [[Max Tegmark]] - AI and exponential change context

**Influential People** (4 found):
- [[Frédéric Laloux]] - Organizational evolution theory, studied 12 Teal orgs
- [[Ray Dalio]] - Bridgewater radical transparency, 40 years building idea meritocracy
- [[Nassim Nicholas Taleb]] - Antifragility, embracing disorder for strength
- [[Ken Wilber]] - AQAL integral framework, comprehensive perspectives

**Recommendation:**
Start with [[Reinventing Organizations]] and [[AQAL]] for multi-perspective analysis (structure + culture + individual + system). This is chronic/strategic, use think-understanding-with-frameworks skill for synthesis.
```

**Total time: 12 minutes, comprehensive discovery complete**

## Red Flags - Search More Thoroughly

If you're about to say:
- "Nothing found, creating new note" → Did you start with MoC? Try all 4 entry points?
- "Only found 1 framework" → Did you search multiple domains? Check related areas?
- "Topic not in vault" → Did you check Books? Influential People? Cross-reference?
- "Quick search showed nothing" → Did you read MoC completely?
- "No obvious match" → Try synonyms, related concepts, cross-domain search?

**All mean: Search more thoroughly using all entry points**

## Success Criteria

You discovered knowledge correctly when:

- ✅ Started with MoC Mental Models (not random grep)
- ✅ Found multiple frameworks (not just one)
- ✅ Checked multiple entry points (not just mental models)
- ✅ Followed cross-references (Model → Book → Person)
- ✅ Structured output (user sees what + why + where to start)
- ✅ Appropriate depth (quick for acute, comprehensive for strategic)

## Test Scenarios

### Baseline (RED) - Without this skill

**Scenario:** "User asks: How should I improve team performance?"

**Agent behavior without skill:**
- Generic grep: `Grep "team performance" in vault/`
- Gets 23 random results across all directories
- Doesn't start with MoC (misses organized frameworks)
- Reads file titles, not content
- Reports: "Found some notes on teams"
- User has no idea which frameworks to apply

**Failure modes:**
1. Didn't leverage knowledge graph structure
2. Overwhelming, unstructured results
3. Missed obvious frameworks in MoC
4. No prioritization

### With Skill (GREEN)

**Same scenario with this skill loaded:**

- [ ] Trigger detected: "How should I" → Discovering-relevant-frameworks
- [ ] Starts with MoC Mental Models (60s)
- [ ] Scans Leadership + Business + Psychology sections
- [ ] Finds: Extreme Ownership, AQAL, Radical Transparency, Teal Organizations
- [ ] Supplementary Books search (2 min)
- [ ] Finds: [[Principles]], [[Extreme Ownership]], [[Reinventing Organizations]]
- [ ] Checks Influential People (1 min)
- [ ] Finds: [[Ray Dalio]], [[Jocko Willink]], [[Frédéric Laloux]]
- [ ] Structured output with recommendations

**Output:**
```markdown
## Relevant Knowledge: Team Performance

**Mental Models** (4 found):
- [[Extreme Ownership]] - Leader accountability for all outcomes
- [[AQAL Four Quadrants]] - Individual + collective, interior + exterior
- [[Radical Transparency]] - Idea meritocracy culture
- [[Reinventing Organizations]] - Self-management evolution

**Books** (3 found):
- [[Extreme Ownership]] by [[Jocko Willink]] - Combat leadership principles
- [[Principles]] by [[Ray Dalio]] - Radical transparency, idea meritocracy
- [[Reinventing Organizations]] by [[Frédéric Laloux]] - Teal breakthrough

**Recommendation:**
Acute problem → Start with Extreme Ownership (take accountability).
Strategic/chronic → Use think-understanding-with-frameworks for multi-model synthesis.
```

**Total time: 4 minutes, structured, actionable results**

**Success indicators:**
1. Started with MoC (leveraged structure)
2. Multiple entry points (comprehensive)
3. Structured output (actionable)
4. Prioritized recommendations (guided next steps)

### Refactor (Close Loopholes)

**New rationalizations discovered during testing:**

| Rationalization | Counter Added to Skill |
|-----------------|------------------------|
| "MoC doesn't have my exact keyword" | "Scan DOMAIN sections + descriptions in table" |
| "Too many results to read" | "Prioritize by domain match + MoC featured list" |
| "Just need quick answer, skip comprehensive" | "Quick = MoC scan only. Takes 60s, never skip." |
| "Generic grep is faster" | "MoC scan is FASTER and BETTER. Organized knowledge beats random search." |

## Integration with Other Skills

**Extends:**
- skills/obsidian/vault-discovering-vault-knowledge - Uses same multi-strategy search foundation

**Calls:**
- None (foundational search skill)

**Called by:**
- skills/knowledge-resources/think-solving-with-frameworks - Quick discovery for narrow mode
- skills/knowledge-resources/think-understanding-with-frameworks - Comprehensive discovery for broad mode
- skills/knowledge-resources/think-context-aware-reasoning - Orchestration of discovery

## Remember

**The knowledge graph IS your competitive advantage. Search it structurally.**

Start with MoC. Follow links. Use multiple entry points. Structure your findings.
