---
name: Strength Workout Design
description: Creates today's specific strength workout by reading cycle plan, recent training, and adapting to current circumstances (location/time/recovery)
when_to_use: before each strength training session, when ready to work out and need today's specific plan
version: 1.0.0
dependencies: Active Strength-Cycle file, Equipment.md, recent journal entries
---

# Strength Workout Design

## Overview

**Generates today's specific strength training workout by autonomously reading the active cycle plan, analyzing recent training history, checking equipment availability, and adapting to current recovery state and time constraints.**

Minimizes questions (asks only location, time, recovery), makes intelligent adaptations, and outputs a ready-to-execute workout with logging template for journal.

## When to Use

Use this skill when:
- About to do strength training session
- Need today's specific workout from cycle plan
- Want workout adapted to current circumstances
- Ready to train NOW (not planning ahead multiple days)

**Do NOT use** when:
- No active Strength-Cycle file exists (run cycle design first)
- Not ready to train today (this generates immediate workout)

## Pre-Execution Autonomous Context Gathering

**MANDATORY: Read all state before asking questions**

### Step 1: Read State & Load Active Strength Cycle
```
FIRST: Read Physical Training/State.md
- Get current cycle ID
- Get current week number
- Get active Strength-Cycle filename
- Get recent scores for context

THEN: Read Physical Training/Strength-Cycle-[from State].md

Extract:
- Current week number (verify against State.md)
- Training days breakdown (Day 1, Day 2, etc. with exercises)
- Today's prescribed workout:
  - Exercises
  - Sets × Reps
  - Load guidance
  - Rest periods
  - Mobility integration
- Progression rules
- Equipment assumptions
```

### Step 2: Determine Which Cycle Day is Next
```
Read: 06-JOURNAL/Workout/ (most recent entries)

Parse last 7 days:
1. Find most recent workout file (handles Dutch dates: "2025-10-15 Workout.md")
2. Extract:
   - Date of last session
   - Which cycle day was completed (match exercises to cycle plan)
   - Days since last workout
   - Any notes about performance or issues
3. Calculate: Next cycle day = Last day + 1 (or Day 1 if new week)

Example:
- Last workout: "2025-10-15 Cleans Workout" = Cycle Day 2, Week 3
- Days since: 2 days ago
- Today should be: Cycle Day 3, Week 3
```

### Step 3: Calculate Current Week
```
From Strength-Cycle file start date + days elapsed:
- If file says "Current Week: 1 of 6" but dated 10 days ago → Actually Week 2
- Update week number based on actual time passed

OR rely on journal entry tracking if user has been logging week numbers
```

### Step 4: Load Equipment Availability
```
Read: Physical Training/Equipment.md

Prepare to ask: "Where are you?"
Then load appropriate equipment section:
- "Home" → load home equipment list
- "Gym - [Name]" → load gym equipment
- "Travel" → load portable equipment

Have equipment swap rules ready if prescribed exercise unavailable
```

## Quick Reference

### Context Gathered Automatically

| Data Point | Source | Purpose |
|------------|--------|---------|
| Current Week | Cycle file + date math | Know which week's prescription |
| Current Day | Last journal entry + cycle | Know which day of split |
| Days Since Last | Journal dates | Assess recovery time |
| Last Session Performance | Journal notes | Context for today's approach |
| Prescribed Workout | Cycle file | Base template |
| Equipment Available | Equipment.md + user location | Adapt exercises |

### Questions Asked (Only 3)

1. **Location?** → [Home / Gym / Travel] (determines equipment)
2. **Time available?** → [30 / 45 / 60 / 75+ min] (determines completeness)
3. **Recovery state (1-10)?** → (determines intensity adjustment)

## Implementation

### Phase 1: Context Summary & Minimal Questions

**Create**: `Communication/Workout-[Date].md`

```markdown
# Workout Design - [Date]

## Context Analyzed

### Cycle Status
- **Current Cycle**: Strength-Cycle-[Date].md
- **Week**: X of 6 - [Phase name, e.g., "Volume Build"]
- **Last Workout**: [Date] - [Cycle Day Y] - [X days ago]
- **Today Should Be**: Cycle Day [Z], Week [X]

### Last Session Summary (from journal)
**Date**: [Last workout date]
**Exercises**: [What was done]
**Performance**: [Any notes from reflection section]
**Issues**: [If any reported]

**Days Since**: [X days] → [Recovery assessment: Fresh / Adequate / Possibly fatigued]

### Today's Prescribed Plan (from Cycle)

**From Week [X], Day [Z] of Strength-Cycle**:

**Main Lifts**:
1. [Exercise]: [Sets × Reps] @ [Load guidance]
2. [Exercise]: [Sets × Reps] @ [Load guidance]

**Accessories** (if applicable):
1. [Exercise]: [Sets × Reps]
2. [Exercise]: [Sets × Reps]

**Mobility**:
- Pre: [Prescribed prep]
- Post: [Prescribed cool-down]

**Estimated Time**: [Calculate: ~X minutes based on exercises, sets, rest]

---

## Questions (minimal - only what cannot be inferred)

### 1. Location
Where are you training today?
- [ ] Home
- [ ] Gym - [Name]
- [ ] Travel / Other location

### 2. Time Available
How much time do you have for the BASE workout?
- [ ] 20 minutes (main lifts only, minimal volume)
- [ ] 30 minutes (main lifts only, reduced volume)
- [ ] 45 minutes (main lifts full, some accessories)
- [ ] 60 minutes (full session as prescribed)
- [ ] 75+ minutes (full session + extras)

**Note**: You will ALWAYS receive TWO workout options:
1. **Base Workout**: Fits within your stated time limit
2. **Extended Workout**: Base + up to 30 minutes of additional work (optional accessories, extra sets, conditioning)

### 3. Recovery State
How recovered do you feel? (1-10 scale)
- 1-3: Very fatigued, sore, poor sleep
- 4-6: Moderately recovered, some lingering fatigue
- 7-9: Well recovered, ready to push
- 10: Fully fresh, explosive

---

**Proposed course of action**: Generate adapted workout based on above context + your responses.

Please respond: [Location] / [Time] / [Recovery #]
```

**Wait for user's brief response.**

### Phase 2: Adapt Workout to Circumstances

**Based on responses, create adaptation logic:**

```markdown
## Workout Adaptation Analysis

### Equipment Check

**Location**: [Home / Gym / Travel]
**Available Equipment** (from Equipment.md - [Location] section):
[List equipment]

**Exercise Swaps Needed**:
[Check prescribed exercises against available equipment]

Example:
- Cycle prescribes: Back Squat
- Equipment available: Dumbbells only
- **Swap**: Back Squat → Goblet Squat (from Equipment.md swap rules)

OR:
- Cycle prescribes: Back Squat
- Equipment available: Barbell
- **No swap needed**: Proceed as prescribed

### Time Adaptation

**Base Time Available**: [X minutes]
**Cycle prescription**: ~[Y minutes]

**ALWAYS provide TWO workout versions:**

**BASE WORKOUT** (fits within [X] minutes):
- Priority 1: Main lifts (always keep, may reduce sets if very limited)
- Priority 2: Key accessories (keep if time allows)
- Priority 3: Extra accessories (drop if needed)
- Mobility: Abbreviate pre-workout to essentials (5 min minimum)
- Post-workout: Brief (3-5 min) if time limited

**EXTENDED WORKOUT** (Base + up to 30 min additional):
- Includes all of Base Workout
- PLUS: Additional volume options:
  - Extra accessory exercises
  - Additional sets on main lifts (backoff sets, volume work)
  - Conditioning work (Assault bike intervals, kettlebell complexes)
  - Extended mobility work
  - Skill practice (handstands, muscle-ups, etc.)
- Total time: Base + [10-30 min]

**Time Adaptation Examples**:
- If base = 20 min: Main lift only (3 sets), 5 min mobility → Extended adds accessories + conditioning (total 45-50 min)
- If base = 45 min: Full main lifts + key accessories → Extended adds extra volume + skill work (total 75 min)

**Specific Plan**:
[Detail the base and extended workout structure for today]

### Recovery Adaptation

**Recovery State**: [1-10 number]

**Adaptation Rules**:

**If 8-10 (Well Recovered)**:
- Execute as prescribed
- Can push for PR attempts if in progression range
- Full intensity and volume

**If 5-7 (Moderately Recovered)**:
- Execute as prescribed
- Cap top end (don't push for new PRs today)
- If sets feel unusually hard, drop final set
- Stay in prescribed ranges, don't exceed

**If 1-4 (Fatigued)**:
- **Option A**: Technique day (reduce load to 70%, focus on form, 2 sets only)
- **Option B**: Skip strength, do mobility session instead
- **Do NOT push through** - fatigue masks poor form and increases injury risk

**Today's Plan**:
[Specific adjustment based on recovery number]

---

**Proposed course of action**: Generate final workout with above adaptations.

Please respond: yes/no/other
```

**Brief user confirmation, then generate workout.**

### Phase 3: Generate Final Workout

**In Communication file, create ready-to-execute workout:**

```markdown
## Today's Workout - [Date]

**Cycle**: Week [X], Day [Y] - [Phase]
**Location**: [Where]
**Base Time**: [X min] | **Extended Time**: [X+10-30 min]
**Equipment**: [What's available]
**Recovery**: [State]
**Adaptations**: [Summary of any changes from cycle prescription]

---

## 🏋️ BASE WORKOUT ([X] minutes)

**Complete this if you have limited time**

### Warm-Up (5-10 min)

**From Mobility Cycle** (pre-workout prep for today's lifts):

1. [Mobility drill 1]: [Duration / reps]
   - **Cue**: [What to focus on]

2. [Mobility drill 2]: [Duration / reps]
   - **Cue**: [...]

3. [Movement prep / activation]: [Sets × reps]

**Transition**: Light sets of first main lift (empty bar or light weight)
- [Exercise]: 1 × 10 @ empty, 1 × 5 @ warmup weight

---

### Main Work

#### Exercise 1: [Name]

**Today's Target** (Week [X] prescription):
- **Sets × Reps**: [Specific, e.g., "4 × 6-8"]
- **Load**: [Specific guidance from cycle]
  - Starting suggestion: [Calculate from last session if logged, or from cycle guidance]
  - Example: "Week 3 calls for +5kg from Week 2. Last session you did 100kg × 6,6,5. Try 105kg today."

**Rest**: [Period, e.g., "3-4 minutes between sets"]

**Execution**:
- Set 1: [Target reps] @ [weight]
- Set 2: [Target reps] @ [weight]
- Set 3: [Target reps] @ [weight]
- Set 4: [Target reps] @ [weight] (if prescribed)

**Form Cues**:
- [Key point 1 from cycle or general best practice]
- [Key point 2]

**Progression Rule** (from cycle):
[When to add weight or progress, e.g., "If you hit 6+ reps on all sets, add 2.5-5kg next session"]

**Adaptation Notes** (if any):
[e.g., "Swapped to goblet squat due to equipment" OR "Reduced to 3 sets due to recovery state"]

---

#### Exercise 2: [Name]

[Same detailed structure as Exercise 1]

---

#### Exercise 3: [Name] (Accessory)

**Today's Target**:
- **Sets × Reps**: [e.g., "3 × 8-12"]
- **Load**: [Guidance, e.g., "Choose weight where last 2 reps are challenging"]

**Rest**: [Period, e.g., "2 minutes"]

**Form Cues**:
- [Key points]

**Notes**:
[e.g., "Addressing pull strength imbalance from benchmark"]

---

[Repeat for all prescribed exercises]

---

### Cool-Down (5-15 min, time permitting)

**From Mobility Cycle** (post-workout protocol for today):

1. [Cool-down activity]: [Duration, e.g., "2-3 min light walk"]

2. [Targeted stretch 1]: [Duration / reps]
   - **Cue**: [...]

3. [Targeted stretch 2]: [Duration / reps]

4. [Priority area work from mobility cycle]: [Duration]
   - [Specific drill]: [How long]

**If time limited**: At minimum do [Priority stretch], skip optional extras

---

## 💪 EXTENDED WORKOUT (+10-30 minutes)

**Do this if you have extra time and energy**

**Includes**: All of BASE workout above, PLUS:

### Additional Volume / Accessories

**Option 1: Extra Sets on Main Lifts**
- [Main Exercise 1]: 2-3 backoff sets @ 80-85% of working weight
  - Purpose: [e.g., "Build volume for strength endurance"]

**Option 2: Additional Accessory Work**
- [Accessory Exercise 4]: 3 × 10-12
  - Purpose: [e.g., "Extra pulling volume for upper back"]

- [Accessory Exercise 5]: 3 × 8-10
  - Purpose: [e.g., "Unilateral leg work for balance"]

### Conditioning Block (10-15 min)

**Choose one:**

**A. Assault Bike Intervals** (if at home)
- 8 rounds: 20 sec hard / 40 sec easy
- Purpose: Conditioning without interfering with strength recovery

**B. Kettlebell Complex** (if at home)
- 5 rounds: KB Swing × 10, Goblet Squat × 5, KB Press × 5 each
- Rest 90 sec between rounds
- Weight: [Moderate KB, e.g., 20kg or 24kg]

**C. CrossFit-style Chipper** (if at gym)
- [Prescribed based on equipment and energy]

### Extended Mobility Work (5-10 min)

**Priority Areas** (from mobility cycle):
- [Extended work on flagged limitation, e.g., "Adductor stretching - 3 positions × 90 sec"]
- [Thoracic mobility - specific drills]
- [Foam rolling / voodoo floss on tight areas]

### Skill Practice (5-10 min)

**If at park or gym:**
- Pull-up volume work: [e.g., "5 sets of max reps, rest 2 min"]
- Handstand practice: [e.g., "Wall holds or freestanding attempts"]
- Muscle-up transitions: [Specific skill work]

---

### Extended Workout Summary

**Total Extended Time**: ~[X + 20-30] minutes
**Additional Work**: [Summary of what extended adds]
**Do this if**: You feel good, have time, want extra volume

**Skip this if**: Base workout felt hard, recovery was low, limited time

---

### BASE vs EXTENDED Decision Guide

**Do BASE only if:**
- Time is truly limited (must finish in [X] min)
- Recovery state was 1-6 (low to moderate)
- CrossFit WOD earlier today (already got volume)
- Feeling fatigued or sore

**Add EXTENDED if:**
- Have extra 20-30 min available
- Recovery state was 7-10 (feeling good)
- Want extra volume for weak areas
- No CrossFit WOD today
- Enjoying the session and want to do more

---

## Logging Template

**Copy to Journal**: 06-JOURNAL/Workout/[Date] Workout.md

```markdown
# Workout Log - [Date in Dutch format]

**Datum**: [Date]
**Workout**: [Name, e.g., "Lower Body - Squat Focus"]
**Cycle**: Week [X], Day [Y]

---

## Uitgevoerde Gewichten

### [Exercise 1]

|Set|Gewicht|Reps|Resultaat|
|---|---|---|---|
|1|___ kg|___|✓ / No Rep|
|2|___ kg|___|✓ / No Rep|
|3|___ kg|___|✓ / No Rep|
|4|___ kg|___|✓ / No Rep|

**Hoogste succesvolle**: ___ kg × ___ reps

---

### [Exercise 2]

[Same table structure]

---

[Repeat for all exercises]

---

## Reflectie

**Technische uitvoering**:
-

**Fysieke staat**:
-

**Algemene observatie**:
-

---

## Workout Context

- **Cycle**: Week [X] of 6, Day [Y]
- **Equipment**: [Location]
- **Time**: [Duration]
- **Recovery going in**: [#]/10
- **Adaptations made**: [Any changes from prescribed]

---

**Next Session**: [Preview - "Day [Z], focus on [...]"]
```

**End of logging template.**

---

### Next Session Preview

**When you're ready for your next workout**, run this skill again.

Based on cycle progression:
- **Next will be**: Day [Z+1], Week [X or X+1]
- **Focus**: [Brief preview of what's coming]
- **Estimated**: [Days from now based on typical schedule]

---

**Proposed course of action**: Execute above workout, log results in journal using template.

Please respond: yes (ready to train) / no (need changes) / other
```

## Communication Protocol Integration

**Transparent decision-making at every step:**

1. **Context Summary**: Show what was read from cycle, journal, equipment
2. **Adaptation Analysis**: Explain why Exercise X swapped, why volume reduced, etc.
3. **Final Workout**: Clear, executable plan
4. **Request Confirmation**: User can approve or request changes

**If user says "other"**: Ask what needs adjustment, modify workout, re-confirm.

## Common Mistakes

### ❌ Not Reading Recent Journal
Generating workout without checking last session. **Always read most recent journal entries to understand context.**

### ❌ Ignoring Recovery State
Prescribing full intensity when user reports 3/10 recovery. **Adapt intelligently - technique day or skip if severely fatigued.**

### ❌ Equipment Assumptions
Prescribing barbell work when user is traveling. **Always check Equipment.md for location and swap exercises accordingly.**

### ❌ Time Optimism
Fitting 90 minutes of work into 45-minute window. **Prioritize main lifts, cut accessories if time constrained.**

### ❌ Losing the Plot
Making too many adaptations, workout no longer resembles cycle intent. **Adaptations should be minimal - only for true constraints.**

### ❌ No Logging Template
User has to figure out how to log workout. **Always provide copy-paste ready template in their journal format (Dutch).**

## Adaptation Decision Framework

### Equipment Unavailable

**Process**:
1. Check Equipment.md for exercise swap rules
2. If no rule exists, apply principle-based swap:
   - Same movement pattern (squat → squat variant)
   - Similar load potential (barbell → dumbbell if available)
   - Maintain intent (strength → strength, not endurance)

**Common Swaps**:
- Back Squat → Goblet Squat / Bulgarian Split Squat
- Barbell Bench → Dumbbell Bench / Push-ups (weighted if possible)
- Barbell Row → Dumbbell Row / Inverted Row
- Deadlift → Single-leg Deadlift / Romanian DL with DBs

### Time Limited

**Priority Hierarchy**:
1. **Keep**: Warm-up (abbreviated to 5 min if needed)
2. **Keep**: Main lifts (all sets, but can reduce rest slightly)
3. **Reduce**: Accessories (drop 1-2 sets or entire accessory)
4. **Abbreviate**: Cool-down (5 min minimum vs. 15 min full)

**Example**:
- Prescribed: 60 min total
- Available: 45 min
- **Cut**: Drop 2nd accessory, reduce cool-down to 5 min
- **Keep**: Both main lifts at full volume

### Recovery Compromised

**1-4/10 (Severely Fatigued)**:
- **Recommend**: Skip or technique-only day
- **If technique day**: 2 sets @ 60-70% prescribed load, focus on perfect form
- **Better choice**: Do mobility session instead

**5-7/10 (Moderately Recovered)**:
- **Execute**: As prescribed
- **Cap**: Don't push for PRs today, stay in prescribed ranges
- **Monitor**: If struggling early, consider dropping final set

**8-10/10 (Well Recovered)**:
- **Execute**: Full prescription
- **Allow**: PR attempts if progression rules allow
- **Encourage**: Push the working sets

## Online Research Protocol

**When to research:**
- User mentions unfamiliar exercise not in cycle or Equipment.md
- Question about form cue for specific lift
- Need alternative exercise due to pain/injury concern
- Doubt about progression rule interpretation

**Process:**
1. Note need in Communication file
2. WebSearch for current best practices or video demos
3. Integrate finding into workout
4. Document source

## Success Criteria

**Workout design is complete when:**
- ✅ Current cycle day and week determined from journal
- ✅ Equipment availability checked and swaps made if needed
- ✅ Time constraints acknowledged and volume adapted
- ✅ Recovery state assessed and intensity adjusted
- ✅ Clear, executable workout plan created
- ✅ Form cues and progression rules included
- ✅ Dutch-format logging template provided
- ✅ User confirmed ready to train

**User should feel:** Clear on exactly what to do, confident in the plan, ready to execute immediately.
