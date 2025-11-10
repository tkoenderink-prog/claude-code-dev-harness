---
name: Strength Cycle Design
description: Creates evidence-based 6-week strength program from benchmark results and training history (CC/BLS/Hybrid)
when_to_use: after benchmark week complete, at end of 6-week cycle, or when starting new training phase with existing benchmark
version: 1.0.0
dependencies: Benchmark-Results file, Equipment.md, journal workout history, Background Research files
---

# Strength Cycle Design

## Overview

**Creates detailed 6-week strength training cycle based on benchmark results, recent training history, and evidence-based programming principles (Convict Conditioning, Bigger Leaner Stronger, or Hybrid).**

Autonomously reads benchmark data, analyzes past 5 weeks of workouts, loads appropriate training principles, and generates week-by-week programming with transparent decision-making documented in Communication folder.

## When to Use

Use this skill when:
- Benchmark week just completed (fresh Benchmark-Results-*.md file exists)
- Current Strength-Cycle-*.md is 6+ weeks old (cycle complete)
- Starting new program phase with existing valid benchmark
- Major training variable changed (equipment, schedule, goals) requiring redesign

**Do NOT use** when actively mid-cycle unless explicitly redesigning early.

## Pre-Execution Autonomous Context Gathering

**MANDATORY: Read all state before asking questions**

### Step 1: Load Benchmark Data
```
Read: Physical Training/Benchmark-Results-[most recent].md

Extract:
- Program recommendation (CC / BLS / Hybrid)
- Strength priorities (top 3 weaknesses)
- Equipment available (reference Equipment.md)
- Schedule (days/week, time/session)
- Test results (for baseline programming)
```

### Step 2: Check Existing Cycle
```
Check: Physical Training/Strength-Cycle-*.md

If found and dated <6 weeks:
  Create Communication file:
  "Active cycle detected: [Name], currently Week X.
   Redesign early or continue current cycle?"

If found and dated 6+ weeks:
  Proceed with new cycle design
  Note previous cycle for comparison
```

### Step 3: Load Training History
```
Read: Obsidian-Private/01-Private/06-JOURNAL/Workout/

Automatically find and read last 5 weeks of workout logs:
1. Search for files dated within last 35 days
2. Parse workout entries (handles Dutch format)
3. Extract:
   - Exercises performed
   - Volume patterns (sets × reps)
   - Weights used and progression
   - Training frequency (actual days/week)
   - Any reported issues (injuries, missed sessions, notes)

Document findings in Communication file
```

### Step 4: Load Training Principles
```
Based on benchmark program recommendation, read:

If CC or Hybrid:
  - Background Research/Convict Conditioning - Complete Guide.md
  - Extract: Progressions, volume guidelines, frequency, rest periods

If BLS or Hybrid:
  - Background Research/Bigger Leaner Stronger Principles for 40+.md
  - Extract: Set/rep schemes, progression methods, volume targets, deload protocol

Always:
  - Strength Training and Weightlifting Ratios.md (for balance checks)
  - CrossFit General Goals.md (if conditioning component)
```

## Quick Reference

### Cycle Structure (6 Weeks)

| Week | Phase | Focus | Volume | Intensity |
|------|-------|-------|--------|-----------|
| 1 | Foundation | Technique, baseline | Moderate | Moderate |
| 2-3 | Volume Build | Work capacity | High | Moderate-High |
| 4 | Peak Volume | Max productive stimulus | Highest | High |
| 5 | Consolidation | Maintain + refine | Moderate | High |
| 6 | Deload | Active recovery | Low | Low |

### Programming Parameters by System

**Convict Conditioning:**
- Frequency: 2-3x per week per exercise
- Sets: 1-3 working sets
- Reps: Progressive standard (varies by step)
- Progression: Master current step → advance to next step

**BLS:**
- Frequency: 2x per week per muscle group
- Sets: 9-12 hard sets per muscle per week
- Reps: 4-6 for compounds, 6-10 for accessories
- Progression: Double progression (reps then weight)

**Hybrid:**
- Bodyweight: CC progressions (upper body or full body)
- Barbell: BLS schemes (lower body or compounds)
- Frequency: Balanced based on schedule

## Implementation

### Phase 1: Context Analysis & Communication

**Create**: `Communication/Strength-Cycle-Design-[Date].md`

```markdown
# Strength Cycle Design - [Date]

## Sources Analyzed

### 1. Benchmark Results (from Benchmark-Results-[Date].md)
- Program: [CC / BLS / Hybrid]
- Strength priorities: [list top 3]
- Test results summary:
  - Push-ups: X reps
  - Pull-ups: X reps
  - Back Squat: X kg (X × BW)
  - Deadlift: X kg (X × BW)
  - [etc.]
- Equipment: [summary from Equipment.md]
- Schedule: [X days/week, Y min/session]

### 2. Training History (Last 5 Weeks)

**Analysis of recent workouts**:
- Actual frequency: [X days/week averaged]
- Exercise patterns: [What's been done regularly]
- Volume trends: [Increasing/stable/decreasing]
- Weights progressed: [Notable progressions]
- Gaps identified: [Exercises/patterns missed]
- Reported issues: [Any injury notes or problems]

**Key findings**:
[2-3 bullet points about what training history reveals]

### 3. Training Principles Loaded

**From Convict Conditioning** (if CC or Hybrid):
[List key principles: progressive overload, 10-step progressions, recovery protocols, etc.]

**From BLS** (if BLS or Hybrid):
[List key principles: 4-6 rep range, volume targets, double progression, deload protocol, etc.]

**From Strength Ratios**:
[Current ratios vs. target ratios for balance]

## Analysis

### Strength Profile & Priority Actions

**Current State**: [Interpretation of test results + recent training]

**Imbalances**: [Any strength ratio issues or asymmetries]

**Priority Actions for Next 6 Weeks**:
1. [e.g., "Build pull strength from 2 to 6-8 strict pull-ups"]
2. [e.g., "Increase squat from 1.4× to 1.6× bodyweight"]
3. [e.g., "Master CC Level 4 push-up progression"]

### Program Structure Recommendation

**Days per Week**: [3 / 4 / 5]

**Split Type**:
- [Full body / Upper-Lower / Push-Pull-Legs]
- **Rationale**: [Why this split for goals + schedule]

**Exercise Selection**:
- **Primary movements** (main strength drivers): [list]
- **Accessory movements** (support + balance): [list]
- **Equipment considerations**: [Any swaps needed based on Equipment.md]

### Progression Scheme

**If CC**: [Which progressions to work, current step → target step]

**If BLS**: [Starting weights, target progression per week]

**If Hybrid**: [Mix of both above]

### Weekly Periodization

**Week 1: Foundation**
- Goal: [Establish baseline, refine technique]
- Load: [Specific guidance]

**Week 2-3: Volume Build**
- Goal: [Accumulate work, build capacity]
- Progression: [How to increase from Week 1 to Week 3]

**Week 4: Peak**
- Goal: [Max productive volume, test strength]
- Load: [Highest of cycle]

**Week 5: Consolidation**
- Goal: [Solidify gains, refine]
- Load: [Maintain Week 4 intensity, slight volume reduction]

**Week 6: Deload**
- Goal: [Active recovery, prepare for next cycle]
- Protocol: [50% volume/intensity or specific deload method]

## Proposed Cycle Structure

[Detailed week-by-week, day-by-day breakdown below]

**Proposed course of action**: Create detailed Strength-Cycle-[Date].md file with this structure.

Please respond: yes/no/other
```

**Wait for user approval before creating cycle file.**

### Phase 2: Create Detailed Cycle File

**After approval, create**: `Physical Training/Strength-Cycle-[Date].md`

```markdown
# Strength Cycle - [Start Date] to [End Date]

**Program**: [CC / BLS / Hybrid]
**Schedule**: [X] days per week
**Split**: [Type]
**Current Week**: 1 of 6

**Last Updated**: [Date]
**Next Benchmark**: [Date + 6 weeks]

---

## Cycle Goals

### Primary Objectives
1. [Specific measurable goal from priority #1]
2. [Specific measurable goal from priority #2]
3. [Specific measurable goal from priority #3]

### Success Metrics
- [How to measure progress, e.g., "Add 10kg to squat"]
- [e.g., "Progress from CC Level 3 to Level 4 push-ups"]
- [e.g., "Achieve 6 strict pull-ups"]

---

## Cycle Overview

### Week 1: Foundation & Technique
**Focus**: Movement quality, establish working weights/progressions
**Volume**: Moderate (3 sets per exercise)
**Intensity**: 70-75% effort, RPE 6-7
**Notes**: Use Week 1 to confirm starting points, adjust as needed

### Week 2-3: Volume Build
**Focus**: Accumulate training volume, increase capacity
**Volume**: Week 2 = 3-4 sets, Week 3 = 4 sets
**Intensity**: Week 2 = 75-80%, Week 3 = 80-85%
**Progression**: Add reps or weight each session (double progression)

### Week 4: Peak Volume
**Focus**: Maximum productive stimulus
**Volume**: Highest - 4 sets, pushing close to technical failure
**Intensity**: 85-90% effort, RPE 8-9
**Notes**: This week should feel challenging but manageable

### Week 5: Consolidation
**Focus**: Maintain intensity, slight volume reduction to solidify gains
**Volume**: 3 sets, quality over quantity
**Intensity**: 85-90% maintained
**Notes**: Refine technique under load, prepare for deload

### Week 6: Deload
**Focus**: Active recovery, restore adaptation capacity
**Volume**: 50% of normal (2 sets or reduce frequency)
**Intensity**: 50-60% of max efforts
**Protocol**: [Specific deload method based on program]
**Notes**: Should feel easy, week ends with readiness for new cycle

---

## Training Days Breakdown

### [Day 1 Name - e.g., "Monday: Lower Body / Full Body / Push"]

#### Week-by-Week Prescription

**Main Lift 1: [Exercise Name]**
- **Purpose**: [Primary strength driver for X muscle/pattern]
- **Equipment**: [What's needed from Equipment.md]
- **CC Progression** (if applicable): [Current step, target step]

| Week | Sets × Reps | Load / Progression | Rest | Notes |
|------|-------------|-------------------|------|-------|
| 1 | 3 × 8-10 | [e.g., "70% of heavy single from benchmark"] | 3 min | Focus on form |
| 2 | 3 × 6-8 | [e.g., "+5kg from Week 1 or +2 reps"] | 3 min | Increase load |
| 3 | 4 × 6-8 | [e.g., "+5kg or +1 rep"] | 3-4 min | Add volume |
| 4 | 4 × 4-6 | [e.g., "+5kg, pushing limits"] | 4 min | Peak intensity |
| 5 | 3 × 4-6 | [e.g., "Maintain Week 4 weight"] | 4 min | Solidify |
| 6 | 2 × 5 | [e.g., "50% of Week 4 weight"] | 2 min | Deload |

**Form Cues**: [Key points to focus on]
**Progression Rule**: [When to add weight/advance step]

---

**Main Lift 2: [Exercise Name]**
[Same detailed structure as above]

---

**Accessory 1: [Exercise Name]** (if time permits)
- **Purpose**: [Support main lift / address imbalance]
- **All Weeks**: 3 × 8-12, RPE 7-8
- **Deload Week**: 2 × 8 @ easy weight

---

**Accessory 2: [Exercise Name]** (if time permits)
[Same structure]

---

**Mobility Integration - Pre-Workout (5-10 min)**
[Specific prep from mobility cycle for this day's lifts]

**Mobility Integration - Post-Workout (10 min)**
[Cool-down + targeted work from mobility cycle]

---

[Repeat above structure for each training day]

### [Day 2 Name]
[Full breakdown]

### [Day 3 Name]
[Full breakdown]

[etc. for all training days]

---

## Progression Protocols

### Convict Conditioning Progressions (if applicable)

**Push-Up Progression**:
- Current Step: [X]
- Target Step: [X+1 or X+2]
- Advancement Criteria: [e.g., "3 sets of 10 with perfect form"]

**Pull-Up Progression**:
- Current Step: [X]
- Target Step: [X+1]
- Advancement Criteria: [Standard from CC]

[List all CC progressions being worked]

### BLS Double Progression (if applicable)

**Method**:
1. Start with weight where you can do 4-6 reps
2. Each session, aim to add reps (4 → 5 → 6)
3. Once you hit 6 reps on all sets, add weight (usually 2.5-5kg)
4. Reset to 4-6 reps with new weight
5. Repeat cycle

**Example**:
- Week 1: 100kg × 4,4,4
- Week 2: 100kg × 5,5,4
- Week 3: 100kg × 6,6,5
- Week 4: 105kg × 4,4,4 (weight increased)

### Hybrid Approach (if applicable)

[Combine CC step progressions for bodyweight + BLS double progression for barbell]

---

## Equipment-Based Exercise Swaps

**If equipment unavailable on given day, substitute as follows**:

[Auto-generated from Equipment.md]

Example:
- Back Squat → Goblet Squat (if only dumbbells)
- Back Squat → Bulgarian Split Squat (if bodyweight only)
- Barbell Row → Dumbbell Row or Inverted Row
[etc.]

---

## Deload Week Protocol

### Option A: Reduced Volume (Recommended)
- Perform same exercises
- 2 sets instead of 3-4
- 50% of normal weight/intensity
- Maintain frequency (still train X days/week)

### Option B: Reduced Frequency
- Train 2 days only (if normally 4-5 days)
- Light full-body sessions
- Focus on mobility and movement quality

### Option C: Active Rest
- No strength training
- Mobility work only (from mobility cycle)
- Walking, swimming, or light recreation

**Chosen Method**: [Based on program and user preference]

---

## Integration with Mobility Cycle

**Mobility Cycle**: See Mobility-Cycle-[Date].md

**Integration Points**:
- **Pre-workout**: 5-10 min mobility prep from mobility cycle (specific to day's lifts)
- **Post-workout**: 10-15 min targeted mobility work
- **Rest days**: 2× per week standalone mobility sessions (30-45 min)

**Priority areas from benchmark**:
1. [Area]: [Specific work to support this cycle]
2. [Area]: [How it integrates]
3. [Area]: [Relevance to strength work]

---

## Weekly Checklist

Use this to track actual completion:

### Week 1
- [ ] Day 1 completed
- [ ] Day 2 completed
- [ ] Day 3 completed
- [ ] [Day 4 if applicable]
- [ ] [Day 5 if applicable]
- [ ] Notes: [User can add observations]

[Repeat for Weeks 2-6]

---

## Cycle Progress Notes

[User editable section to track how cycle is going]

**Week 1 Reflections**:
-

**Week 2 Reflections**:
-

[etc.]

---

## References Applied

This cycle was designed using principles from:
- [Convict Conditioning principles if CC/Hybrid]
- [BLS principles if BLS/Hybrid]
- Strength Training and Weightlifting Ratios (for balance)
- Benchmark Results [Date]
- Training History [Date range analyzed]

---

## Next Steps

**After Week 6 Deload**:
1. Run `physical-training-benchmark-week` skill to reassess
2. Compare results to current benchmark
3. Design next 6-week cycle with updated data

**During Cycle**:
- Use `physical-strength-workout-design` skill to generate daily workouts
- Skill will reference this cycle file and adapt to current week, time, equipment, recovery
```

## Communication Protocol Integration

**At every decision point, document in Communication file:**

1. **Sources**: What data informed the decision
2. **Analysis**: Reasoning about why X over Y
3. **Conclusion**: Proposed structure
4. **Request**: "Proposed course of action is [X]. Please respond: yes/no/other"

**User has final say** on:
- Exercise selection
- Split choice
- Deload protocol
- Progression speeds

## Common Mistakes

### ❌ Ignoring Training History
Designing cycle without reading recent workouts. **Always analyze last 5 weeks - it reveals actual capacity and patterns.**

### ❌ Over-Programming Deload
Making Week 6 too intense or skipping deload. **Deload is mandatory for adaptation - 50% volume/intensity.**

### ❌ Equipment Assumptions
Prescribing exercises not in Equipment.md. **Only program what user can actually do.**

### ❌ Volume Mismatch
Programming BLS volume for someone with CC recommendation or vice versa. **Follow benchmark program recommendation.**

### ❌ No Mobility Integration
Creating strength cycle without noting mobility prep. **Mobility supports strength - integrate explicitly.**

### ❌ Vague Progressions
"Add weight when it feels easy." **Define specific progression rules: reps targets, weight jumps, or step advancement criteria.**

## Online Research Protocol

**When to research:**
- Unfamiliar exercise in training history
- User mentions specific program variant not in Background Research
- Need clarification on periodization principle
- Age-specific training modifications

**Process:**
1. Note research need in Communication file
2. Use WebSearch to find evidence-based info
3. Cite sources in analysis
4. Integrate findings into cycle design

## Success Criteria

**Cycle design is complete when:**
- ✅ Benchmark data analyzed and documented
- ✅ Last 5 weeks training history reviewed
- ✅ Training principles loaded from Background Research
- ✅ Analysis with transparent reasoning in Communication file
- ✅ User approved proposed structure
- ✅ Strength-Cycle-[Date].md file created in Physical Training folder
- ✅ Week-by-week, day-by-day programming detailed
- ✅ Progression protocols clearly defined
- ✅ Mobility integration points specified
- ✅ User understands how to use cycle with daily workout skill

**User should feel:** Clear on 6-week plan, confident in progression strategy, ready to train.
