---
name: Discovering Vault Knowledge
description: Multi-strategy search finds existing knowledge before claiming ignorance or creating duplicates
when_to_use: when exploring a topic, before writing new content, or when user asks "what do I know about X"
version: 1.0.0
languages: all
---

# Discovering Vault Knowledge

## Overview

**Search multiple ways. The vault knows more than you think.**

Single-strategy search misses 60-80% of relevant content. Thorough discovery prevents duplicates and surfaces unexpected connections.

**Core principle:** If you searched only one way (filename OR content OR links OR tags), you haven't really searched.

## When to Use

**Before claiming:**
- "You don't have any notes on X"
- "This topic isn't in your vault"
- "I couldn't find anything about X"

**Before creating:**
- New note on any topic
- New project or area
- Duplicate research

**When exploring:**
- User asks "show me everything about X"
- Research phase for project
- Looking for connections between topics

## Multi-Strategy Search Framework

### Strategy 1: Direct Content Search

**What it finds:** Notes mentioning the topic anywhere in content

```bash
# Case-insensitive content search
Grep pattern: "topic-keyword" -i
output_mode: files_with_matches
path: /path/to/vault

# Try variations
Grep pattern: "variation|alternate|synonym" -i
```

**Example:**
```bash
# Searching for "Python"
Grep pattern: "python|py|pandas|numpy" -i
```

### Strategy 2: Wikilink Search

**What it finds:** Notes explicitly linking to topic

```bash
# Find all links TO a topic
Grep pattern: \[\[.*topic.*(\|[^\]]+)?\]\] -i
output_mode: files_with_matches

# Exact link target
Grep pattern: \[\[Topic Name(\|[^\]]+)?\]\]
```

**Why needed:** Content search misses notes that link without mentioning keyword

### Strategy 3: Tag Search

**What it finds:** Notes tagged with topic

```bash
# Find specific tag
Grep pattern: #topic-tag
output_mode: files_with_matches

# Find tag variations
Grep pattern: #(topic|related-topic)
```

### Strategy 4: Filename Pattern Search

**What it finds:** Notes with topic in filename

```bash
# Glob search (fast, filename only)
Glob pattern: **/*topic*.md
path: /path/to/vault

# Case variations
Glob pattern: **/*{Topic,topic,TOPIC}*.md
```

**Why needed:** Well-named notes may not mention keyword in first paragraph

### Strategy 5: PARA Cross-Reference

**What it finds:** Same topic across different PARA categories

```bash
# Search each PARA folder separately
Grep pattern: "topic" -i
path: 01-Private/01-PROJECTS

Grep pattern: "topic" -i
path: 01-Private/02-AREAS

Grep pattern: "topic" -i
path: 01-Private/03-RESOURCES

Grep pattern: "topic" -i
path: 04-ARCHIVE
```

**Why needed:** Topic spans categories (e.g., "Python" in both PROJECTS and RESOURCES)

### Strategy 6: Time-Based Discovery

**What it finds:** Recent notes on topic

```bash
# Recent modifications (last 7 days)
find "/path/to/vault" -name "*.md" -mtime -7 -type f

# Then grep results for topic
# Or read recent files directly
```

**Why needed:** Recent work context, capturing momentum

## Search Execution Pattern

### Phase 1: Quick Discovery (30 seconds)

```bash
# 1. Content search (most comprehensive)
Grep pattern: "topic-keyword" -i
output_mode: files_with_matches

# 2. Filename search (fast)
Glob pattern: **/*topic*.md
```

**Decision:** Found 5+ matches? → Read top 3-5 files
**Decision:** Found 0-2 matches? → Continue to Phase 2

### Phase 2: Deep Discovery (60 seconds)

```bash
# 3. Wikilink search
Grep pattern: \[\[.*topic.*\]\] -i
output_mode: files_with_matches

# 4. Tag search
Grep pattern: #topic -i
output_mode: files_with_matches

# 5. Variations/synonyms
Grep pattern: "variation1|variation2|synonym" -i
output_mode: files_with_matches

# 6. PARA cross-reference
# Search each PARA folder separately
```

**Decision:** Combine all results, read most relevant 3-5 files

### Phase 3: Content Analysis (2-3 minutes)

- [ ] Read identified files completely
- [ ] Note existing structure and subfolders
- [ ] Identify existing wikilinks (potential connections)
- [ ] Check YAML frontmatter for related tags/areas
- [ ] Decide: Create new vs enhance existing vs synthesize

## Quick Reference

| Goal | Primary Tool | Pattern | Secondary Tool | Pattern |
|------|-------------|---------|----------------|---------|
| Find mentions | Grep | `topic` (-i flag) | Grep | `synonym\|variation` |
| Find links | Grep | `\[\[.*topic.*\]\]` | Grep | `\[\[Exact Topic\]\]` |
| Find tags | Grep | `#topic-tag` | Grep | `#(tag1\|tag2)` |
| Find files | Glob | `**/*topic*.md` | Bash | `find -iname` |
| Cross PARA | Grep | per-folder search | Glob | per-folder pattern |
| Recent work | Bash | `find -mtime -7` | Grep | on results |

## Common Mistakes

| Mistake | What You Miss | Fix |
|---------|--------------|-----|
| **Filename search only** | 80% of content (notes mentioning topic without topic in filename) | Always do content Grep first |
| **Single keyword** | Variations, synonyms (searching "Python" misses "pandas", "py", "data analysis") | Include variations: `python\|pandas\|numpy\|py` |
| **Stopped after first search** | Wikilink-only references, tagged content | Use multi-strategy (all 6 strategies) |
| **Ignored PARA structure** | Archived notes, resources in different folders | Cross-reference all PARA folders |
| **Case-sensitive search** | "Python" vs "python" | Always use `-i` flag with Grep |
| **Didn't read results** | Context, existing structure, opportunities to enhance | Read top 3-5 matches completely |

## Red Flags - Search Deeper

If you catch yourself saying:
- "Nothing found, creating new note" → Did you try all 6 strategies?
- "Only found 1 note" → Did you search variations? Tags? Wikilinks?
- "Searched files, nothing there" → Did you search CONTENT?
- "Topic not in vault" → Did you cross-reference PARA? Check archives?
- "Quick search showed nothing" → Did you do Phase 2 Deep Discovery?

**ALL of these mean: You haven't searched thoroughly enough.**

## Search Result Thresholds

| Matches Found | Interpretation | Action |
|--------------|----------------|---------|
| **0 matches** | Truly new topic OR incomplete search | Verify: tried all 6 strategies? If yes, create new |
| **1-2 matches** | Related content exists | Read matches, decide enhance vs create |
| **3-5 matches** | Established topic | Read all matches, likely enhance existing |
| **6-10 matches** | Well-developed area | Read top 5, create MOC if doesn't exist |
| **10+ matches** | Major vault topic | Synthesize, create/update MOC, don't create scattered note |

## Integration with Other Skills

**Called by:**
- skills/obsidian/vault-creating-obsidian-notes (Phase 1 - Discovery)
- skills/obsidian/vault-obsidian-linking-strategy (Finding connection candidates)

**Calls:**
- None (foundational skill)

## Example: Full Discovery Workflow

**User:** "Show me everything about CrossFit"

```bash
# Strategy 1: Content
Grep pattern: "crossfit|cross-fit|wod|workout of the day" -i
output_mode: files_with_matches
# Result: 12 files

# Strategy 2: Wikilinks
Grep pattern: \[\[.*[Cc]rossfit.*\]\]
output_mode: files_with_matches
# Result: 5 files (3 overlap with Strategy 1, 2 new)

# Strategy 3: Tags
Grep pattern: #(crossfit|fitness|workout)
output_mode: files_with_matches
# Result: 8 files (4 new)

# Strategy 4: Filenames
Glob pattern: **/*{Crossfit,crossfit,CrossFit}*.md
# Result: 3 files (1 new)

# Strategy 5: PARA cross-ref
Grep pattern: "crossfit" -i
path: 01-Private/02-AREAS/Gezondheid
# Result: 7 files in Gezondheid area

Grep pattern: "crossfit" -i
path: 01-Private/06-JOURNAL
# Result: 15 daily notes

# Strategy 6: Recent
find -name "*.md" -mtime -7 | xargs grep -l "crossfit" -i
# Result: 2 recent mentions

# TOTAL UNIQUE: ~25 files about CrossFit across vault
```

**Report to user:**
```markdown
## CrossFit Knowledge in Vault

Found **25 notes** about CrossFit:

**Primary Hub**: [[01-Private/02-AREAS/Gezondheid/Crossfit/]]
- 7 notes in dedicated folder
- Workout logs, benchmarks, progress tracking

**Daily Journal References**: 15 entries mentioning CrossFit

**Related Links**:
- [[Whoop Data]] (recovery tracking)
- [[Fitness Goals]] (broader context)
- [[Nutrition]] (performance)

**Recent Activity**: 2 notes from last 7 days

Would you like me to:
1. Create a CrossFit MOC to consolidate these?
2. Read specific subset?
3. Synthesize into dashboard?
```

## Success Criteria

You know discovery worked when:
- Found content you didn't expect (multi-strategy worked)
- Prevented duplicate creation (search found existing)
- Surfaced cross-PARA connections (comprehensive coverage)
- Can report "X notes found across Y categories" (quantified knowledge)

## Time Investment

- Quick Discovery (Phase 1): 30 seconds
- Deep Discovery (Phase 2): 60 seconds
- Content Analysis (Phase 3): 2-3 minutes

**Total: 3-4 minutes to discover years of accumulated knowledge**

Much faster than recreating or searching manually later.

## Remember

**The vault contains more than you think. Search like you mean it.**

Multi-strategy search or don't claim ignorance.
