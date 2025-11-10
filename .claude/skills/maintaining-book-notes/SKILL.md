---
name: Maintaining Book Notes
description: Research and document books with consistent structure, automatically create author profiles and extract mental models with full linking
when_to_use: when processing new book, updating after reading, or found book mentioned without note
version: 2.0.0
languages: all
---

# Maintaining Book Notes

## Overview

**Books are SOURCE MATERIAL for mental models, frameworks, and wisdom.**

Consistent documentation enables:
- Fast lookup of "what was that book about?"
- Mental model extraction and attribution
- Author philosophy synthesis
- Cross-book pattern discovery

**Core principle:** Book notes are research artifacts, not reading logs. Focus on WHAT the book teaches, not personal experience reading it.

**NEW in v2.0:** This skill now **automatically executes** the maintaining-influential-people-notes and maintaining-mental-model-notes skills, creating a fully integrated knowledge graph with all links in place. One workflow creates: book note → author profile → mental model notes → all bidirectional links.

## When to Use

**Create/update book note when:**
- Added to Kindle/library (research phase)
- Finished reading (deep notes phase)
- Referenced in conversation/project (quick lookup needed)
- Extracting mental models (attribution required)

**Don't create when:**
- Already exists in vault (search first!)
- Not actually reading it (wishlist ≠ book note)
- Only skimmed or read summary (mark status: researched)

## Process: Research Phase (Before/During Reading)

**IMPORTANT: Use TodoWrite for this checklist**

### Phase 1: Discovery

- [ ] **Search vault for existing note**
  ```bash
  # By title
  Grep pattern: "book-title" -i
  path: 03-RESOURCES/Books/

  # By author
  Grep pattern: "author-name" -i
  path: 03-RESOURCES/Books/

  # Check if author has person note
  Grep pattern: "author-name" -i
  path: 03-RESOURCES/Influential People/
  ```

- [ ] **Decision point:**
  - Found existing note → Update it (don't duplicate)
  - Not found → Continue to Phase 2

### Phase 2: Comprehensive Research

- [ ] **Web research (multiple sources)**
  - Publisher description (Amazon, official website)
  - Professional summaries (Blinkist, Shortform, getAbstract)
  - Critical reviews (Goodreads, academic sources, professional critiques)
  - Author interviews/TED talks about the book
  - Table of contents (reveals structure)

- [ ] **Document research sources**
  - Note where information came from
  - Distinguish: publisher marketing vs critical analysis vs academic review

### Phase 3: Author Integration

- [ ] **Check for author in Influential People**
  ```bash
  Glob pattern: **/*author-name*.md
  path: 03-RESOURCES/Influential People/
  ```

- [ ] **Decision: Author profile exists?**
  - Found existing → Update it with this book (go to Phase 4)
  - Not found → Create author profile (go to Phase 3a)

### Phase 3a: AUTOMATIC Author Profile Creation

**CRITICAL:** This phase automatically executes the maintaining-influential-people-notes skill.

- [ ] **Read the maintaining-influential-people-notes skill**
  ```bash
  Read: ${SUPERPOWERS_SKILLS_ROOT}/skills/knowledge-resources/maintaining-influential-people-notes/SKILL.md
  ```

- [ ] **Announce skill usage**
  "I've read the Maintaining Influential People Notes skill and I'm using it to create [[Author Name]]'s profile."

- [ ] **Execute complete author profile workflow:**
  - Create TodoWrite todos for ALL checklist items from maintaining-influential-people-notes
  - Phase 1: Discovery & Verification (search for existing)
  - Phase 2: Biographical Research (facts, credentials, authority)
  - Phase 3: Philosophy Synthesis (3-5 paragraphs on HOW they think)
  - Phase 4: Critical Analysis (balanced: strengths AND limitations)
  - Phase 5: Integration (link to this book)
  - Phase 6: Quantification (concrete numbers for impact)

- [ ] **Quality check author profile:**
  - [ ] Philosophy section: 3-5 paragraphs (not biography!)
  - [ ] Balanced table: Specific positives AND specific limitations
  - [ ] Quantified impact (numbers provided)
  - [ ] This book listed in "Books in Collection"
  - [ ] Bidirectional link: Author → Book, Book → Author

- [ ] **Mark author profile as complete** before continuing to Phase 4

### Phase 4: Content Creation

- [ ] **Create frontmatter**
  ```yaml
  ---
  type: resource
  category: book
  status: researched | reading | completed
  created: YYYY-MM-DD
  author: [[Author Name]]
  section: [Business, Psychology, Philosophy, Technology, Health, Biography, Finance]
  rating: memorable | valuable | reference
  tags: [book, domain-tags, author-name]
  ---
  ```

- [ ] **Write "What This Book Is About" section**
  - 3-5 paragraphs comprehensive summary
  - Paragraph 1: Core thesis in plain language
  - Paragraphs 2-4: Key frameworks, concepts, unique contributions
  - Paragraph 5: Why significant/influential (impact, reception)
  - **NOT personal opinion** (that goes in Personal Notes section at end)

- [ ] **Create standard sections:**
  ```markdown
  ## 🎯 What This Book Is About
  [3-5 paragraphs comprehensive summary]

  ## 🔗 Related Notes
  - [[Author Name]] - Person profile
  - [[Related Book 1]]
  - [[Related Mental Model]]

  ## 📚 Context
  This book appears in [collection/category]

  ## 🔖 Research Notes
  - Research conducted: YYYY-MM-DD
  - Sources: [list of sources used]
  - Key concepts verified across multiple sources

  ## 📝 Personal Notes & Reflections
  [Optional: Your insights, applications, how you use this]
  ```

## Phase 5: Mental Model Identification

**CRITICAL:** Books often contain 3-5 extractable mental models

- [ ] **Identify extractable mental models** (look for):
  - Frameworks with names (5-Step Process, AQAL, Extreme Ownership)
  - Decision tools (Prioritize and Execute, First Principles)
  - Conceptual lenses (Antifragile, Circle of Influence)
  - Thinking patterns author explicitly teaches

- [ ] **Criteria for extraction:**
  - ✅ Has a name or can be named
  - ✅ Universal (not book-specific example)
  - ✅ Reusable across domains
  - ✅ Worth referencing independently
  - ❌ Don't extract: one-time examples, generic advice

- [ ] **Create list of mental models to extract** (typically 3-5 models)

## Phase 5a: AUTOMATIC Mental Model Extraction

**CRITICAL:** This phase automatically executes the maintaining-mental-model-notes skill FOR EACH identified mental model.

- [ ] **Read the maintaining-mental-model-notes skill**
  ```bash
  Read: ${SUPERPOWERS_SKILLS_ROOT}/skills/knowledge-resources/maintaining-mental-model-notes/SKILL.md
  ```

- [ ] **For EACH mental model identified in Phase 5:**

  **Step 1: Check if already exists**
  - [ ] Search for existing note:
    ```bash
    Grep pattern: "model-name" -i
    path: 03-RESOURCES/Mental Models/
    ```

  **Step 2a: If model exists:**
  - [ ] Read existing note
  - [ ] Update with this book as additional source
  - [ ] Add new insights if this book provides them
  - [ ] Ensure bidirectional link: Model → Book, Book → Model

  **Step 2b: If new model - CREATE IT AUTOMATICALLY:**

  - [ ] **Announce skill usage**
    "I've read the Maintaining Mental Model Notes skill and I'm using it to create [[Mental Model Name]]."

  - [ ] **Execute complete mental model workflow:**
    - Create TodoWrite todos for ALL checklist items from maintaining-mental-model-notes
    - Phase 1: Verification (is this really a mental model?)
    - Phase 2: Research (web search, original sources, critics)
    - Phase 3: Content Creation (all 9 required sections)
    - Phase 4: Integration (link to book, author, MoC, related models)

  - [ ] **Quality check mental model note:**
    - [ ] All 9 sections present
    - [ ] Limitations section: 5+ specific items (equal weight to strengths)
    - [ ] 3 examples from DIFFERENT domains
    - [ ] Creator attribution: Link to [[Author Name]]
    - [ ] Source attribution: Link to this [[Book Title]]
    - [ ] Added to [[MoC Mental Models]]
    - [ ] Cross-referenced from this book note

  - [ ] **Mark mental model as complete** before moving to next model

- [ ] **After ALL models extracted:**
  - [ ] Update book note with "Key Mental Models Extracted" section:
    ```markdown
    ## Key Mental Models Extracted
    - [[Mental Model 1]] - Brief description
    - [[Mental Model 2]] - Brief description
    - [[Mental Model 3]] - Brief description
    ```

## Phase 6: Complete Integration & Linking

**CRITICAL:** Ensure ALL bidirectional links are in place across the knowledge graph.

- [ ] **Verify book note links:**
  - [ ] Links to [[Author Name]]
  - [ ] Links to all extracted [[Mental Models]]
  - [ ] Links to related books (similar themes)
  - [ ] Links to [[Books MOC]]

- [ ] **Verify author profile links:**
  - [ ] Author profile links to this book (in "Books in Collection")
  - [ ] Author profile links to all mental models they created
  - [ ] This book links to author profile

- [ ] **Verify mental model links:**
  - [ ] Each mental model links to this book as source
  - [ ] Each mental model links to [[Author Name]] as creator
  - [ ] Each mental model added to [[MoC Mental Models]]
  - [ ] This book links to each mental model

- [ ] **Update [[MoC Mental Models]]:**
  - [ ] Add all new models to comprehensive table
  - [ ] Include this book as source for each
  - [ ] Update statistics (total count)

- [ ] **Final cross-reference check:**
  - [ ] Book → Mental Models (extracted from) ✅
  - [ ] Mental Models → Book (source) ✅
  - [ ] Book → Author (written by) ✅
  - [ ] Author → Book (bibliography) ✅
  - [ ] Author → Mental Models (created) ✅
  - [ ] Mental Models → Author (creator) ✅
  - [ ] Book → Related Books (similar themes) ✅

## Required Frontmatter Fields

```yaml
---
type: resource                    # Always "resource"
category: book                    # Always "book"
status: researched | reading | completed
created: YYYY-MM-DD
author: [[Author Name]]           # Wikilink to person note
section: [Category]               # Business, Psychology, etc.
rating: memorable | valuable | reference
tags: [book, domain-tags, author-name]
---
```

**Status meanings:**
- `researched`: Web research completed, not yet read
- `reading`: Currently reading
- `completed`: Finished reading, full notes added

**Rating meanings:**
- `memorable`: Life-changing, frequently reference
- `valuable`: Important insights, occasional reference
- `reference`: Useful information, lookup when needed

## Common Mistakes

| Mistake | Impact | Fix |
|---------|--------|-----|
| **Created before searching** | Duplicates, wasted effort | ALWAYS search first (title + author) |
| **Skipped research phase** | Shallow notes, missing context | Web research before/during reading |
| **No author profile** | Missing philosophical context | AUTOMATIC: Phase 3a creates it if missing |
| **Didn't extract mental models** | Models trapped in book note | AUTOMATIC: Phase 5a extracts 3-5 standalone notes |
| **Skipped automatic phases** | Disconnected knowledge graph | Execute Phase 3a and 5a FULLY before marking complete |
| **Didn't read related skills** | Shallow execution | MUST read maintaining-influential-people-notes and maintaining-mental-model-notes |
| **Missing bidirectional links** | Orphaned notes | Phase 6 verifies ALL links: Book ↔ Author ↔ Models |
| **Personal reading log style** | Not reference material | Focus on WHAT book teaches, not your experience |
| **Only 1-2 paragraph summary** | Can't remember what book covered | 3-5 comprehensive paragraphs |
| **No sources documented** | Can't verify later | List research sources in Research Notes |
| **Wrong status** | Confusion about completion | researched ≠ reading ≠ completed |
| **Incomplete author profile** | Unbalanced analysis | Phase 3a: 3-5 paragraphs philosophy + balanced limitations |
| **Shallow mental models** | Missing critical sections | Phase 5a: All 9 sections + 5+ limitations per model |

## Example: Complete Book Note

**File:** `03-RESOURCES/Books/Principles - Life and Work.md`

```markdown
---
type: resource
category: book
status: researched
created: 2025-10-20
author: [[Ray Dalio]]
section: Business
rating: memorable
tags: [book, business, principles, management, radical-transparency]
---

# 📖 Principles - Life and Work

**Author:** Ray Dalio
**Category:** [[Books MOC]] > Business & Leadership
**Status:** Content researched, not yet read
**Source:** [[Kindle Books on Amazon.nl account]]

## 🎯 What This Book Is About

Ray Dalio's "Principles: Life and Work" is a comprehensive guide to the unconventional principles he developed and refined over four decades while building Bridgewater Associates from a two-bedroom New York apartment operation into the world's largest hedge fund. The book is structured in three parts: Dalio's personal journey (1949-2017), his Life Principles, and his Work Principles, containing over 500 actionable guidelines that treat life, management, economics, and investing as systems that can be understood like machines.

At the core of Dalio's philosophy is the concept that principles are fundamental truths serving as the foundation for behavior that gets you what you want out of life. His approach emerged from painful failure—in 1982, he nearly lost everything after misjudging the global economy and had to borrow $4,000 from his father for bills. This experience birthed his famous equation: **Pain + Reflection = Progress**...

[Continue with 3-5 more paragraphs as shown in vault example]

## Key Mental Models Extracted

- [[5-Step Process]] - Goals → Problems → Diagnosis → Design → Execute
- [[Pain + Reflection = Progress]] - Learning framework
- [[Radical Truth & Radical Transparency]] - Organizational culture
- [[Idea Meritocracy]] - Decision-making system
- [[Believability-Weighted Decisions]] - Expertise weighting

## 🔗 Related Notes

- [[Ray Dalio]] - Author profile
- [[Principles for Dealing with the Changing World Order]] - Dalio's other book
- [[Big Debt Crises]] - Related Dalio book
- [[Books MOC]] - All books

## 📚 Context

This book appears in the "[[Kindle Books on Amazon.nl account]]" collection under **Business, Leadership & Management** as one of the "Most Memorable" books.

## 🔖 Research Notes

- Research conducted: 2025-10-20
- Sources: Amazon, principles.com, book summaries, CNBC articles
- Key concepts verified across multiple sources for accuracy

## 📝 Personal Notes & Reflections

*Space for personal insights after reading*

---
*This is a content research note. Reading notes will be added when book is actually read.*
```

## Red Flags - STOP and Reconsider

If you're about to:
- Create book note without searching → STOP. Check for duplicates first
- Skip Phase 3a (author profile creation) → STOP. Execute maintaining-influential-people-notes skill
- Skip Phase 5a (mental model extraction) → STOP. Execute maintaining-mental-model-notes skill for EACH model
- Skip reading related skills → STOP. MUST read maintaining-influential-people-notes and maintaining-mental-model-notes
- Create shallow author profile → STOP. 3-5 paragraphs philosophy + balanced limitations required
- Create shallow mental models → STOP. All 9 sections + 5+ limitations per model required
- Skip Phase 6 (linking verification) → STOP. Verify ALL bidirectional links
- Write personal review style → STOP. Focus on what book teaches, not opinion
- Create 1-paragraph summary → STOP. Write 3-5 comprehensive paragraphs
- Mark as "completed" when only researched → STOP. Use accurate status

**All mean: Review this skill before proceeding**

## Test Scenarios

### Baseline (RED) - Without this skill

**Scenario:** Process "Principles: Life and Work" by Ray Dalio

**Agent behavior without skill:**
- Doesn't search first (creates duplicate if one exists)
- Minimal summary: "This book is about Ray Dalio's principles for life and business"
- No author profile check (misses existing [[Ray Dalio]] note)
- Mental models mentioned in summary but not extracted
- Frontmatter incomplete (missing rating, wrong status)
- No research sources documented

**Failure modes:**
1. Potential duplicate creation
2. Shallow documentation
3. Disconnected from knowledge graph
4. Mental models not accessible independently
5. No author profile created
6. No mental model notes created

### With Skill v2.0 (GREEN) - AUTOMATIC WORKFLOW

**Same scenario with this skill loaded:**

**Phase 1-2: Discovery & Research**
- [ ] Searches first: `Grep "principles" + "dalio"` in Books/
- [ ] Found existing or creates new
- [ ] Comprehensive web research (Amazon, principles.com, summaries, critiques)

**Phase 3-3a: Author Profile (AUTOMATIC)**
- [ ] Checks [[Ray Dalio]] in Influential People
- [ ] NOT found → Phase 3a triggered automatically
- [ ] Reads maintaining-influential-people-notes skill
- [ ] Announces: "I've read the Maintaining Influential People Notes skill..."
- [ ] Creates TodoWrite todos for complete author profile workflow
- [ ] Executes all 6 phases of maintaining-influential-people-notes:
  - Biographical research (hedge fund founder, $150B AUM, net worth)
  - Philosophy synthesis (3-5 paragraphs on principles-based thinking)
  - Critical analysis (balanced: strengths AND limitations)
  - Quantification (specific numbers documented)
  - Balanced table entry (radical transparency benefits vs 18mo adaptation requirement)
- [ ] Quality check: Philosophy 3-5 paragraphs ✅, Limitations balanced ✅
- [ ] Links book to author profile bidirectionally

**Phase 4: Book Note Creation**
- [ ] 3-5 paragraph summary: core thesis, pain+reflection, radical transparency, 5-step process, impact
- [ ] Proper frontmatter: status=researched, author=[[Ray Dalio]], rating=memorable
- [ ] Research sources documented

**Phase 5-5a: Mental Model Extraction (AUTOMATIC)**
- [ ] Identifies 5 extractable mental models: 5-Step Process, Pain+Reflection=Progress, Radical Transparency, Idea Meritocracy, Believability-Weighted Decisions
- [ ] For EACH model → Phase 5a triggered automatically:
  - Reads maintaining-mental-model-notes skill
  - Announces: "I've read the Maintaining Mental Model Notes skill and I'm using it to create [[5-Step Process]]"
  - Creates TodoWrite todos for complete mental model workflow
  - Executes all 4 phases of maintaining-mental-model-notes:
    - Verification (is this a mental model? Yes)
    - Research (web search, original sources, critics)
    - Content Creation (all 9 sections, 5+ limitations, 3 examples)
    - Integration (link to book, author, MoC, related models)
  - Quality check per model: All 9 sections ✅, 5+ limitations ✅, 3 examples ✅
- [ ] Repeats for all 5 mental models
- [ ] Updates book note with "Key Mental Models Extracted" section

**Phase 6: Complete Integration (AUTOMATIC)**
- [ ] Verifies ALL bidirectional links:
  - Book → [[Ray Dalio]] ✅
  - [[Ray Dalio]] → Book (in "Books in Collection") ✅
  - Book → [[5-Step Process]], [[Radical Transparency]], etc. ✅
  - Each mental model → Book (source) ✅
  - Each mental model → [[Ray Dalio]] (creator) ✅
  - [[Ray Dalio]] → All mental models (in "Key Concepts") ✅
- [ ] Updates [[MoC Mental Models]] with all 5 frameworks
- [ ] No orphaned notes

**Success indicators:**
1. No duplicates (searched first) ✅
2. Rich book summary (3-5 paragraphs) ✅
3. Complete author profile created automatically (3-5 paragraphs philosophy + balanced analysis) ✅
4. 5 mental model notes created automatically (all with 9 sections, 5+ limitations each) ✅
5. Fully integrated knowledge graph (all bidirectional links verified) ✅
6. Accurate metadata (status, rating) ✅

**Outcome:** One workflow created 7 notes (1 book + 1 author + 5 models) with complete integration.

### Refactor (Close Loopholes)

**New rationalizations discovered during testing:**

| Rationalization | Counter Added to Skill (v2.0) |
|-----------------|------------------------|
| "I'll research it after reading" | "Research phase FIRST - informs what to pay attention to" |
| "Mental models are obvious from summary" | "Phase 5a AUTOMATIC: Execute maintaining-mental-model-notes for EACH model" |
| "Author isn't influential enough for profile" | "Phase 3a AUTOMATIC: Execute maintaining-influential-people-notes" |
| "One paragraph summary is enough" | "3-5 paragraphs minimum - fast lookup needs detail" |
| "I'll link to author later" | "Phase 6 AUTOMATIC: Verify ALL bidirectional links before complete" |
| "I'll create mental models later" | "Phase 5a AUTOMATIC: Create ALL mental models before proceeding" |
| "Author profile can be quick" | "Phase 3a: Full workflow required (3-5 paragraphs + balanced analysis)" |
| "Mental models can be brief" | "Phase 5a: All 9 sections + 5+ limitations per model required" |
| "I'll skip automatic phases to save time" | "Automatic phases NOT optional - execute FULLY or knowledge graph breaks" |

## Success Criteria

You followed this skill correctly when:

**Book Note:**
- ✅ Searched for duplicates first (no duplicate creation)
- ✅ Comprehensive 3-5 paragraph "What This Book Is About"
- ✅ Complete frontmatter with accurate status
- ✅ Research sources documented
- ✅ "Key Mental Models Extracted" section lists all models

**Author Profile (Phase 3a - AUTOMATIC):**
- ✅ Read maintaining-influential-people-notes skill
- ✅ Created/updated author profile with complete workflow
- ✅ Philosophy section: 3-5 paragraphs (HOW they think, not biography)
- ✅ Balanced table: Specific positives AND specific limitations
- ✅ Quantified impact (numbers provided)
- ✅ This book listed in author's "Books in Collection"

**Mental Models (Phase 5a - AUTOMATIC):**
- ✅ Read maintaining-mental-model-notes skill
- ✅ Identified 3-5 extractable mental models
- ✅ For EACH model: Created/updated with complete workflow
- ✅ All 9 sections present per model
- ✅ Limitations section: 5+ specific items per model
- ✅ 3 examples from different domains per model
- ✅ Creator attribution: Links to [[Author Name]]
- ✅ Source attribution: Links to this [[Book Title]]

**Integration (Phase 6 - AUTOMATIC):**
- ✅ [[MoC Mental Models]] updated with all extracted frameworks
- ✅ ALL bidirectional links verified:
  - Book ↔ Author ✅
  - Book ↔ Mental Models ✅
  - Author ↔ Mental Models ✅
  - Mental Models ↔ MoC ✅
- ✅ No orphaned notes (everything connected)

**Quality Gates:**
- ✅ No shortcuts taken on automatic phases
- ✅ All TodoWrite checklists completed for each skill
- ✅ Quality checks passed for author profile and each mental model

## Integration with Other Skills

**Automatically Executes (v2.0):**
- skills/knowledge-resources/maintaining-influential-people-notes - AUTOMATIC in Phase 3a
- skills/knowledge-resources/maintaining-mental-model-notes - AUTOMATIC in Phase 5a (for EACH model)

**Calls:**
- skills/obsidian/creating-obsidian-notes - For note creation
- skills/obsidian/discovering-vault-knowledge - For duplicate checking

**Called by:**
- skills/knowledge-resources/discovering-relevant-frameworks - Finding books on topic
- skills/knowledge-resources/context-aware-reasoning - Researching domain

**Workflow Chain:**
```
maintaining-book-notes (this skill)
  ↓
  ├─→ Phase 3a: maintaining-influential-people-notes (AUTOMATIC)
  │   └─→ Creates/updates author profile with full workflow
  ↓
  ├─→ Phase 5a: maintaining-mental-model-notes (AUTOMATIC, per model)
  │   └─→ Creates 3-5 mental model notes with full workflow
  ↓
  └─→ Phase 6: Verifies ALL bidirectional links
      └─→ Book ↔ Author ↔ Mental Models ↔ MoC
```

## Remember

**Books are source material. Extract the frameworks, link the knowledge graph, enable discovery.**

**v2.0:** One workflow creates everything: book note → author profile → mental model notes → all links.

Research thoroughly. Execute automatic phases completely. Connect the dots.
