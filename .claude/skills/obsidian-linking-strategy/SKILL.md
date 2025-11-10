---
name: Obsidian Linking Strategy
description: Strategic linking prevents orphans and builds knowledge graph through bidirectional connections and MOCs
when_to_use: when deciding what to link, creating connections, or building knowledge graph structure
version: 1.0.0
languages: all
---

# Obsidian Linking Strategy

## Overview

**Links are the value. Notes without links are just files.**

Obsidian's power comes from connections, not content. Strategic linking transforms isolated notes into a knowledge graph that surfaces insights.

**Core principle:** Minimum 3 meaningful links per note. No orphans. Ever.

## The Iron Law

```
NO NOTE WITHOUT 3+ OUTGOING LINKS
```

If you create a note with fewer than 3 links, it's not connected to the knowledge graph. It's a dead end.

**Exceptions:**
- Inbox items (temporary, will be processed)
- Template files (by definition)

## When to Use

**Use this skill when:**
- Creating any new note (decide which 3+ links to add)
- Note feels isolated (add more connections)
- Building MOC or hub note (structure connections)
- Wondering "should I link this?" (decision framework)

**Especially when:**
- Creating in established AREA (link to existing structure)
- Topic has 7+ related notes (consider MOC)
- Building project (link to context, resources, areas)

## Linking Principles

### Principle 1: When to Create Links

**DO link when:**
- ✅ **Concept relationship:** Note explains/uses/extends concept
- ✅ **Context reference:** "See [[X]] for background on this approach"
- ✅ **Hub connection:** Link to MOC or area dashboard
- ✅ **Direct semantic relationship:** Notes are about related aspects of same topic
- ✅ **Dependency:** "This requires [[X]] to work"
- ✅ **Example/Implementation:** "This implements [[Theory X]]"

**DON'T link when:**
- ❌ **Tangential mention:** Passing reference without real relevance
- ❌ **Already in hierarchy:** Parent folder provides context (don't duplicate folder structure in links)
- ❌ **Forced connection:** Linking just to hit 3-link minimum (quality > quantity)

### Principle 2: Bidirectional Linking

**Bidirectional = Link goes both ways with context**

```markdown
# From Note A: Python Learning Project
See [[Persoonlijke Ontwikkeling]] area for broader learning goals.
This project uses tutorials from [[Python Resources]].

# From Note B: Persoonlijke Ontwikkeling
Current active projects:
- [[Python Learning Project]] - Data analysis skills by Dec 2025
- [[Communication Skills]] - Ongoing practice

# From Note C: Python Resources
These tutorials are being used in:
- [[Python Learning Project]] (active)
```

**When bidirectional is needed:**
- Hub note ↔ Spoke notes (Area ↔ Projects)
- Project ↔ Related area (mutual context)
- Implementation ↔ Research (theory-practice connection)
- MOC ↔ Content notes (navigation)

**When one direction is enough:**
- Reference → Source (don't pollute source with all references)
- Specific → General (general note doesn't need to list all specifics)
- Many → One (10 notes linking to concept vs concept listing all 10)

### Principle 3: Link Density Targets

| Note Type | Outgoing Links | Reasoning |
|-----------|---------------|-----------|
| **Daily Note** | 3-8 | Today's topics, related areas, active projects |
| **Project** | 5-10 | Context (area), resources, related projects, stakeholders |
| **Area** | 3-7 | Active projects, key resources, related areas |
| **Resource** | 2-5 | Related resources, source, topic hub |
| **MOC** | 10-30 | Comprehensive topic coverage |
| **Hub Note** | 15-50 | Natural accumulation, don't force |

**Lower bound = MINIMUM. Upper bound = typical, not maximum.**

## Link Patterns

### Pattern 1: Contextual Linking

```markdown
❌ BAD: Bare link list
Related: [[Health]], [[Fitness]], [[Nutrition]]

✅ GOOD: Context around links
This project supports the [[Gezondheid|Health]] area's goal of
maintaining consistent [[Crossfit]] training 3x/week.
See [[Whoop Data]] for recovery tracking integration.
```

**Why better:** Context explains relationship, makes links meaningful

### Pattern 2: Hub-and-Spoke

```markdown
# Hub: Gezondheid (Area)
Ongoing health responsibilities

## Active Projects
- [[Run 5K by November]] - Cardio goal
- [[Improve Sleep Quality]] - Recovery focus

## Sub-Areas
- [[Fitness]] - Training and movement
- [[Nutrition]] - Fuel and energy
- [[Recovery]] - Rest and restoration

## Resources
- [[Whoop Data]] - Metrics and insights
- [[Health Research]] - Science and studies
```

**Each spoke links back:**
```markdown
# Spoke: Run 5K by November
Part of [[Gezondheid]] area's fitness goals.
```

### Pattern 3: MOC (Map of Content)

**Create MOC when topic has 7+ notes**

```markdown
# Python MOC

## Core Learning
- [[Python Fundamentals]]
- [[Data Structures]]
- [[Functions and Methods]]

## Libraries
- [[Pandas for Data Analysis]]
- [[NumPy Arrays]]
- [[Matplotlib Visualization]]

## Projects Using Python
- [[Data Analysis Project]]
- [[Second Brain Pipeline]]

## Resources
- [[Python Learning Resources]]
- [[Python Documentation]]

## Related Topics
- [[Data Science MOC]]
- [[Persoonlijke Ontwikkeling]]
```

**When to create MOC:**
- 7+ notes on topic scattered across vault
- Topic spans PARA categories (Projects + Areas + Resources)
- Need navigation/overview
- Onboarding others to topic

**Hub vs MOC:**
- **Hub:** Natural note others reference (emerges organically)
- **MOC:** Created intentionally for organization
- Hub becomes MOC when you add navigation structure

### Pattern 4: Cross-PARA Linking

```markdown
# PROJECT: Python Data Analysis (01-PROJECTS/)
**Related Area:** [[Persoonlijke Ontwikkeling]]
**Resources:** [[Python Tutorials]], [[DataCamp Course Notes]]
**Past Work:** [[Archive/Python Basics 2023]]

# AREA: Persoonlijke Ontwikkeling (02-AREAS/)
**Active Projects:**
- [[Python Data Analysis]] (by Dec 2025)
- [[Communication Skills]] (ongoing)

# RESOURCE: Python Tutorials (03-RESOURCES/)
**Used in:**
- [[Python Data Analysis]] (current project)
```

**Why important:** Same topic across PARA categories needs connection

## Anti-Patterns (What NOT to Do)

| Anti-Pattern | Symptom | Fix |
|-------------|---------|-----|
| **Over-linking** | Every noun is link, 50+ links in note | Link only meaningful connections |
| **Under-linking** | Note has 0-1 links, orphan in graph | Minimum 3 links always |
| **One-way streets** | Note has 10 backlinks, 0 outgoing | Add context links outward |
| **Link pollution** | High-traffic note has 100+ backlinks | Use MOC as intermediary |
| **Circular only** | A→B→A, no external connections | Connect to broader context |
| **Folder = links** | Rely on folder structure, no wikilinks | Folders are storage, links are navigation |
| **All in frontmatter** | Links only in YAML, not in content | Frontmatter for metadata, content for semantic |

## Link Verification

Before finalizing note:

- [ ] **Count outgoing links: 3+ ?**
  ```bash
  # Count wikilinks in note
  Grep pattern: \[\[.*?\]\]
  path: /path/to/note.md
  output_mode: count
  ```

- [ ] **Verify linked notes exist**
  ```bash
  # For each link [[Note Name]]
  Glob pattern: **/Note Name.md
  # If no results → broken link
  ```

- [ ] **Check link context: meaningful sentences?**
  - Not just: `Related: [[X]], [[Y]], [[Z]]`
  - But: "This implements [[X]]'s approach to Y"

- [ ] **Bidirectional where needed?**
  - Hub notes point back?
  - Related projects cross-reference?

## Finding Link Candidates

**Use skills/obsidian/discovering-vault-knowledge to find:**

```bash
# Find notes about similar topics
Grep pattern: "topic|related-keyword" -i
output_mode: files_with_matches

# Find notes in same Area
Glob pattern: *.md
path: 02-AREAS/Same-Area/

# Find notes with same tags
Grep pattern: #shared-tag
output_mode: files_with_matches

# Find recent related notes
find -name "*.md" -mtime -30 | xargs grep -l "keyword" -i
```

## Special Linking Cases

### Case 1: New Note in Established Area

```markdown
# Creating: Crossfit Workout Log
# Location: 02-AREAS/Gezondheid/Fitness/

MUST link to:
1. Parent area: [[Gezondheid]]
2. Sibling notes: [[Crossfit Benchmarks]], [[Workout History]]
3. Related data: [[Whoop Data]], [[Recovery Notes]]

# Explore existing structure first
Glob pattern: *.md
path: 02-AREAS/Gezondheid/Fitness/
# Found: Crossfit/, Fietsen/, Running/

# Link to discovered structure
```

### Case 2: Project Linking to Context

```markdown
# PROJECT: Python Data Analysis

Required context links:
1. **Parent Area:** [[Persoonlijke Ontwikkeling]]
   - Why: Broader personal development context
2. **Resources:** [[Python Learning Resources]], [[DataCamp Notes]]
   - Why: Materials being used
3. **Related Projects:** [[AI Second Brain]] (future integration)
   - Why: Potential synergy
4. **Past Work:** [[Archive/Python Basics 2023]]
   - Why: Building on previous foundation
```

### Case 3: Daily Note Linking

```markdown
# 2025-10-20 Daily Note

Link to:
- Areas worked on today: [[Gezondheid]], [[POA Work]]
- Projects progressed: [[Python Learning]], [[Family Vacation Planning]]
- New ideas captured: [[Idea: Automated Task Processing]]
- People mentioned: [[Colleagues/Noor]], [[Family/Kai]]

Minimum 3, typically 5-8 for active day
```

## MOC Creation Workflow

When topic reaches 7+ notes:

1. **Create MOC note**
   ```markdown
   # Topic MOC

   Overview of [topic] across the vault.

   Last updated: {{date}}
   ```

2. **Categorize existing notes**
   ```markdown
   ## Core Concepts
   - [[Note 1]]
   - [[Note 2]]

   ## Active Projects
   - [[Project A]]

   ## Resources
   - [[Resource X]]
   ```

3. **Add MOC link to all topic notes**
   ```markdown
   # Individual topic note
   Part of [[Topic MOC]]
   ```

4. **Link MOC to parent Area**
   ```markdown
   # Area note
   Key MOCs in this area:
   - [[Python MOC]]
   - [[Health Tracking MOC]]
   ```

## Red Flags - Improve Linking

If you catch yourself:
- "This note has 0 links but that's fine" → **NO. Minimum 3 links always**
- "I'll add links later" → **NO. Links now or note is orphan**
- "Links are obvious from folder" → **NO. Folders ≠ semantic connections**
- "Too many links = cluttered" → **NO. 10-15 links in project is normal**
- "Just linking everything to hit 3" → **NO. Quality links, not random**

**ALL mean: Add strategic links following this skill.**

## Success Criteria

You know linking worked when:
- No orphan notes in graph view (all have 3+ connections)
- Can navigate topic without folder hierarchy (follow links)
- Related notes surface through backlinks (discoverability)
- MOCs exist for major topics (7+ notes)
- New notes enhance graph density (connections grow)

## Integration with Other Skills

**Called by:**
- skills/obsidian/creating-obsidian-notes (Phase 5 - Linking)

**Calls:**
- skills/obsidian/discovering-vault-knowledge (Finding link candidates)

## Remember

**Links are the knowledge graph. Notes are just nodes. The magic is in the connections.**

3+ meaningful links. Every note. Every time.
