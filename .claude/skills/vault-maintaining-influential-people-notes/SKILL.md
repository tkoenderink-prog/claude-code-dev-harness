---
name: Maintaining Influential People Notes
description: Create person profiles with philosophy, achievements, AND critical limitations in balanced analysis
when_to_use: when processing book by new author, referencing thought leader, or creating mental model with specific creator
version: 1.0.0
languages: all
---

# Maintaining Influential People Notes

## Overview

**Influential people notes provide CONTEXT for their frameworks and wisdom.**

Critical requirement: **Balanced analysis** - positive impressions AND limitations/concerns with equal rigor.

**Core principle:** Every thinker has blind spots. Document strengths and weaknesses critically. Hero worship helps no one.

## When to Use

**Create person note when:**
- Read book by author not in vault
- Creating mental model attributed to specific person
- Referenced thought leader in conversation
- Building knowledge graph connections
- Processing influential person's work

**Don't create when:**
- Person only mentioned in passing
- Not actually influential in your knowledge domain
- Already have comprehensive note (update instead)

## Required Structure

### Frontmatter Template

```yaml
---
type: resource
category: influential-person
status: researched | in-depth
books_in_collection: [count]
created: YYYY-MM-DD
tags: [author, influential-person, domain-tags, person-name]
---
```

**Status meanings:**
- `researched`: Basic research completed
- `in-depth`: Read multiple works, deep understanding

### Content Sections (All Required)

**1. Header Block**
```markdown
# [Person Name] - [Primary Role/Contribution]

**Profession:** [What they do/did]
**Born:** [Year, Location] or [Year - Year] if deceased
**Known For:** [Key contribution in one line]
**Related:** [[Books MOC]] | [[MoC Influential People]]
```

**2. Philosophy & Core Principles** (3-5 paragraphs)
- Comprehensive worldview synthesis
- What they believe and teach
- How they think about problems
- Integration of their major works
- Core principles that guide their approach
- **NOT just biography - synthesize their THINKING**

**3. Books in Collection** (If applicable)
For each book:
```markdown
### [Book Title] (Year)
[2-3 paragraph summary of what this book teaches]

**Link:** [[Book Title]]
```

**4. Notable Works & Resources (Not in Collection)**
- TED talks, YouTube channels
- Papers, articles, blog posts
- Courses, programs
- Other significant outputs

**5. External Links**
- Official website
- Social media (LinkedIn, Twitter, etc.)
- Key talks/interviews
- Wikipedia or official biography

**6. Impact & Legacy**
- **QUANTIFIED where possible:**
  - Books sold
  - Companies using framework
  - Awards/recognition
  - Proven results
- Influence on field
- What changed because of their work

**7. Key Concepts & Contributions** (Bullet list)
- Mental models they created/popularized
- Frameworks and tools
- Key ideas (with links to mental model notes)
- Original contributions vs synthesis of others

**8. Related Vault Notes**
- [[Book 1]], [[Book 2]] - Their works
- [[Mental Model 1]], [[Mental Model 2]] - Frameworks they created
- [[Related Person 1]] - Influenced by / Influenced
- [[Books MOC]], [[MoC Influential People]] - Hubs

**9. Personal Notes & Reflections**
- Your synthesis
- How you use their work
- Questions or critiques you have

### CRITICAL: Balanced Quick Reference Table

**MANDATORY for fast scanning:**

```markdown
| Person | Short Description | Positive Impression | Limitations/Worries |
|--------|------------------|---------------------|-------------------|
| [[Person Name]] | [2-5 words] | [Specific strengths, concrete] | [Specific concerns, evidence-based] |
```

**Requirements for table:**
- **Positive Impression:** Concrete, specific strengths (NOT generic praise)
- **Limitations/Worries:** Specific concerns with examples (NOT vague "some disagree")
- **Equal weight:** Both columns should have similar depth
- **Evidence-based:** Cite specific issues, not assumptions

## Research Methodology

**IMPORTANT: Use TodoWrite for this checklist**

### Phase 1: Discovery & Verification

- [ ] **Search vault for existing note**
  ```bash
  # By name
  Grep pattern: "person-name" -i
  path: 03-RESOURCES/Influential People/

  # Check if mentioned in books
  Grep pattern: "person-name" -i
  path: 03-RESOURCES/Books/
  ```

- [ ] **Decision: Create new or update existing?**
  - Found → Update and expand
  - Not found → Create new

### Phase 2: Biographical Research

- [ ] **Basic facts**
  - Wikipedia, official bio
  - Career timeline
  - Education, background
  - Current activities

- [ ] **Credentials & authority**
  - What qualifies them to teach?
  - Track record and experience
  - Formal credentials vs practical experience
  - Proven results (quantified)

### Phase 3: Philosophy Synthesis

- [ ] **Primary sources**
  - Read/watch at least 2-3 different works
  - Books, talks, articles
  - Look for consistent themes
  - Identify core principles

- [ ] **Philosophical framework**
  - What do they believe about reality?
  - How do they approach problems?
  - What values guide their thinking?
  - What questions drive their work?

- [ ] **Synthesis (3-5 paragraphs)**
  - Not just biography
  - Capture HOW they think
  - Integrate across their works
  - Show patterns in their approach

### Phase 4: Critical Analysis

**CRITICAL:** This is what separates useful notes from fan pages

- [ ] **Academic/professional critiques**
  - What do critics say?
  - Peer reviews and rebuttals
  - Academic analysis if applicable
  - Professional disagreements

- [ ] **Limitations research**
  - Where has approach failed?
  - What does it overlook?
  - Cultural/temporal limitations
  - Scope boundaries

- [ ] **Controversies**
  - Known controversies or issues
  - Ethical concerns
  - Changed positions over time
  - Conflicts of interest

- [ ] **Document specific limitations:**
  - NOT: "Some people disagree"
  - ✅ YES: "Requires 18-month adaptation period, not all personalities suit, expensive programs ($10K-100K)"
  - NOT: "Approach has limits"
  - ✅ YES: "Works best in tech startups, less applicable in regulated industries, requires significant capital"

### Phase 5: Integration & Cross-Reference

- [ ] **Link all their books**
  - Update each book note to link to person
  - Person note links to all books

- [ ] **Link mental models created**
  - Which frameworks did they create/popularize?
  - Update each mental model note with creator link
  - Person note lists all their frameworks

- [ ] **Related thinkers**
  - Who influenced them?
  - Who did they influence?
  - Who offers complementary perspectives?
  - Who offers contrasting perspectives?

### Phase 6: Quantification

- [ ] **Find concrete numbers:**
  - Books sold (millions)
  - Companies using framework (hundreds/thousands)
  - Revenue/valuation achieved
  - Awards and recognition
  - Years of experience
  - Size of community/following

**Quantification makes impact tangible, not just claimed.**

## Common Mistakes

| Mistake | Impact | Fix |
|---------|--------|-----|
| **Only positive framing** | Uncritical hero worship, blind application | Equal weight to limitations |
| **Limitations too vague** | Not actionable ("some disagree") | Specific concerns with examples |
| **Skipped critical research** | Missing important context | Read critics, not just fans |
| **No quantification** | Vague impact claims | Numbers: sold, using, achieved |
| **Missing cross-references** | Isolated from knowledge graph | Link ALL books, models, people |
| **Biography not philosophy** | Know their life, not their thinking | Synthesize HOW they think |
| **Created before reading their work** | Shallow understanding | Read 2-3 works first |
| **Uncritical of controversies** | Miss important warnings | Research controversies thoroughly |

## Example: Complete Person Note

**File:** `03-RESOURCES/Influential People/Ray Dalio.md`

```markdown
---
type: resource
category: influential-person
status: in-depth
books_in_collection: 3
created: 2025-10-21
tags: [author, influential-person, investing, economics, principles, bridgewater]
---

# Ray Dalio - Investor, Author, Radical Transparency Pioneer

**Profession:** Founder of Bridgewater Associates (world's largest hedge fund)
**Born:** 1949, Jackson Heights, New York
**Net Worth:** $19+ billion
**Known For:** Principles-based thinking, radical transparency, economic cycle analysis
**Related:** [[Books MOC]] | [[MoC Influential People]]

## 🎯 Philosophy & Core Principles

Ray Dalio's philosophy represents one of the most comprehensive frameworks for understanding reality, making decisions, and building organizations in modern business thought. At its foundation is the belief that life operates according to discoverable principles—fundamental truths that serve as the foundation for behavior and achievement. This principles-based approach emerged from a painful personal failure in 1982, when Dalio nearly lost everything after misjudging the global economy and had to borrow $4,000 from his father. This humbling experience birthed his famous equation: **Pain + Reflection = Progress**...

[Continue with 3-5 paragraphs as in vault example]

## 📚 Books in Collection

### 1. Principles: Life and Work (2017)
A comprehensive guide to the unconventional principles Dalio developed while building Bridgewater Associates into the world's largest hedge fund...

**Link:** [[Principles - Life and Work]]

[Continue with other books]

## 🌐 Notable Works & Resources (Not in Collection)

### Videos & Animated Content
1. **"How the Economic Machine Works"** - 30-minute animated video...

[Continue as in vault example]

## 🔗 External Links
- **Official Website:** [principles.com](https://www.principles.com)
[etc.]

## 📊 Impact & Legacy
- **Founded:** Bridgewater Associates (1975) - $150B+ AUM
- **Recognition:** TIME's 100 Most Influential People
- **Downloads:** "Principles" downloaded 3M+ times before publication
[etc.]

## 🎓 Key Concepts & Contributions
- [[Radical Truth & Radical Transparency]]
- [[Idea Meritocracy]]
- [[Pain + Reflection = Progress]]
- [[5-Step Process]]
[etc.]

## 🔗 Related Vault Notes
- [[Principles - Life and Work]], [[Big Debt Crises]], [[Principles for Dealing with the Changing World Order]]
- [[5-Step Process]], [[Radical Transparency]], [[Idea Meritocracy]]
- [[Books MOC]], [[MoC Influential People]]

## 📝 Personal Notes & Reflections
*Your synthesis of their work*
```

**CRITICAL - Balanced Table Entry:**

```markdown
| Person | Short Description | Positive Impression | Limitations/Worries |
|--------|------------------|---------------------|-------------------|
| [[Ray Dalio]] | Bridgewater founder, principles-based thinking | Systematic approach to reality, radical transparency creates trust-based culture, debt cycle framework predicted crises, 500+ documented principles | Radical transparency requires 18mo adaptation, not all personalities fit, believability hierarchy can become rigid, works best in specific cultures |
```

## Red Flags - STOP and Reconsider

If you're about to:
- Only write positive description → STOP. Add critical limitations
- Write "some disagree with approach" → STOP. Be specific about what concerns
- Skip quantification → STOP. Find concrete numbers for impact
- Create without reading their work → STOP. Read 2-3 sources first
- Miss cross-references to books/models → STOP. Link ALL related content
- Write biography not philosophy → STOP. Synthesize HOW they think

**All mean: Review this skill before proceeding**

## Test Scenarios

### Baseline (RED) - Without this skill

**Scenario:** Create profile for Ray Dalio after reading "Principles"

**Agent behavior without skill:**
- Philosophy section: 1 paragraph, mostly biographical facts
- Positive impression: "Innovative thinker, successful investor, great teacher"
- Limitations: "Some people find radical transparency difficult to adapt to"
- No quantification (missing $150B AUM, 3M downloads, etc.)
- Doesn't link to mental models he created
- Missing critical analysis (no mention of 18-month adaptation period, cultural fit requirements)
- Created without comprehensive research (only one book read)

**Failure modes:**
1. Uncritical hero worship
2. Vague limitations (not actionable)
3. Missing context (no quantification)
4. Disconnected from knowledge graph

### With Skill (GREEN)

**Same scenario with this skill loaded:**

- [ ] Searches first: `Grep "dalio"` in Influential People/
- [ ] Comprehensive research: Wikipedia, principles.com, interviews, critiques
- [ ] Philosophy synthesis: 3-5 paragraphs integrating multiple works
- [ ] Specific positive impression: "Systematic reality-based approach, radical transparency creates idea meritocracy, debt cycle framework predicted 2008 crisis, 500+ documented principles at Bridgewater"
- [ ] Specific limitations: "Radical transparency requires 18-month adaptation, not all personalities suit, believability hierarchy can become authoritarian, culture works in finance but difficult in other domains"
- [ ] Quantification: "$150B AUM, $19B net worth, 3M+ downloads, TIME 100, founded 1975"
- [ ] Links to 3 books, 5+ mental models created
- [ ] Critical analysis: Read both proponents AND critics
- [ ] Cross-references complete: Person ↔ Books ↔ Mental Models
- [ ] Balanced table entry with equal-weight positive/limitations

**Success indicators:**
1. Balanced critical analysis
2. Specific limitations with evidence
3. Comprehensive philosophy synthesis
4. Rich quantification
5. Integrated into knowledge graph

### Refactor (Close Loopholes)

**New rationalizations discovered during testing:**

| Rationalization | Counter Added to Skill |
|-----------------|------------------------|
| "Limitations seem harsh/critical" | "Critical analysis IS the value. Every thinker has blindspots." |
| "Positive impression is longer than limitations" | "Balance word count - equal weight required" |
| "Everyone knows who Ray Dalio is" | "Document anyway - vault is for future you" |
| "One book is enough to understand them" | "Read 2-3 works minimum for synthesis" |
| "Controversies are off-topic" | "Controversies reveal important context and warnings" |

## Success Criteria

You followed this skill correctly when:

- ✅ Philosophy section: 3-5 paragraphs synthesizing their thinking
- ✅ Balanced table: Specific positives AND specific limitations
- ✅ Limitations equal weight to strengths (word count similar)
- ✅ Quantified impact (numbers for books, followers, companies, etc.)
- ✅ Cross-referenced ALL books and mental models
- ✅ Read critics, not just fans (critical analysis)
- ✅ Proper location: 03-RESOURCES/Influential People/

## Integration with Other Skills

**Calls:**
- skills/obsidian/creating-obsidian-notes - For note creation
- skills/obsidian/discovering-vault-knowledge - For duplicate checking

**Called by:**
- skills/knowledge-resources/maintaining-book-notes - When processing author
- skills/knowledge-resources/maintaining-mental-model-notes - When attributing creator
- skills/knowledge-resources/discovering-relevant-frameworks - Finding thought leaders

## Remember

**Every thinker has blind spots. Balanced critical analysis > hero worship.**

Document their philosophy, quantify their impact, and honestly assess their limitations.
