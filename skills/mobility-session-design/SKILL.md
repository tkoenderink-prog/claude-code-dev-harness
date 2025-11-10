---
name: Mobility Session Design
description: Creates today's specific mobility session by reading cycle plan and adapting to context (pre-workout/post-workout/standalone) and time available
when_to_use: before mobility work, when ready for pre-workout prep, post-workout cool-down, or standalone mobility session
version: 1.0.0
dependencies: Active Mobility-Cycle file, optionally Strength-Cycle file (if pre/post workout)
---

# Mobility Session Design

## Overview

**Generates today's specific mobility session by autonomously reading the active mobility cycle plan, determining context (pre/post/standalone), and adapting to current circumstances (time, specific needs).**

Minimizes questions (asks only context and time, optionally specific focus areas), intelligently selects appropriate session from cycle, and outputs ready-to-execute mobility work.

## When to Use

Use this skill when:
- About to do mobility work (pre-workout, post-workout, or standalone)
- Need today's specific mobility session from cycle plan
- Want session adapted to current context and time

**Do NOT use** when:
- No active Mobility-Cycle file exists (run cycle design first)
- Not ready for mobility work right now

## Pre-Execution Autonomous Context Gathering

**MANDATORY: Read all state before asking questions**

### Step 1: Read State & Load Active Mobility Cycle
```
FIRST: Read Physical Training/State.md
- Get current cycle ID
- Get current week number
- Get active Mobility-Cycle filename
- Get priority mobility areas

THEN: Read Physical Training/Mobility-Cycle-[from State].md

Extract:
- Current week number (verify against State.md)
- Weekly structure (Week 1-2 foundation, 3-4 development, etc.)
- Pre-workout protocols (by training day)
- Post-workout protocols (by training day)
- Standalone sessions (A and B)
- Priority areas (top 3 from benchmark)
- Current progression guidelines
```

### Step 2: Check Strength Training Context (if relevant)
```
If user doing mobility around strength training:

Read: Physical Training/Strength-Cycle-[most recent].md

Extract:
- Today's strength training day (if pre-workout)
- Just completed strength day (if post-workout)
- Which lifts = which mobility prep needed

Example:
- Today is strength Lower Body day → Load lower body pre-workout prep
- Just finished Upper Body day → Load upper body post-workout protocol
```

### Step 3: Calculate Current Week
```
From Mobility-Cycle start date + elapsed days:
- Current week = 1, 2, 3, 4, 5, or 6
- Load appropriate progressions for that week
  - Weeks 1-2: Foundation (shorter holds, lighter intensity)
  - Weeks 3-4: Development (longer holds, added load)
  - Week 5: Integration (maintain while fatigued from strength)
  - Week 6: Reassessment (back to assessment holds)
```

### Step 4: Check Recent Mobility History (optional)
```
If user logs mobility work separately:

Read: Journal entries mentioning mobility

Extract:
- Last standalone session done (A or B?)
- Any areas mentioned as particularly tight
- When last worked priority areas
```

## Quick Reference

### Context Types

| Context | Duration | Purpose | Source in Cycle |
|---------|----------|---------|-----------------|
| **Pre-Workout** | 8-10 min | Prime patterns, activate | Pre-workout prep section |
| **Post-Workout** | 12-15 min | Cool down, stretch, address areas hit | Post-workout section |
| **Standalone** | 30-45 min | Comprehensive, priority area focus | Session A or B |

### Questions Asked (Only 2-3)

1. **Context?** → [Pre-workout / Post-workout / Standalone]
2. **Time available?** → [Specific minutes or range]
3. **Optional: Any specific areas extra tight today?** → [Free text or skip]

## Implementation

### Phase 1: Context Determination & Minimal Questions

**Create**: `Communication/Mobility-Session-[Date].md`

```markdown
# Mobility Session Design - [Date]

## Context Analyzed

### Cycle Status
- **Current Cycle**: Mobility-Cycle-[Date].md
- **Week**: [X] of 6 - [Phase, e.g., "Development"]
- **Progressions**: [Week-appropriate intensity and duration]

### Strength Training Context (if relevant)

**Recent strength session**:
- [If pre-workout]: Today's plan is [X] → Need [relevant mobility prep]
- [If post-workout]: Just completed [Y] → Need [relevant cool-down]
- [If standalone]: No strength training today → Comprehensive session

### Priority Areas (from Mobility Cycle)
1. [Area] - Target: [goal from cycle]
2. [Area] - Target: [goal]
3. [Area] - Target: [goal]

---

## Questions (minimal)

### 1. Context
What's the context for this mobility work?
- [ ] Pre-workout (before strength training)
- [ ] Post-workout (after strength training or conditioning)
- [ ] Standalone (dedicated mobility session)

### 2. Time Available
How much time do you have for the BASE session?
- [Pre-workout: 5 / 8 / 10 / 12 min]
- [Post-workout: 10 / 12 / 15 / 20 min]
- [Standalone: 20 / 30 / 40 / 45 min]

**Note**: You will ALWAYS receive TWO session options:
1. **Base Session**: Fits within your stated time limit
2. **Extended Session**: Base + up to 15-30 minutes of additional mobility work (deeper stretching, extra priority areas, tools like foam rolling/voodoo floss)

### 3. Optional: Specific Focus
Any areas feeling particularly tight or needing extra attention today?
- [Free text or "No, follow cycle plan"]

---

**Proposed course of action**: Generate mobility session based on context + responses.

Please respond: [Context] / [Time] / [Optional focus]
```

**Wait for brief user response.**

### Phase 2: Select & Adapt Session

**Based on responses, determine which session from cycle:**

```markdown
## Session Selection & Adaptation

### Context: [Pre-Workout / Post-Workout / Standalone]

**Session Type**: [Determined from context]

**From Mobility Cycle**:
[Load appropriate section]

Example logic:
- Context = Pre-Workout + Today's strength = Lower Body
  → Load "Pre-Workout Prep: Lower Body Day" from cycle

- Context = Post-Workout + Just did = Upper Body
  → Load "Post-Workout: After Upper Body Day" from cycle

- Context = Standalone + Last standalone was A
  → Load "Session B: Upper Body Focus" from cycle

### Time Adaptation

**Base Time Available**: [X minutes]
**Cycle prescription**: [Y minutes]

**ALWAYS provide TWO session versions:**

**BASE SESSION** (fits within [X] minutes):
- Priority area work (always included)
- Essential prep or cool-down drills
- Time-appropriate holds/durations
- If very limited time: Core drills only, abbreviated durations

**EXTENDED SESSION** (Base + 15-30 min additional):
- Includes all of Base Session
- PLUS: Extended work options:
  - Longer holds on priority areas (90-120 sec vs 30-60 sec)
  - Additional positions for same area
  - Secondary mobility areas from cycle
  - Tool work (foam rolling, voodoo floss, lacrosse ball)
  - Developmental drills (deeper stretches, loaded mobility)

**Specific Plan**:
[Detail the base and extended session structure for today]

### Specific Focus Adaptation

**User mentioned**: [Any specific tight areas]

**Action**:
- If area is Priority 1, 2, or 3: Add extra time (already in session)
- If area is new/different: Add specific drill at end (2-3 min)
- If "follow cycle": No additions, execute as planned

---

**Proposed course of action**: Generate final mobility session with adaptations.

Please respond: yes/no/other
```

### Phase 3: Generate Final Mobility Session

**In Communication file, create ready-to-execute session:**

```markdown
## Today's Mobility Session - [Date]

**Cycle**: Week [X], [Phase]
**Context**: [Pre/Post/Standalone]
**Base Time**: [X min] | **Extended Time**: [X+15-30 min]
**Focus**: [Priority areas or specific]
**Adaptations**: [Any changes from cycle prescription]

---

## 🧘 BASE SESSION ([X] minutes)

**Complete this if you have limited time**

### [If Pre-Workout]

**Purpose**: Prime movement patterns for today's training, reduce injury risk

#### Structure (5-10 min)

**1. [Drill 1 - e.g., "Ankle Mobilization"]** (2-3 min)
- **Exercise**: [Specific method from cycle]
- **Duration**: [e.g., "3 × 30 sec per ankle"]
- **Cue**: [What to focus on]
- **Why**: [Relevance to today's lifts]

**2. [Drill 2 - e.g., "Hip Opening"]** (2-3 min)
- **Exercise**: [...]
- **Duration**: [...]
- **Cue**: [...]

**3. [Drill 3 - e.g., "Movement Prep"]** (2 min)
- **Exercise**: [Specific prep for main lift]
- **Sets × Reps**: [e.g., "2 × 10 goblet squats, 2 × 10 glute bridges"]
- **Cue**: [...]

**4. [Drill 4 - e.g., "Activation"]** (2 min)
- **Exercise**: [...]
- **Cue**: [...]

**Transition to Workout**: Light warm-up sets of first exercise

---

### [If Post-Workout]

**Purpose**: Cool down, address tissues stressed by training, work priority areas

#### Structure (12-15 min)

**1. Cool-Down** (3 min)
- **Activity**: [e.g., "Light walking or easy movement"]
- **Purpose**: Downregulate, transition from training

**2. Targeted Stretching** (6-8 min)
- **[Stretch 1]**: [e.g., "Hamstring stretch"]
  - Duration: 2 × 60 sec per leg
  - Cue: [...]
  - Why: [Relevance to workout just done]

- **[Stretch 2]**: [e.g., "Hip flexor stretch"]
  - Duration: 2 × 60 sec per side
  - Cue: [...]

- **[Stretch 3]**: [...]
  - Duration: [...]
  - Cue: [...]

**3. Priority Area Work** (4-6 min)
- **Focus**: [Priority area from cycle, e.g., "Ankle dorsiflexion"]
- **Drill**: [Specific exercise]
- **Duration**: 2 × 90 sec per side
- **Cue**: [...]
- **Goal**: [Progress toward cycle target]

**End**: Note any unusual tightness or areas needing attention

---

### [If Standalone]

**Purpose**: Comprehensive mobility work, focus on cycle priorities, make measurable progress

#### Structure (30-45 min)

**Warm-Up** (5 min)
1. [General mobility drill 1]: 2 × 10 reps
2. [General mobility drill 2]: 2 × 10 per side
3. [General mobility drill 3]: 2 × 60 sec hold

**Priority Area 1: [Name, e.g., "Ankle Dorsiflexion"]** (10-12 min)
- **Current Status**: [From benchmark or last check]
- **Goal**: [Cycle target]

**Drill 1 - [Name]**:
- Method: [Specific technique from cycle]
- Duration: [e.g., "3 × 2 min per ankle"]
- Week [X] Progression: [Intensity level for current week]
- Cue: [...]

**Drill 2 - [Name]**:
- Method: [...]
- Duration: [...]
- Cue: [...]

**Check**: [Quick assessment - "Does knee-to-wall feel easier?"]

---

**Priority Area 2: [Name]** (10-12 min)

[Same detailed structure as Priority Area 1]

---

**Priority Area 3: [Name]** (8-10 min)

[Same structure]

---

**Cool-Down** (5 min)
1. [Restorative position 1]: 2 min hold
2. [Restorative position 2]: 2 min hold
3. Breathing focus: 1 min

**End**: Note how each priority area felt, any changes observed

---

## 🧘‍♂️ EXTENDED SESSION (+15-30 minutes)

**Do this if you have extra time and want deeper work**

**Includes**: All of BASE session above, PLUS:

### Additional Options (Choose 1-3 based on available time)

**Option 1: Longer Holds on Priority Areas** (+10-15 min)
- Repeat Priority Area 1 with longer holds (90-120 sec vs base 30-60 sec)
- Add developmental positions for same area
- Example: "For ankles - add loaded ankle dorsiflexion with KB"

**Option 2: Secondary Mobility Areas** (+10-15 min)
- Work areas beyond top 3 priorities
- Example areas:
  - Wrist mobility (for handstands, push-ups)
  - Neck/cervical spine
  - Toe/foot intrinsics
  - Hip internal rotation (if not in top 3)

**Option 3: Tool Work** (+10-15 min)
- **Foam rolling**: Full body or targeted
  - Available: Big foam roller with spikes
  - Focus on: [areas that respond well to rolling]

- **Lacrosse ball work**: Trigger point release
  - Available: Lacrosse ball, peanut ball, SuperNova ball
  - Target: [specific tight spots, e.g., "right shoulder blade area", "adductors"]

- **Voodoo floss**: Compression + movement
  - Available: Wide and narrow floss
  - Use on: [joints or muscle bellies flagged as tight]

**Option 4: Developmental Stretching** (+15-20 min)
- End-range work (careful, controlled)
- Loaded stretching with KBs
- PNF techniques (contract-relax)
- Partner stretching (if available)

**Option 5: Breathing & Parasympathetic Work** (+10-15 min)
- Extended restorative positions (5 min holds)
- Box breathing or 4-7-8 breathing
- Body scan meditation
- Purpose: Recovery, downregulation, HRV improvement

### Extended Session Examples

**Pre-Workout Extended**: Base 8 min prep + 15 min extra mobility on today's focus areas
**Post-Workout Extended**: Base 12 min cool-down + 20 min foam rolling + extra stretching
**Standalone Extended**: Base 30 min priority work + 20 min tool work + breathing

---

### BASE vs EXTENDED Decision Guide

**Do BASE only if:**
- Time is limited (must finish in stated time)
- About to start strength training (don't fatigue yourself)
- Already did CrossFit WOD today (recovery limited)
- Body feels good, no extra tightness

**Add EXTENDED if:**
- Have extra time and no rush
- Feeling particularly tight or restricted
- Standalone day with no other training
- Want to accelerate progress on priority areas
- Enjoy the mobility work and want more

---

### Session Summary

**Base Time**: ~[X minutes]
**Extended Time**: ~[X + 15-30] minutes
**Main Focus**: [Priority areas worked]
**Week [X] Progression**: [What intensity level was used]
**Next**: [What's next in cycle - opposite session if standalone, or next training day prep]

---

## Progress Notes (Optional)

**How did priority areas feel?**:
- [Area 1]: [Better/same/tighter than usual?]
- [Area 2]: [...]
- [Area 3]: [...]

**Observations**:
-

**For next cycle design**: [Any insights for future programming]

---

**Proposed course of action**: Execute above mobility session.

Please respond: yes (ready to start) / no (need changes) / other
```

## Communication Protocol Integration

**Transparent at each step:**

1. **Context Analysis**: Show what was read, which session selected
2. **Adaptation Reasoning**: Explain why drills chosen, why duration adjusted
3. **Final Session**: Clear, executable plan
4. **Confirmation**: User can proceed or request changes

## Common Mistakes

### ❌ Wrong Context Session
Doing standalone session when user wanted quick pre-workout prep. **Always ask context first - determines session type.**

### ❌ Ignoring Cycle Progression
Doing Week 1 intensity when actually in Week 4. **Calculate current week, apply appropriate progression level.**

### ❌ Too Much Volume Pre-Workout
Making pre-workout mobility 20 minutes and fatiguing. **Pre-workout brief (8-10 min max), not exhausting.**

### ❌ Not Connecting to Strength Work
Generic mobility post-workout instead of targeting areas just trained. **If pre/post workout, tailor to that day's lifts.**

### ❌ Skipping Priority Areas
Doing random stretches instead of cycle's priority focus. **Always work top 3 priority areas, especially in standalone sessions.**

### ❌ No Time Adaptation
Trying to fit 45-minute session into 20 minutes without cutting anything. **Adapt intelligently - keep priorities, reduce secondaries.**

## Adaptation Decision Framework

### Context Determines Session Type

**Pre-Workout**:
- Purpose: Prepare, not exhaust
- Duration: 8-10 min (can compress to 5 min if very limited)
- Intensity: Light to moderate, activation-focused
- Source: Cycle's pre-workout prep section (match to today's strength day)

**Post-Workout**:
- Purpose: Cool down + recovery + priority work
- Duration: 12-15 min (can extend to 20 if time available)
- Intensity: Relaxed stretching, deeper holds
- Source: Cycle's post-workout section (match to strength day just completed)

**Standalone**:
- Purpose: Comprehensive, make progress on priorities
- Duration: 30-45 min (can abbreviate to 20 if constrained)
- Intensity: Working intensity per week's progression
- Source: Cycle's Session A or B (alternate between them)

### Time Limited

**Pre-Workout (need minimum 5 min)**:
- Keep: 1-2 most relevant drills for today's lifts
- Drop: General warm-up, reduce activation

**Post-Workout (need minimum 8 min)**:
- Keep: Priority area work (most important)
- Reduce: Cool-down to 1-2 min, fewer stretches

**Standalone (need minimum 20 min)**:
- Keep: Top priority area only (full protocol)
- Reduce: Skip warm-up, abbreviated cool-down, drop lower priorities

### Week Progression

**Week 1-2 (Foundation)**:
- Holds: 30-45 sec
- Intensity: Comfortable stretch, 4-5/10 sensation
- Focus: Learning positions

**Week 3-4 (Development)**:
- Holds: 60-90 sec
- Intensity: Working stretch, 6-7/10 sensation
- Add: Load or complexity

**Week 5 (Integration)**:
- Holds: Same as Week 4
- Intensity: Maintain despite strength training fatigue
- Focus: Quality under load

**Week 6 (Reassessment)**:
- Holds: Back to assessment mode, 30-45 sec
- Intensity: Not pushing, just demonstrating ROM
- Focus: Measuring progress

## Online Research Protocol

**When to research:**
- User mentions pain during specific mobility drill (safety check needed)
- Unfamiliar mobility technique in cycle
- Need video reference for proper execution
- User requests alternative method for same goal

**Process:**
1. Note in Communication file
2. WebSearch for current mobility science or demos
3. Integrate finding or suggest alternative
4. Document source

## Success Criteria

**Mobility session is complete when:**
- ✅ Current week and progression level determined
- ✅ Context identified (pre/post/standalone)
- ✅ Appropriate session selected from cycle
- ✅ Time constraints acknowledged and session adapted
- ✅ Specific focus areas incorporated if mentioned
- ✅ Clear, executable session plan created
- ✅ Drills include cues and durations
- ✅ User confirmed ready to proceed

**User should feel:** Clear on what to do, understand why these drills today, ready to execute mobility work.
