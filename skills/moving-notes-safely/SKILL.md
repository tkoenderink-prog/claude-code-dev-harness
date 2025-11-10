---
name: Moving Notes Safely in Obsidian
description: Systematic workflow for moving Obsidian notes via CLI without breaking wikilinks and embeds
when_to_use: when moving or reorganizing markdown files in Obsidian vault, renaming notes, or restructuring folder hierarchies
version: 1.0.0
languages: all
---

# Moving Notes Safely in Obsidian

## Overview

**Moving files via command line breaks Obsidian links.** Wikilinks (`[[Note]]`) and embeds (`![[Note]]`) reference files by name/path. When you use `mv` or file operations outside Obsidian, all references to that file become broken links.

**Core principle:** Pre-analyze → Git commit → Move file → Update all references → Verify integrity.

## Why This Matters

**Reality:** A single `mv` command breaks dozens of links across your vault.

**From baseline testing:**
- Simple `mv Meeting\ Notes.md Areas/` broke 4 references in 2 files
- Agent rationalized "links will still work" - they didn't
- Time pressure caused skipping verification
- No reference analysis before move = blind operation

## Link Types That Break

| Link Type | Example | What Breaks |
|-----------|---------|-------------|
| Simple wikilink | `[[Meeting Notes]]` | File moved, reference unchanged |
| Wikilink with alias | `[[Meeting Notes\|Important]]` | Same issue |
| Path-based wikilink | `[[Areas/Meeting Notes]]` | Path changed, reference stale |
| Embed | `![[Meeting Notes]]` | File moved, embed broken |
| Markdown link | `[text](Meeting Notes.md)` | Relative path invalid |

**All of these need updating when files move.**

## When NOT to Use This Skill

**Skip this workflow for:**
- Moving files within Obsidian app (it handles links automatically - ALWAYS prefer this if available)
- Files with zero references (but you must verify this first)
- Non-markdown files that aren't referenced in notes

**Note:** Moving files within the Obsidian app is ALWAYS safer because Obsidian updates links automatically. This skill exists for situations where:
- You're working in a terminal/SSH session without Obsidian GUI access
- You're automating workflows via CI/CD or scripts
- You prefer CLI workflows for your development process

**If Obsidian app is available, use it. If not, use this workflow. Don't skip the workflow thinking "my case is different."**

## The Workflow

### Phase 1: Pre-Move Analysis

**Find all references to the file you're moving:**

```bash
# Get filename without extension and path
FILE_NAME="Meeting Notes"

# Find all wikilinks (including aliases and embeds)
grep -r "\[\[.*${FILE_NAME}" /path/to/vault/

# Find markdown links
grep -r "\](.*${FILE_NAME}.md)" /path/to/vault/

# Find with path variations
grep -r "\[\[.*/${FILE_NAME}" /path/to/vault/
```

**Document what you find:**
- How many files reference this note?
- What link formats are used?
- Are there embeds (`![[]]`)?

**If you find 0 references, verify with multiple patterns before proceeding.**

### Phase 2: Safety Net

**Commit current state to git:**

```bash
cd /path/to/vault
git add .
git commit -m "Before moving: ${FILE_NAME}"
git push origin main
```

**Why:** If links break catastrophically, you can revert. No git? STOP. Set up git first.

### Phase 3: Move the File

**Now and only now, move the file:**

```bash
# Verify source exists
ls -la "Meeting Notes.md"

# Verify destination folder exists
ls -ld "Areas/"

# Move with verbose output
mv -v "Meeting Notes.md" "Areas/Meeting Notes.md"

# Verify move succeeded
ls -la "Areas/Meeting Notes.md"
```

**Do NOT use wildcards. Do NOT batch move multiple files. One file at a time.**

### Phase 4: Update References

**You must update EVERY reference you found in Phase 1.**

**For simple wikilinks without paths:**

If the file moved from root to `Areas/`, update references:

```bash
# From: [[Meeting Notes]]
# To: [[Areas/Meeting Notes]]
```

**Use Edit tool for each file:**
- old_string: `[[Meeting Notes]]`
- new_string: `[[Areas/Meeting Notes]]`
- For files with multiple types, do separate Edit calls

**For embeds:**

```bash
# From: ![[Meeting Notes]]
# To: ![[Areas/Meeting Notes]]
```

**For wikilinks with aliases:**

```bash
# From: [[Meeting Notes|Important Meeting]]
# To: [[Areas/Meeting Notes|Important Meeting]]
```

**For path-based links that are now wrong:**

```bash
# If something was [[Projects/Meeting Notes]] and you moved to Areas:
# From: [[Projects/Meeting Notes]]
# To: [[Areas/Meeting Notes]]
```

**Critical:** Update the file's own outgoing links if they used relative paths.

### Phase 5: Verification

**Verify all references are updated:**

```bash
# OLD references should return 0 results
grep -r "\[\[Meeting Notes\]\]" /path/to/vault/
# (Should be empty - if not, you missed some)

# NEW references should match your Phase 1 count
grep -r "\[\[Areas/Meeting Notes" /path/to/vault/
# (Count should equal original reference count)
```

**If counts don't match, you broke something. Find and fix before proceeding.**

**Check the moved file itself:**

```bash
cat "Areas/Meeting Notes.md"
# Verify its internal links still make sense
```

### Phase 6: Commit the Change

**Commit with descriptive message:**

```bash
git add .
git commit -m "Move: Meeting Notes → Areas/Meeting Notes (updated 4 references in 2 files)"
git push origin main
```

**The commit message documents what you did for future reference.**

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|-------------|-----|
| "Just move it, Obsidian will figure it out" | CLI moves are invisible to Obsidian | Follow the workflow |
| Moving without git commit | Can't recover from errors | Always commit first |
| Skipping reference analysis | You don't know what to update | Phase 1 is mandatory |
| Using `mv *.md` for batch moves | Mass breakage, impossible to track | One file at a time |
| "I'll update links later" | You forget, links stay broken | Update immediately after move |
| Trusting grep results without verification | Regex misses edge cases | Always verify final counts |
| "Only 2 references, I'll do it manually" | Manual = mistakes | Use Edit tool even for 1 reference |

## Handling Renames (Same Folder)

**Renaming is moving with extra complexity:**

```bash
# If renaming "Meeting Notes.md" → "Team Sync Notes.md" in same folder:

# 1. Find references (same as Phase 1)
grep -r "\[\[Meeting Notes" /path/to/vault/

# 2. Git commit
git add . && git commit -m "Before rename: Meeting Notes → Team Sync Notes"

# 3. Rename file
mv "Meeting Notes.md" "Team Sync Notes.md"

# 4. Update ALL references to new name
# [[Meeting Notes]] → [[Team Sync Notes]]
# [[Meeting Notes|alias]] → [[Team Sync Notes|alias]]

# 5. Verify and commit
```

**Renaming is MORE dangerous than moving because more patterns can match.**

## Red Flags - STOP and Reconsider

If you find yourself thinking:

- "Quick move, I'll check links later" → NO. Check now.
- "Obsidian uses filename resolution, links will work" → FALSE for CLI moves.
- "Only moving one file, low risk" → One file can have 50+ references.
- "Time pressure, need to move now" → 5 minutes now saves 2 hours fixing later.
- "I'll do Phase 1 after the move" → Reversed order = broken vault.
- "These references look optional" → ALL references matter.
- "I'll write a script to move them all safely" → Scripts have bugs. One file at a time.
- "Doing them one-by-one is inefficient" → Efficiency is not the goal. Safety is.
- "I can make batch processing work" → You can't. The rule exists for good reason.

**All of these mean: Slow down. Follow the workflow.**

## Batch Operations

**Need to move 10 files?**

1. DO NOT write a loop script
2. DO NOT write a Python/shell script to "safely" batch process
3. DO NOT use wildcards
4. DO move files one at a time
5. DO commit after each successful move
6. DO verify after each move before starting next

**Why one mistake doesn't cascade to 10 files:**
- Script bugs affect all files at once
- One regex error breaks every link update
- Can't tell which file caused the problem
- Git history is clean: each move is separate commit
- Can stop if you spot a problem

**"But I'll write a careful script" is NOT an exception:**
- Your script will have bugs (they all do)
- Testing takes longer than doing files manually
- One bug = 10 broken files = hours of recovery
- The discipline of one-at-a-time prevents compound errors

**From testing:**
- Agent created "safe batch script" despite explicit prohibition
- Rationalized as "more efficient"
- Violated rule under efficiency pressure
- Even good scripts violate the safety principle

**No exceptions. No scripts. One file at a time.**

## Recovery from Broken Links

**If you already broke links:**

```bash
# 1. Check git status
git status

# 2. If uncommitted, revert
git restore .

# 3. If committed, revert the commit
git log  # Find commit hash
git revert <hash>

# 4. Start over with this workflow
```

## Real-World Impact

**From production usage:**
- "Meeting Notes" move: Would have broken 4 references without workflow
- Time cost: 5 minutes with workflow vs 2+ hours finding/fixing broken links
- Git safety net: Enabled instant revert when testing edge cases

**The workflow takes longer. The broken vault takes longer to fix.**

## Common Rationalizations for Skipping Steps

| Excuse | Reality |
|--------|---------|
| "I'll write a safe batch script" | Scripts have bugs. One bug = all files broken. |
| "One-by-one is too slow" | Slow and safe beats fast and broken. |
| "I'll test the script first" | Testing takes longer than manual. Just do it right. |
| "Links will auto-resolve" | Not for CLI moves. They break. Period. |
| "I'll fix links later" | Later = never. Broken vault stays broken. |
| "Already moved, too late" | Never too late. Fix the links now. |
| "Only a few references" | Even 1 broken link matters. Update all. |
| "Time pressure" | 5 min now vs 2 hours fixing later. Choose. |

**All of these mean: Follow the workflow. No shortcuts.**

## Violations Are NOT Differences in Style

"I prefer to move first then check links" = Breaking the workflow = Broken links.

**Violating the letter of this workflow is violating the spirit of this workflow.**

The order matters. The verification matters. The git commits matter. Skip steps = break links.

## Checklist

**Use TodoWrite to create todos for EACH item:**

- [ ] Phase 1: Run grep to find all references, document count
- [ ] Phase 2: Git add/commit/push current state
- [ ] Phase 3: Move file with mv, verify destination exists
- [ ] Phase 4: Update every reference found in Phase 1 using Edit tool
- [ ] Phase 5: Verify old references = 0, new references = original count
- [ ] Phase 5: Check moved file's internal links
- [ ] Phase 6: Git add/commit/push with descriptive message

**Create these todos BEFORE starting any move operation.**
