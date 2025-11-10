---
name: using-skills
description: Use when starting any conversation - establishes mandatory workflows for finding and using skills, including mandatory first response protocol, using Skill tool before announcing usage, following brainstorming before coding, and creating TodoWrite todos for checklists
---

<EXTREMELY-IMPORTANT>
If you think there is even a 1% chance a skill might apply to what you are doing, you ABSOLUTELY MUST read the skill.

IF A SKILL APPLIES TO YOUR TASK, YOU DO NOT HAVE A CHOICE. YOU MUST USE IT.

This is not negotiable. This is not optional. You cannot rationalize your way out of this.
</EXTREMELY-IMPORTANT>

# Getting Started with Skills

## MANDATORY FIRST RESPONSE PROTOCOL

Before responding to ANY user message, you MUST complete this checklist:

1. ☐ List available skills in your mind
2. ☐ Ask yourself: "Does ANY skill match this request?"
3. ☐ If yes → Use the Skill tool to read and run the skill file
4. ☐ Announce which skill you're using
5. ☐ Follow the skill exactly

**Responding WITHOUT completing this checklist = automatic failure.**

## Critical Rules

1. **Use Read tool before announcing skill usage.** The session-start hook does NOT read skills for you. Announcing without calling Read = lying.

2. **Follow mandatory workflows.** Brainstorming before coding. Check for skills before ANY task.

3. **Create TodoWrite todos for checklists.** Mental tracking = steps get skipped. Every time.

4. Execute skills with the Skill tool

## Common Rationalizations That Mean You're About To Fail

If you catch yourself thinking ANY of these thoughts, STOP. You are rationalizing. Check for and use the skill.

- "This is just a simple question" → WRONG. Questions are tasks. Check for skills.
- "I can check git/files quickly" → WRONG. Files don't have conversation context. Check for skills.
- "Let me gather information first" → WRONG. Skills tell you HOW to gather information. Check for skills.
- "This doesn't need a formal skill" → WRONG. If a skill exists for it, use it.
- "I remember this skill" → WRONG. Skills evolve. Run the current version.
- "This doesn't count as a task" → WRONG. If you're taking action, it's a task. Check for skills.
- "The skill is overkill for this" → WRONG. Skills exist because simple things become complex. Use it.
- "I'll just do this one thing first" → WRONG. Check for skills BEFORE doing anything.
- "Session-start showed it to me" → WRONG. That was using-skills only. Read the actual skill.

**Why:** Skills document proven techniques that save time and prevent mistakes. Not using available skills means repeating solved problems and making known errors.

If a skill for your task exists, you must use it or you will fail at your task.

## Mandatory Workflow: Before ANY Task

**1. Check skills list** at session start, or run `find-skills [PATTERN]` to filter.

**2. If relevant skill exists, YOU MUST use it:**

- Use Read tool with full path: `.claude/skills/skill-name/SKILL.md`
- Read ENTIRE file, not just frontmatter
- Announce: "I've read [Skill Name] skill and I'm using it to [purpose]"
- Follow it exactly

## How to Read a Skill

Every skill has the same structure:

1. **Frontmatter** - `description` tells you if this skill matches your situation
2. **Overview** - Core principle in 1-2 sentences
3. **Quick Reference** - Scan for your specific pattern
4. **Implementation** - Full details and examples
5. **Supporting files** - Load only when implementing

**Skill locations:**
- Project skills: `.claude/skills/skill-name/SKILL.md`
- Personal skills: `~/.claude/skills/skill-name/SKILL.md`

## Skills with Checklists

If a skill has a checklist, YOU MUST create TodoWrite todos for EACH item.

**Don't:**
- Work through checklist mentally
- Skip creating todos "to save time"
- Batch multiple items into one todo
- Mark complete without doing them

**Why:** Checklists without TodoWrite tracking = steps get skipped. Every time. The overhead of TodoWrite is tiny compared to the cost of missing steps.

## Announcing Skill Usage

After you've read a skill with Read tool, announce you're using it.

"I've read the [Skill Name] skill and I'm using it to [what you're doing]."

**Examples:**
- "I've read the brainstorming skill and I'm using it to refine your idea into a design."
- "I've read the test-driven-development skill and I'm using it to implement this feature."
- "I've read the systematic-debugging skill and I'm using it to find the root cause."

**Why:** Transparency helps your human partner understand your process and catch errors early. It also confirms you actually read the skill.

# About these skills

**Many skills contain rigid rules (TDD, debugging, verification).** Follow them exactly. Don't adapt away the discipline.

**Some skills are flexible patterns (architecture, naming).** Adapt core principles to your context.

The skill itself tells you which type it is.

## Instructions ≠ Permission to Skip Workflows

Your human partner's specific instructions describe WHAT to do, not HOW.

"Add X", "Fix Y" = the goal, NOT permission to skip brainstorming, TDD, or RED-GREEN-REFACTOR.

**Red flags:** "Instruction was specific" • "Seems simple" • "Workflow is overkill"

**Why:** Specific instructions mean clear requirements, which is when workflows matter MOST. Skipping process on "simple" tasks is how simple tasks become complex problems.

## Summary

**Starting any task:**
1. Run find-skills to check for relevant skills (or check at session start)
2. If relevant skill exists → Use Read/Skill tool with full path
3. Announce you're using it
4. Follow what it says

**Skill has checklist?** TodoWrite for every item.

**Finding a relevant skill = mandatory to read and use it. Not optional.**
