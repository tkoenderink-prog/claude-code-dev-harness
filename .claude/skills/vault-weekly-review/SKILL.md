---
name: Vault Weekly Review
description: Systematic maintenance prevents vault degradation through inbox processing, link health, and metadata hygiene
when_to_use: when conducting weekly review, or when vault feels disorganized, chaotic, or degraded
version: 1.0.0
languages: all
---

# Vault Weekly Review

## Overview

**Weekly maintenance prevents monthly disasters.**

Vaults degrade without maintenance:
- Inbox accumulates (50+ unprocessed items)
- Orphan notes proliferate (no links in/out)
- Projects stall (no updates for weeks)
- Broken links accumulate (notes renamed/moved)
- Metadata inconsistencies grow

**Core principle:** 30-45 minutes weekly saves 4-6 hours monthly cleanup.

## When to Use

**Use weekly** (scheduled, not when broken):
- Friday afternoon or Sunday evening
- End of work week
- During weekly planning ritual

**Use immediately when:**
- Inbox has 15+ items
- Can't find recent notes
- Projects feel stalled
- Vault seems chaotic
- Haven't reviewed in 2+ weeks

## Review Workflow

**IMPORTANT: Use TodoWrite to create todos for this checklist.**

### Phase 1: Inbox Processing (Target: 15 min)

- [ ] **Count current inbox items**
  ```bash
  ls -1 "/path/to/vault/00-INBOX" | wc -l
  ```

- [ ] **Target: INBOX zero or <5 items**
  - Process each item using skills/obsidian/vault-creating-obsidian-notes
  - Quick wins first (2-minute items)
  - Complex items: Create placeholder in correct PARA location, add to project

- [ ] **Check for aged items (>7 days in INBOX)**
  ```bash
  find "00-INBOX" -name "*.md" -mtime +7 -type f
  ```
  - Aged items = failed capture → Process immediately or archive

- [ ] **Verify processed items moved correctly**
  ```bash
  # Spot check: Read 2-3 recently processed notes
  # Verify: YAML frontmatter, 3+ links, correct PARA placement
  ```

**Success metric:** Inbox ≤5 items, no items >7 days old

### Phase 2: Project Review (Target: 10 min)

- [ ] **List all active projects**
  ```bash
  Grep pattern: "status: active"
  path: 01-Private/01-PROJECTS
  output_mode: files_with_matches

  Grep pattern: "status: active"
  path: 02-POA/01-PROJECTS
  output_mode: files_with_matches
  ```

- [ ] **For each project: Check last modified date**
  ```bash
  find "01-PROJECTS" -name "*.md" -type f -exec stat -f "%Sm %N" -t "%Y-%m-%d" {} \;
  ```

- [ ] **Identify stalled projects (>14 days no update)**
  ```bash
  find "01-PROJECTS" -name "*.md" -mtime +14 -type f
  ```

- [ ] **Decision for each stalled project:**
  - Archive? (no longer relevant) → Move to 04-ARCHIVE
  - Reactivate? (add next actions) → Update with next steps
  - Convert to Area? (ongoing, not time-bound) → Reclassify

- [ ] **Update project deadlines (in YAML frontmatter)**
  - Adjust if timeline changed
  - Add deadline if missing

- [ ] **Archive completed projects**
  - Read project, confirm Definition of Done met
  - Update status to "completed"
  - Move to 04-ARCHIVE/YYYY/MM/

**Success metric:** All active projects updated this week, completed projects archived

### Phase 3: Link Health Check (Target: 10 min)

- [ ] **Find notes created this week**
  ```bash
  find "/path/to/vault" -name "*.md" -mtime -7 -type f
  ```

- [ ] **Check each for orphan status (no links)**
  - Read note
  - Count outgoing links: \[\[...\]\]
  - If <3 → Add links using skills/obsidian/vault-obsidian-linking-strategy

- [ ] **Find potential broken links**
  ```bash
  # Extract all wikilinks
  Grep pattern: \[\[([^\]]+)\]\]
  output_mode: content
  path: /path/to/vault

  # For common targets, verify they exist
  # E.g., [[Python MOC]] → does it exist?
  Glob pattern: **/Python MOC.md
  ```

- [ ] **Quick graph view check**
  - Use Obsidian graph view or count backlinks for key notes
  - Major hub notes should have 10+ connections
  - New notes should appear connected, not floating

**Success metric:** No orphans created this week, broken links identified and logged

### Phase 4: Dashboard Updates (Target: 5 min)

- [ ] **Update main Dashboard.md with current stats**
  ```markdown
  | Metric | Value |
  |--------|-------|
  | Inbox count | [from Phase 1] |
  | Active projects (Private) | [from Phase 2] |
  | Active projects (POA) | [from Phase 2] |
  | Notes created this week | [from Phase 3] |
  | Last review date | {{today}} |
  ```

- [ ] **Update Area dashboards**
  ```markdown
  # 02-AREAS/Gezondheid/Dashboard.md

  | Area | Last Activity | Health | Focus |
  |------|--------------|---------|--------|
  | Fitness | {{date}} | 🟢/🟡/🔴 | [Current focus] |
  | Nutrition | {{date}} | 🟢/🟡/🔴 | [Current focus] |
  ```

- [ ] **Verify Dataview queries refresh**
  - Open Dashboard.md in Obsidian
  - Check Dataview sections display correctly
  - If errors → Fix query syntax

**Success metric:** Dashboards show current data, no stale information

### Phase 5: Metadata Hygiene (Target: 10 min)

- [ ] **Check recent notes for YAML frontmatter**
  ```bash
  # Find notes created this week
  find -name "*.md" -mtime -7 -type f

  # For each: Check starts with ---
  Grep pattern: ^---$
  path: [each file]
  ```

- [ ] **Verify required fields present**
  - type: project|area|resource|daily
  - status: active|planning|archived (for projects)
  - created: YYYY-MM-DD
  - tags: [at least 1 tag]

- [ ] **Standardize tags**
  - Find common misspellings: #crossfit vs #CrossFit
  - Find redundant tags: #learning + #education
  - Create tag standards if needed

- [ ] **Check PARA placement accuracy (spot check)**
  - Read 3-5 random recent notes
  - Verify classification correct per skills/obsidian/vault-para-classification-decisions
  - If misclassified → Move to correct location, update links

**Success metric:** All recent notes have proper frontmatter, tags consistent

### Phase 6: Reflection & Planning (Target: 5 min)

- [ ] **Quick wins identified:**
  - What improved this week?
  - Which projects made progress?
  - What insights emerged from vault connections?

- [ ] **Issues to address:**
  - Recurring problems (e.g., inbox always full)
  - Workflow bottlenecks
  - Missing templates or structures

- [ ] **Next week priorities:**
  - Which projects need focus?
  - Which areas need attention?
  - Any vault improvements needed?

**Success metric:** Clear sense of vault health, actionable insights

## Quick Commands Reference

| Task | Command |
|------|---------|
| Count inbox | `ls -1 "00-INBOX" \| wc -l` |
| Find aged inbox | `find "00-INBOX" -mtime +7` |
| Active projects | `Grep pattern: "status: active"` |
| Stalled projects | `find "01-PROJECTS" -mtime +14` |
| Recent notes | `find -name "*.md" -mtime -7` |
| Find orphans | Grep for notes with <3 wikilinks |
| Broken links | Extract wikilinks, verify targets exist |

## Health Metrics

| Metric | Healthy | Warning | Critical |
|--------|---------|---------|----------|
| **Inbox count** | 0-5 | 6-15 | 15+ |
| **Aged inbox items** | 0 | 1-3 | 3+ |
| **Stalled projects** | 0-1 | 2-3 | 4+ |
| **Orphan notes (weekly)** | 0 | 1-2 | 3+ |
| **Broken links** | 0 | 1-5 | 5+ |
| **Projects without update** | 0 | 1-2 | 3+ |

**Vault health:**
- All green → Excellent, maintain
- 1-2 yellow → Good, address warnings
- 1 red → Needs attention, prioritize fix
- 2+ red → Degraded, dedicate recovery time

## Common Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| **Inbox always full** | Capturing faster than processing | Daily 5-min inbox triage + better templates |
| **Projects stalling** | No weekly check-in | Add project review to daily note template |
| **Orphan notes** | Creating without linking | Use skills/obsidian/vault-creating-obsidian-notes strictly |
| **Inconsistent metadata** | Skipping templates | Never create note without template |
| **Can't find notes** | Poor linking, no MOCs | Create MOCs for topics with 7+ notes |
| **Broken links** | Renaming without updating | Use Obsidian's rename feature (auto-updates links) |

## Red Flags - Schedule Extra Review Time

If you catch yourself:
- "Inbox is fine at 20 items" → **NO. Critical at 15+**
- "I'll process inbox next week" → **NO. Process now or daily**
- "Projects are fine without updates" → **NO. >14 days = stalled**
- "Weekly review takes too long" → **NO. 30-45 min weekly saves hours monthly**
- "Skipping this week, not much happened" → **NO. Degradation happens invisibly**

**ALL mean: Review is overdue. Do abbreviated version today.**

## Time-Boxed Shortcuts

**If you only have 15 minutes:**
1. Process inbox to <5 items (10 min)
2. Check for stalled projects, archive/reactivate (5 min)

**If you only have 30 minutes:**
1. Full Phase 1: Inbox (15 min)
2. Full Phase 2: Projects (10 min)
3. Quick Phase 3: Check for orphans this week only (5 min)

**Full review (recommended): 45 minutes**
- All 6 phases
- Thorough, prevents accumulation

## Integration with Other Skills

**Uses:**
- skills/obsidian/vault-creating-obsidian-notes (Processing inbox items)
- skills/obsidian/vault-obsidian-linking-strategy (Fixing orphans)
- skills/obsidian/vault-para-classification-decisions (Verifying placement)

**Called by:**
- None (standalone maintenance ritual)

## Automation Opportunities

**Can be partially automated:**
```bash
# Weekly review preparation script
echo "=== Vault Health Report ==="
echo "Inbox count: $(ls -1 '00-INBOX' | wc -l)"
echo "Aged items: $(find '00-INBOX' -mtime +7 | wc -l)"
echo "Stalled projects: $(find '01-PROJECTS' -mtime +14 -name '*.md' | wc -l)"
echo "Recent notes: $(find . -name '*.md' -mtime -7 | wc -l)"
```

**Keep manual:**
- Inbox processing decisions (what/where)
- Project status updates (only you know progress)
- Link creation (requires understanding context)

## Success Criteria

You know weekly review worked when:
- Inbox ≤5 items (processed efficiently)
- All projects active or archived (no stale)
- No orphans created this week (linking worked)
- Dashboards current (up-to-date visibility)
- Metadata consistent (quality maintained)
- Feel clear on vault state (mental model accurate)

## Remember

**Maintenance is not overhead. It's compound interest on your knowledge system.**

30-45 minutes weekly maintains vault health that took months to build.

Skip reviews → degradation → hours of cleanup → eventual vault reset.

Do the review. Every week.
