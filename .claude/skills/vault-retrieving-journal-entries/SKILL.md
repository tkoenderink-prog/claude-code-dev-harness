---
name: Retrieving Journal Entries
description: Find personal journal entries by date, topic, emotional state, metrics, or content patterns
when_to_use: when searching for journal notes by date (august 2025, week 34), content (overwhelm, procrastination), metrics (sleep, status), or emotional patterns
version: 1.0.0
languages: all
---

# Retrieving Journal Entries

## Overview

Efficiently search and retrieve personal journal entries from Obsidian-Private vault's structured journal system. Journal entries are organized in Daily and Weekly folders with specific naming conventions and rich metadata that enable precise retrieval.

## When to Use

Use this skill when you need to:
- Find journal entries from a specific date or date range ("august 2025", "week 34", "between june and july")
- Search for content patterns ("mentioning overwhelm", "about procrastination", "sleep problems")
- Retrieve entries with specific metrics ("low sleep weeks", "red status entries", "high HRV")
- Find action items, decisions, or parked items from past reflections
- Analyze emotional patterns or recurring themes across time periods

**Do NOT use when:**
- Searching across entire vault (use vault-wide search instead)
- Looking for non-journal content (use vault-discovering-vault-knowledge skill)
- Creating new journal entries (use vault-creating-obsidian-notes skill)

## Journal Structure

### Folder Locations

```bash
# Base path (absolute)
JOURNAL_BASE="/Users/tijlkoenderink/Library/Mobile Documents/iCloud~md~obsidian/Documents/Obsidian-Private/01-Private/06-JOURNAL"

# Subfolders
Daily:     $JOURNAL_BASE/Daily/
Weekly:    $JOURNAL_BASE/Weekly/
Crossfit:  $JOURNAL_BASE/Crossfit/    # Specialized
Megastacks: $JOURNAL_BASE/Megastacks/  # Specialized
```

### Naming Conventions

**Daily Entries (25+ entries):**
- Format: `YYYY-MM-DD-descriptive-kebab-case-title.md`
- Examples:
  - `2025-08-19-check-in-moving-play-work-claude-code.md`
  - `2025-02-25-crashing-hard-diet-financial-overwhelm.md`
  - `2025-07-11-overwhelming-pressure-accomplished-insane-amount-year.md`

**Weekly Entries (8+ entries):**
- Format: `YYYY-MM-DD_Week_NN_Descriptive_Title_Words.md`
- Examples:
  - `2025-08-25_Week_34_Vakantie_Crash_Overbelast.md`
  - `2025-10-12_Week_41_Stabilisering.md`
  - `2025-09-15_Week_37_Crisis_Triage_Groen_Zelfzorg.md`

### Content Structure

**Daily Entries:**
- YAML frontmatter with: `processed_date`, `type`, `tags`, `action_items`, `decisions`, `deliverables`, `deadline`
- Free-form reflection in mixed Dutch/English
- Often processed by pipeline (includes metadata)
- Sections vary by entry

**Weekly Entries:**
- Structured format with consistent sections:
  - `STATUS OVERVIEW` - Color-coded metrics (🔴 ROOD, 🟠 ORANJE, 🟢 GROEN)
  - `ZELFZORG` (Self-care) - Sleep, HRV, lean mass, sport, energy, procrastination
  - `GEZIN` (Family) - Charlotte, Kai, Sarah, Marjolijn updates
  - `FINANCIËN` (Finances) - Cashflow, actions, administration
  - `WEEKACTIES` (Weekly actions) - Numbered action list
  - `BEWUST GEPARKEERD` (Consciously parked) - Items on hold
  - `NOTITIES` (Notes) - Additional observations
- Metrics with symbols: ✓ (success), ⚠️ (warning), 🎯 (target)
- Tags: `#tag-format` in body text
- Primarily Dutch content

## Quick Reference

| Query Type | Tool | Pattern Example |
|------------|------|-----------------|
| **Specific date** | Glob | `Daily/2025-08-19-*.md` |
| **Month range** | Glob | `Daily/2025-08-*.md` |
| **Week number** | Glob | `Weekly/*_Week_34_*.md` |
| **Date range** | Bash ls + grep | `ls Daily/ \| grep -E "2025-0[6-8]"` |
| **Content search** | Grep | pattern "overwhelm" in Daily/ |
| **Tag search** | Grep | pattern "#overbelast" or "tags:" section |
| **Metric search** | Grep | pattern "🔴 ROOD" or "Slaap.*⚠️" in Weekly/ |
| **Action items** | Grep | pattern "action_items:" or "WEEKACTIES" |
| **Structured section** | Grep with context | pattern "ZELFZORG" with -A 10 |

## Implementation

### Pattern 1: Date-Based Retrieval

**Query: "journal notes from august 2025"**

```bash
# Step 1: List daily entries from august
JOURNAL_BASE="/Users/tijlkoenderink/Library/Mobile Documents/iCloud~md~obsidian/Documents/Obsidian-Private/01-Private/06-JOURNAL"

# Daily entries
Glob: "$JOURNAL_BASE/Daily/2025-08-*.md"

# Weekly entries (if needed)
Glob: "$JOURNAL_BASE/Weekly/2025-08-*.md"
```

**Query: "week 34 journal"**

```bash
# Weekly entries contain week number in filename
Glob: "$JOURNAL_BASE/Weekly/*_Week_34_*.md"
```

**Query: "entries between june and july 2025"**

```bash
# Use bash for range matching
Bash: ls "$JOURNAL_BASE/Daily/" | grep -E "2025-0[6-7]-"

# Or use multiple globs
Glob: "$JOURNAL_BASE/Daily/2025-06-*.md"
Glob: "$JOURNAL_BASE/Daily/2025-07-*.md"
```

### Pattern 2: Content-Based Retrieval

**Query: "journal notes mentioning overwhelm"**

```bash
# Search both daily and weekly
Grep:
  pattern: "overwhelm"
  path: "$JOURNAL_BASE/Daily/"
  output_mode: "files_with_matches"
  -i: true  # Case insensitive

Grep:
  pattern: "overwhelm|overbelast"  # Dutch equivalent
  path: "$JOURNAL_BASE/Weekly/"
  output_mode: "files_with_matches"
  -i: true
```

To see content with context:
```bash
Grep:
  pattern: "overwhelm|overbelast"
  path: "$JOURNAL_BASE/"
  output_mode: "content"
  -i: true
  -C: 3  # 3 lines of context
```

**Query: "procrastination patterns"**

```bash
# Weekly entries track procrastination explicitly
Grep:
  pattern: "Procrastinatie:|procrastination"
  path: "$JOURNAL_BASE/Weekly/"
  output_mode: "content"
  -i: true
  -A: 1  # Show the value after the label
```

### Pattern 3: Metric-Based Retrieval (Weekly)

**Query: "weeks with red status"**

```bash
Grep:
  pattern: "🔴 ROOD"
  path: "$JOURNAL_BASE/Weekly/"
  output_mode: "files_with_matches"
```

**Query: "low sleep weeks"**

```bash
# Sleep is tracked in ZELFZORG section with warnings
Grep:
  pattern: "Slaap.*⚠️"
  path: "$JOURNAL_BASE/Weekly/"
  output_mode: "content"
  -n: true  # Line numbers
```

**Query: "high procrastination periods"**

```bash
Grep:
  pattern: "Procrastinatie.*JA"
  path: "$JOURNAL_BASE/Weekly/"
  output_mode: "content"
  -A: 1
```

### Pattern 4: Structural Search

**Query: "action items from past weeks"**

```bash
# Daily entries: YAML frontmatter
Grep:
  pattern: "action_items:"
  path: "$JOURNAL_BASE/Daily/"
  output_mode: "content"
  -A: 10  # Show items in list

# Weekly entries: WEEKACTIES section
Grep:
  pattern: "WEEKACTIES"
  path: "$JOURNAL_BASE/Weekly/"
  output_mode: "content"
  -A: 5
```

**Query: "decisions made in march"**

```bash
# Combine date filter with content search
Glob: "$JOURNAL_BASE/Daily/2025-03-*.md"
# Then grep in results
Grep:
  pattern: "decisions:|besliss"  # English + Dutch
  path: "$JOURNAL_BASE/Daily/"
  glob: "2025-03-*.md"
  output_mode: "content"
  -i: true
  -A: 3
```

**Query: "what was consciously parked in recent weeks"**

```bash
Grep:
  pattern: "BEWUST GEPARKEERD"
  path: "$JOURNAL_BASE/Weekly/"
  output_mode: "content"
  -A: 8  # Show parked items list
  head_limit: 3  # Last 3 weeks
```

### Pattern 5: Complex Multi-Criteria Search

**Query: "find all august entries mentioning sleep or overwhelm"**

```bash
# Step 1: Get august entries
Glob: "$JOURNAL_BASE/Daily/2025-08-*.md"
Glob: "$JOURNAL_BASE/Weekly/2025-08-*.md"

# Step 2: Filter by content
Grep:
  pattern: "sleep|slaap|overwhelm|overbelast"
  path: "$JOURNAL_BASE/"
  glob: "2025-08-*.md"
  output_mode: "files_with_matches"
  -i: true
```

**Query: "entries with financial stress AND procrastination"**

```bash
# Use bash to combine criteria
Bash: |
  JOURNAL_BASE="/Users/tijlkoenderink/Library/Mobile Documents/iCloud~md~obsidian/Documents/Obsidian-Private/01-Private/06-JOURNAL"

  # Find files mentioning financial stress
  grep -ril "financ.*stress\|financiën.*⚠️" "$JOURNAL_BASE/" > /tmp/financial.txt

  # Find files mentioning procrastination
  grep -ril "procrastina" "$JOURNAL_BASE/" > /tmp/procrastination.txt

  # Find intersection
  comm -12 <(sort /tmp/financial.txt) <(sort /tmp/procrastination.txt)
```

## Language Awareness

Journal entries contain **mixed Dutch and English** content. Always search for both when relevant:

| English Term | Dutch Equivalent | Usage |
|--------------|------------------|-------|
| overwhelm | overbelast | Common in weekly status |
| procrastination | procrastinatie | Tracked metric |
| self-care | zelfzorg | Weekly section name |
| family | gezin | Weekly section name |
| finances | financiën | Weekly section name |
| sleep | slaap | Metric in weekly |
| parked | geparkeerd | Section in weekly |
| warning | waarschuwing | Less common, use ⚠️ |

**Pattern for bilingual search:**
```bash
Grep:
  pattern: "overwhelm|overbelast"
  # OR
  pattern: "sleep|slaap"
  -i: true  # Always case insensitive
```

## Common Mistakes

### ❌ Mistake 1: Using relative paths
```bash
# BAD
Glob: "06-JOURNAL/Daily/2025-08-*.md"
```

**Why:** Journal queries should use absolute paths from vault root.

```bash
# GOOD
JOURNAL_BASE="/Users/tijlkoenderink/Library/Mobile Documents/iCloud~md~obsidian/Documents/Obsidian-Private/01-Private/06-JOURNAL"
Glob: "$JOURNAL_BASE/Daily/2025-08-*.md"
```

### ❌ Mistake 2: Forgetting naming convention differences
```bash
# BAD - Daily naming pattern for weekly
Glob: "Weekly/2025-08-25-*.md"
```

**Why:** Weekly files use underscore format with Week_NN.

```bash
# GOOD
Glob: "$JOURNAL_BASE/Weekly/2025-08-*_Week_*.md"
```

### ❌ Mistake 3: Not searching bilingual content
```bash
# BAD - English only
Grep: pattern "overwhelm"
```

**Why:** Journal entries are mixed Dutch/English.

```bash
# GOOD
Grep: pattern "overwhelm|overbelast"
Grep: -i true  # Case insensitive
```

### ❌ Mistake 4: Missing emoji/symbol patterns in weekly entries
```bash
# BAD
Grep: pattern "red status"
```

**Why:** Weekly entries use emoji and Dutch text.

```bash
# GOOD
Grep: pattern "🔴 ROOD"
# OR for any red status
Grep: pattern "🔴"
```

### ❌ Mistake 5: Not using enough context for content search
```bash
# BAD
Grep:
  pattern: "action"
  output_mode: "files_with_matches"
```

**Why:** User wants to see WHAT the actions are, not just which files contain them.

```bash
# GOOD
Grep:
  pattern: "action_items:|WEEKACTIES"
  output_mode: "content"
  -A: 5  # Show the actual items
```

### ❌ Mistake 6: Searching entire vault instead of journal folders
```bash
# BAD - Too broad, wastes time
Grep:
  pattern: "procrastination"
  path: "/Users/tijlkoenderink/Library/Mobile Documents/iCloud~md~obsidian/Documents/Obsidian-Private/"
```

**Why:** Journal queries should be scoped to journal folders.

```bash
# GOOD
Grep:
  pattern: "procrastination"
  path: "$JOURNAL_BASE/"
  # Or even more specific
  path: "$JOURNAL_BASE/Weekly/"
```

## Workflow Summary

**For any journal retrieval query:**

1. **Identify query type:**
   - Date-based? → Use Glob with date patterns
   - Content-based? → Use Grep with keywords
   - Metric-based? → Use Grep with emojis/symbols
   - Structural? → Use Grep with section headers + context

2. **Choose folder scope:**
   - Daily only? → `$JOURNAL_BASE/Daily/`
   - Weekly only? → `$JOURNAL_BASE/Weekly/`
   - Both? → `$JOURNAL_BASE/`
   - Specialized? → `Crossfit/` or `Megastacks/`

3. **Add bilingual keywords:**
   - Always consider Dutch equivalents
   - Use case-insensitive search (`-i: true`)

4. **Include context when needed:**
   - Use `-A`, `-B`, or `-C` flags
   - Show structured sections fully (5-10 lines)

5. **Present results clearly:**
   - List matching files with dates visible
   - Show relevant excerpts with context
   - Summarize patterns if multiple matches

## Real-World Examples

**Query: "Show me my journal notes about sleep problems from the summer"**

```bash
# Summer = June, July, August
Grep:
  pattern: "sleep|slaap"
  path: "$JOURNAL_BASE/"
  glob: "2025-0[6-8]-*.md"
  output_mode: "content"
  -i: true
  -C: 3
```

**Query: "What were my weekly priorities in September?"**

```bash
# Get September weekly entries
Glob: "$JOURNAL_BASE/Weekly/2025-09-*.md"

# Then extract WEEKACTIES sections
Grep:
  pattern: "WEEKACTIES"
  path: "$JOURNAL_BASE/Weekly/"
  glob: "2025-09-*.md"
  output_mode: "content"
  -A: 8
```

**Query: "Find times I mentioned feeling like things were too much"**

```bash
Grep:
  pattern: "too much|te veel|overwhelm|overbelast|explode|crash"
  path: "$JOURNAL_BASE/"
  output_mode: "content"
  -i: true
  -C: 2
```

**Query: "What did I consciously decide to park or postpone?"**

```bash
# Weekly entries have BEWUST GEPARKEERD section
Grep:
  pattern: "BEWUST GEPARKEERD|geparkeerd"
  path: "$JOURNAL_BASE/Weekly/"
  output_mode: "content"
  -i: true
  -A: 8
```

## Tips for Effective Retrieval

1. **Start broad, then narrow:** Begin with date range, then filter by content
2. **Use file_with_matches first:** See what's available before requesting full content
3. **Leverage structure:** Weekly entries have predictable sections - target them directly
4. **Think bilingual:** Dutch/English mix is standard, search both
5. **Context matters:** Use `-A`, `-B`, `-C` flags generously to understand full picture
6. **Combine tools:** Glob for date selection, Grep for content filtering
7. **Check both types:** Don't forget weekly entries when searching themes - they have rich metrics
8. **Respect privacy:** Journal content is deeply personal - handle with care and discretion

## Pattern Recognition in Results

When presenting results to user, highlight:
- **Temporal patterns:** Does theme recur at specific times?
- **Metric correlations:** Does low sleep correlate with overwhelm mentions?
- **Progress indicators:** Are status colors improving over time?
- **Action follow-through:** Were parked items ever unparked?
- **Decision outcomes:** What happened after major decisions?

This helps transform raw retrieval into meaningful insights.
