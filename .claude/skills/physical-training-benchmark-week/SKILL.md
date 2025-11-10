---
name: Physical Training Benchmark Week
description: Comprehensive strength and mobility assessment with autonomous program selection (CC/BLS/Hybrid)
when_to_use: when starting new training cycle, reassessing after 6 weeks, injury recovery complete, or no active benchmark results in Physical Training folder
version: 1.0.0
dependencies: Obsidian vault access, Background Research files
---

# Physical Training Benchmark Week

## Overview

**Conducts integrated strength and mobility assessment over 7 days, then recommends evidence-based program (Convict Conditioning, Bigger Leaner Stronger, or Hybrid) based on results, goals, and equipment.**

This skill creates transparent documentation in Communication folder, reads existing state before asking questions, and establishes baseline for 6-week training cycles.

## When to Use

Use this skill when:
- Starting a new training program
- 6+ weeks since last benchmark
- Returning from injury
- Significant life change affecting training (equipment, schedule, goals)
- No `Benchmark-Results-*.md` file in Physical Training folder

**Do NOT use** when active benchmark exists (<6 weeks old) unless explicitly re-benchmarking.

## Pre-Execution State Check

**MANDATORY: Read before asking any questions**

```
1. Check folder: Obsidian-Private/01-Private/01-PROJECTS/Zelfzorg/Physical Training/
   - Look for Benchmark-Results-*.md (if dated <6 weeks, ask to continue or re-benchmark)
   - Look for existing Equipment.md
   - Look for active Strength-Cycle-*.md and Mobility-Cycle-*.md

2. Check workout journal: Obsidian-Private/01-Private/06-JOURNAL/Workout/
   - Read recent workout logs (last 2-4 weeks)
   - Identify: Historical lift numbers, training background, equipment used
   - Note: Training context, injury mentions, performance patterns
   - Purpose: Avoid asking questions already answered in journal

3. If active cycle found (dated within 6 weeks):
   Create Communication file asking:
   "Active cycle detected: [Cycle name, Week X].
   Re-benchmark now or continue current cycle?"
```

## Quick Reference

### Benchmark Week Structure

| Phase | Duration | Purpose |
|-------|----------|---------|
| **Setup** | 15-30 min | Goals, equipment inventory, schedule |
| **Testing** | 6-7 days | Hybrid: Core required + optional tests |
| **Analysis** | Auto | Interpret results, recommend program |
| **Output** | 1 file | Benchmark-Results-YYYY-MM-DD.md |

### Test Categories

**CORE REQUIRED (everyone):**
- Strength basics: Max push-ups, max pull-ups, bodyweight squat hold
- If barbell: Heavy singles on squat, deadlift, press
- Mobility essentials: Overhead squat assessment, toe touch, ankle wall test, Apley scratch

**OPTIONAL (choose based on goals):**
- Additional lifts: bench, front squat, cleans, Olympic lifts
- Detailed mobility: 90/90, Thomas test, thoracic rotation
- Conditioning: if CrossFit focus

## Implementation

### Phase 1: Initial Setup & Equipment Inventory

**Step 1: Create Communication File**

```markdown
# Benchmark Week Setup - [Date]

## Current State Analysis

**Existing Benchmark**: [Found: Yes/No, Date: X, Status: Current/Expired]
**Active Cycles**: [Found: Yes/No, Names/Dates]
**Equipment File**: [Found: Yes/No]

## Proceeding with: [Fresh Benchmark / Re-benchmark / Continue Cycle]

---

## Initial Questions

[Questions listed below]
```

**Step 2: Ask Goals & Context**

In Communication file, ask:

```markdown
## Setup Questions

### 1. Training Goals (select primary + secondary)
- [ ] Strength (max lifts, heavy compounds)
- [ ] Size (muscle building)
- [ ] Conditioning (CrossFit, endurance)
- [ ] Mixed (balanced athletic development)
- [ ] Injury prevention / longevity

### 2. Schedule Preference
- [ ] 3 days/week
- [ ] 4 days/week
- [ ] 5 days/week

### 3. Time Per Session
- [ ] 30 minutes
- [ ] 45 minutes
- [ ] 60 minutes
- [ ] 75+ minutes

### 4. Injury History or Current Limitations
[Free text]

### 5. Equipment Available

**Please describe what you have at each location.**
I'll create Equipment.md file for future reference.

---

**Proposed course of action**: Proceed with benchmark testing once above information provided.

Please respond: yes/no/other
```

**Step 3: Create Equipment.md**

After user provides equipment info, create:

```markdown
# Equipment Inventory

**Last Updated**: [Date]

## Home
[User's list]

## Gym - [Name if applicable]
[User's list or "Full commercial gym"]

## Travel / Portable
[Items in gym bag or hotel-friendly equipment]

---

## Equipment-Based Exercise Swaps

[Automatically generated based on inventory]

**If barbell available**: Can do back squat, deadlift, bench, press
**If dumbbells only**: Swap to goblet squat, DB deadlift, DB bench, DB press
**If bodyweight only**: Use Convict Conditioning progressions
```

Location: `Physical Training/Equipment.md`

**Step 4: Initial Program Recommendation**

Based on responses, create analysis in Communication file:

```markdown
## Initial Program Recommendation

### Sources Analyzed
- Goals: [stated goals]
- Equipment: [available equipment]
- Schedule: [days/week, time/session]
- Background Research:
  - Convict Conditioning principles
  - BLS principles for 40+
  - CrossFit standards

### Analysis

[Reasoning about program fit]

**If goals = strength + limited equipment**: Convict Conditioning focus
**If goals = size/strength + barbell**: BLS focus
**If goals = mixed + varied equipment**: Hybrid approach
**If goals = conditioning + CrossFit**: Modified BLS with conditioning

### Preliminary Recommendation: [CC / BLS / Hybrid]

**Note**: Final recommendation after benchmark testing may adjust based on:
- Actual strength levels (some lifts may favor bodyweight progressions)
- Mobility limitations (may require specific program modifications)
- Performance in specific movement patterns

---

**Proposed course of action**: Begin benchmark testing with preliminary [Program] framework.

Please respond: yes/no/other
```

### Phase 2: Benchmark Testing (6-7 Days)

**Day 1-7 Testing Protocol**

Create in Communication file:

```markdown
# Benchmark Testing Protocol

## Core Required Tests (Everyone Does)

### Strength Assessments

**Bodyweight:**
1. **Max Push-Ups** (strict form, chest to floor)
   - Record: Total reps until failure

2. **Max Pull-Ups** (strict, dead hang start)
   - Record: Total reps until failure
   - If zero, record max hang time

3. **Bodyweight Squat Hold** (bottom position, heels down)
   - Record: Max hold time

**If Barbell Available:**
4. **Back Squat** - Work up to heavy single (8-9 RPE)
   - Record: Weight achieved

5. **Deadlift** - Work up to heavy single (8-9 RPE)
   - Record: Weight achieved

6. **Strict Press** - Work up to heavy single (8-9 RPE)
   - Record: Weight achieved

### Mobility Assessments

7. **Overhead Squat Assessment** (PVC pipe or broomstick)
   - Record: Pass/Fail + observations (heels lifting, knees caving, forward lean, arms falling forward)

8. **Toe Touch Test** (standing pike, legs straight)
   - Record: Fingertips to [floor/ankles/shins/knees]

9. **Ankle Dorsiflexion** (knee-to-wall test)
   - Record: Distance in inches/cm each ankle

10. **Shoulder Apley Scratch Test**
    - Record: Fingers [overlap/touch/gap X inches] each side

## Optional Tests (Choose Based on Goals)

### Additional Strength (if barbell + goals include Olympic lifting)
- Front Squat: Heavy single
- Power Clean: Heavy single
- Bench Press: Heavy single

### Detailed Mobility (if mobility is priority or limitations found)
- 90/90 Hip Rotation: Pass/Fail each side
- Thomas Test (hip flexor length): Pass/Fail each leg
- Thoracic Rotation (seated): Degrees estimated each side
- Active Straight Leg Raise: Height achieved each leg

### Conditioning (if CrossFit goals)
- 500m Row for time
- Max unbroken double-unders
- Fran time (if experienced)

---

## Testing Schedule Suggestion

**Day 1**: Strength - Bodyweight tests (push-ups, pull-ups, squat hold)
**Day 2**: Rest or light mobility
**Day 3**: Strength - Barbell (work up to heavies on squat, deadlift, press)
**Day 4**: Mobility testing (all required mobility tests)
**Day 5**: Optional strength tests (if doing additional lifts)
**Day 6**: Optional mobility tests (if doing detailed assessment)
**Day 7**: Rest / Optional conditioning tests

**Flexible**: Can compress or spread based on your schedule. Key is adequate rest between max effort strength days.

---

**Proposed course of action**: Execute testing protocol over next 6-7 days. Report results when complete.

Please respond: yes/no/other (or suggest modified schedule)
```

### Phase 3: Results Analysis & Program Recommendation

**After user reports results, create analysis:**

Location: `Communication/Benchmark-Analysis-[Date].md`

```markdown
# Benchmark Analysis - [Date]

## Sources

### Test Results (Raw Data)
[Copy all reported test results]

### Reference Standards
- **Convict Conditioning**: [Read relevant progressions]
- **BLS Strength Ratios**: [Read ratios from Background Research]
- **CrossFit Standards**: [Read recreational athlete goals]
- **Mobility Framework**: [Read assessment benchmarks]

### Historical Context
[If previous benchmark exists, note changes]

## Analysis

### Strength Profile

**Absolute Strength**: [Assessment based on bodyweight tests and barbell lifts if done]

**Relative Strength**: [Compare to bodyweight ratios from Background Research]

**Strength Ratios**: [If barbell lifts done, compare squat:deadlift:press ratios]

**Pattern**: [Push-dominant / Pull-dominant / Balanced / Leg-weak, etc.]

### Mobility Profile

**Critical Limitations**: [Any failed core mobility tests]

**Secondary Concerns**: [Marginal passes or asymmetries]

**Strengths**: [Areas of good mobility]

**Priority Areas**: [Rank top 3 mobility focuses]

### Program Suitability Analysis

**Convict Conditioning Fit**:
- Pros: [e.g., limited equipment, bodyweight mastery needed, progressive overload clear path]
- Cons: [e.g., if strong lifter, may not be challenged by early progressions]

**BLS Fit**:
- Pros: [e.g., barbell available, size/strength goals, proven periodization]
- Cons: [e.g., if mobility limited, heavy compounds may be contraindicated]

**Hybrid Fit**:
- Pros: [e.g., can address both barbell and bodyweight gaps, flexible]
- Cons: [e.g., requires more exercise swaps, complexity]

## Conclusion

### Final Program Recommendation: [CC / BLS / Hybrid]

**Rationale**: [Clear reasoning based on above analysis]

### Specific Modifications Needed:
[e.g., "BLS with additional mobility work pre-workout due to ankle limitations"]
[e.g., "CC for upper body, barbell squats/deadlifts for lower body (Hybrid)"]

### Priority Focus Areas:
1. [e.g., "Build pull strength - currently 2 pull-ups, target 10"]
2. [e.g., "Improve ankle dorsiflexion for squat depth"]
3. [e.g., "Develop overhead position - failed overhead squat test"]

---

**Proposed course of action**:
1. Create final Benchmark-Results-[Date].md file
2. Ready to proceed to Cycle Design with [Program] framework

Please respond: yes/no/other
```

### Phase 4: Create Official Benchmark Results File

Location: `Physical Training/Benchmark-Results-[Date].md`

```markdown
# Benchmark Results - [Date]

**Program Recommendation**: [CC / BLS / Hybrid]

---

## Test Results Summary

### Strength

| Test | Result | Rating |
|------|--------|--------|
| Max Push-Ups | X reps | [Beginner/Intermediate/Advanced] |
| Max Pull-Ups | X reps | [Rating] |
| Bodyweight Squat Hold | X sec | [Rating] |
| Back Squat | X kg (X × BW) | [Rating per BLS ratios] |
| Deadlift | X kg (X × BW) | [Rating] |
| Strict Press | X kg (X × BW) | [Rating] |

**Strength Pattern**: [Push-dominant / Pull-weak / Balanced, etc.]

### Mobility

| Test | Result | Status |
|------|--------|--------|
| Overhead Squat | Pass/Fail | [Notes] |
| Toe Touch | [Distance] | [Above/Average/Below average] |
| Ankle R/L | X cm / X cm | [Pass/Fail per knee-to-wall] |
| Shoulder Apley R/L | [Gap/Touch/Overlap] | [Status] |

**Mobility Pattern**: [Critical limitations, asymmetries]

---

## Priority Focus Areas

### Strength Priorities
1. [Specific weakness identified]
2. [Second priority]
3. [Third priority]

### Mobility Priorities
1. [Most limited area]
2. [Second concern]
3. [Third area]

---

## Program Framework: [CC / BLS / Hybrid]

### Rationale
[1-2 paragraphs explaining why this program fits goals, equipment, results]

### Key Principles to Apply
[Core principles from Background Research for chosen program]

**From Convict Conditioning** (if CC or Hybrid):
- Progressive overload through 10-step progressions
- Master form before progressing
- Low volume, high quality
- Unilateral strength development

**From BLS** (if BLS or Hybrid):
- Heavy compounds 4-6 rep range
- 9-12 sets per muscle per week
- Double progression method
- Deload every 6-8 weeks

**Mobility Integration**:
- Daily practice of priority areas (10-15 min)
- Pre-workout prep for specific lifts
- 2 standalone mobility sessions per week

---

## Ready for Cycle Design

**Equipment**: See Equipment.md
**Schedule**: [X days/week, Y min/session]
**Timeline**: 6-week cycles with reassessment

**Next Steps**:
1. Run `strength-cycle-design` skill
2. Run `mobility-cycle-design` skill
3. Begin training with `strength-workout-design` and `mobility-session-design` skills

---

**Benchmark Valid Until**: [Date + 6 weeks]
```

## Communication Protocol Integration

**Every decision point creates a Communication file with:**

1. **Sources**: What data was analyzed
2. **Analysis**: Reasoning process
3. **Conclusion**: Proposed recommendation
4. **Request**: "Proposed course of action is [X]. Please respond: yes/no/other"

**User maintains control** - skill only proceeds after explicit approval.

## Common Mistakes

### ❌ Skipping State Check
Testing without checking for existing benchmark/cycles. **Always read Physical Training folder first.**

### ❌ Over-Testing
Doing every optional test when not relevant to goals. **Core tests are sufficient for most; optionals only if specific focus.**

### ❌ Ignoring Mobility-Strength Connection
Recommending heavy barbell program when mobility tests show critical limitations. **Mobility must support strength program.**

### ❌ Equipment Mismatch
Recommending BLS without barbell, or CC when user has full gym and size goals. **Equipment dictates program feasibility.**

### ❌ Not Documenting Rationale
Giving recommendation without showing analysis. **Transparency builds trust and allows user to course-correct.**

## References to Background Research

**This skill actively reads and applies:**

- `Physical Training/Background Research/Convict Conditioning - A Complete Bodyweight Strength Training Guide.md`
- `Physical Training/Background Research/Bigger Leaner Stronger (BLS) Principles for Building Strength (and Size) After 40.md`
- `Physical Training/Crossfit General Goals Recreational Athlete.md`
- `Physical Training/Strength Training and Weightlifting Ratios.md`
- `Physical Training/Background Research/Comprehensive Mobility & Flexibility Assessment Framework.md`

**Use these to**:
- Interpret test results against standards
- Explain program principles in recommendations
- Set realistic targets for next cycle
- Guide exercise selection decisions

## Online Research Protocol

**When to research online:**
- Unfamiliar exercise mentioned by user
- Doubt about mobility test interpretation
- Need for age-specific strength standards
- Clarification of training principle

**Process:**
1. Note what needs research in Communication file
2. Use WebSearch to gather info
3. Document sources in analysis
4. Proceed only after synthesis

## Success Criteria

**Benchmark week is complete when:**
- ✅ Equipment.md file exists
- ✅ All core tests completed and recorded
- ✅ Program recommendation made with clear rationale documented in Communication
- ✅ User approved final recommendation
- ✅ Benchmark-Results-[Date].md file created in Physical Training folder
- ✅ System ready for cycle design skills

**User should feel:** Clear about program direction, confident in rationale, ready to start training.
