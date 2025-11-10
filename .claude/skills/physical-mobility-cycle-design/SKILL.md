---
name: Mobility Cycle Design
description: Creates 6-week mobility program synchronized with strength cycle, addressing benchmark priorities using Kelly Starrett, Egoscue, and FMS principles
when_to_use: after benchmark complete, concurrent with strength cycle design, or when mobility limitations identified
version: 1.0.0
dependencies: Benchmark-Results file, Strength-Cycle file (for coordination), Background Research mobility files
---

# Mobility Cycle Design

## Overview

**Creates detailed 6-week mobility and flexibility program synchronized with strength training cycle, targeting benchmark-identified limitations using evidence-based protocols from Kelly Starrett, Pete Egoscue, and functional movement systems.**

Autonomously reads benchmark mobility results, coordinates with strength cycle demands, loads mobility frameworks, and generates integrated programming with transparent rationale documented in Communication folder.

## When to Use

Use this skill when:
- Benchmark week complete with mobility assessment results
- Strength cycle being designed (run concurrently)
- Current Mobility-Cycle-*.md is 6+ weeks old
- Significant mobility limitation discovered mid-cycle requiring redesign

**Run after or concurrent with** `physical-strength-cycle-design` to ensure coordination.

## Pre-Execution Autonomous Context Gathering

**MANDATORY: Read all state before asking questions**

### Step 1: Load Benchmark Mobility Results
```
Read: Physical Training/Benchmark-Results-[most recent].md

Extract mobility section:
- Overhead squat: Pass/Fail + compensations
- Toe touch: Distance achieved
- Ankle dorsiflexion: R/L measurements
- Shoulder Apley scratch: R/L status
- [Any optional mobility tests done]

Identify top 3 priority areas from benchmark
```

### Step 2: Load Strength Cycle for Coordination
```
Read: Physical Training/Strength-Cycle-[most recent].md

Extract:
- Training days and split (to coordinate mobility timing)
- Main lifts per day (to design pre-workout mobility prep)
- Schedule (X days/week, Y min/session)

Goal: Mobility work must support strength training, not interfere
```

### Step 3: Check Existing Mobility Cycle
```
Check: Physical Training/Mobility-Cycle-*.md

If found and dated <6 weeks:
  Create Communication file asking:
  "Active mobility cycle detected. Redesign or continue?"

If found and dated 6+ weeks:
  Proceed with new cycle
  Note what worked/didn't from previous cycle if user feedback exists
```

### Step 4: Load Mobility Frameworks
```
Read Background Research files:

Required:
- Comprehensive Mobility & Flexibility Assessment Framework.md
  → Interpret benchmark scores, identify interventions

- Kelly Starrett's Principles for Mobility, Flexibility and Injury Recovery.md
  → Daily mobility practice, pre/post workout protocols

- Mobility, Flexibility & Injury-Prevention Plan for a Masters CrossFit Athlete.md
  → Structured programming, progressions, frequency

- Pete Egoscue's Postural Alignment Method.md (if applicable)
  → E-cise sequences for postural issues

Document key principles loaded
```

## Quick Reference

### Mobility Cycle Structure (6 Weeks)

| Week | Phase | Focus | Volume |
|------|-------|-------|--------|
| 1-2 | Foundation | Assessment positions, basic ROM | Moderate |
| 3-4 | Development | Loaded stretching, positional strength | High |
| 5 | Integration | Full ROM under load, movement quality | Peak |
| 6 | Reassessment | Retest benchmarks, consolidate | Maintenance |

### Session Types

**Pre-Workout Prep (5-10 min)**
- Targeted to day's lifts
- Activation + mobility for patterns being loaded

**Post-Workout (10-15 min)**
- Cool-down + stretching
- Address areas stressed by workout

**Standalone Sessions (30-45 min, 2× per week)**
- Comprehensive mobility work
- Focus on priority areas from benchmark
- Progressive overload applied to mobility

## Implementation

### Phase 1: Context Analysis & Communication

**Create**: `Communication/Mobility-Cycle-Design-[Date].md`

```markdown
# Mobility Cycle Design - [Date]

## Sources Analyzed

### 1. Benchmark Mobility Results

**From Benchmark-Results-[Date].md**:

| Test | Result | Status | Priority |
|------|--------|--------|----------|
| Overhead Squat | [Pass/Fail] | [Details] | [1/2/3 or N/A] |
| Toe Touch | [Distance] | [Below/Average/Above] | [Priority rank] |
| Ankle R/L | [cm / cm] | [Pass/Fail each] | [Priority rank] |
| Shoulder Apley R/L | [Gap/Touch/Overlap] | [Asymmetry?] | [Priority rank] |
| [Additional tests] | [...] | [...] | [...] |

**Top 3 Priority Areas Identified**:
1. [Area] - Current: [score], Target: [goal], Impact: [how it limits training]
2. [Area] - Current: [score], Target: [goal], Impact: [...]
3. [Area] - Current: [score], Target: [goal], Impact: [...]

### 2. Strength Cycle Coordination

**From Strength-Cycle-[Date].md**:
- Schedule: [X days/week]
- Split: [Type]
- Main lifts per day:
  - Day 1: [Exercises] → Needs mobility prep for: [movements]
  - Day 2: [Exercises] → Needs mobility prep for: [movements]
  - [etc.]

**Coordination Strategy**:
[How mobility work will integrate with strength training]

### 3. Mobility Frameworks Applied

**From Kelly Starrett**:
- [Key principles: daily practice, 10-minute rule, pre/post protocols]

**From Mobility Plan for Masters Athletes**:
- [Frequency recommendations, volume progression, injury prevention strategies]

**From Pete Egoscue** (if postural issues identified):
- [E-cise sequences for specific conditions]

**From FMS/Assessment Framework**:
- [Corrective strategies for failed movement patterns]

## Analysis

### Mobility Limitations & Root Causes

**Priority 1: [Area, e.g., "Ankle Dorsiflexion"]**
- **Current**: [Measurement]
- **Target**: [Goal]
- **Root Cause**: [e.g., "Tight gastrocnemius/soleus, likely from years of desk work"]
- **Impact on Training**: [e.g., "Limits squat depth, causes heel lift, forward lean compensation"]
- **Intervention**: [Specific protocols from frameworks]

**Priority 2: [Area]**
[Same structure]

**Priority 3: [Area]**
[Same structure]

### Mobility-Strength Integration Plan

**Pre-Workout Prep**: [How to prime movement patterns before lifting]

**Post-Workout**: [How to address tissues stressed by training]

**Standalone Sessions**: [Dedicated work on priority areas 2× per week]

**Progression Strategy**: [How to measure improvement, when to increase difficulty]

### Weekly Structure

**Week 1-2: Foundation**
- Goal: [Establish baseline ROM, learn positions]
- Methods: [Static stretching, basic mobility drills]
- Volume: [Time per session]

**Week 3-4: Development**
- Goal: [Increase ROM, add load to end ranges]
- Methods: [Loaded stretching, PAILs/RAILs, eccentric work]
- Volume: [Increase from Week 1-2]

**Week 5: Integration**
- Goal: [Demonstrate improved ROM under load]
- Methods: [Full ROM movements with strength cycle exercises]
- Volume: [Maintained]

**Week 6: Reassessment**
- Goal: [Retest benchmarks, quantify progress]
- Methods: [Return to assessment positions, compare scores]
- Volume: [Reduced, focus on quality]

## Proposed Mobility Cycle Structure

[Detailed week-by-week breakdown below]

**Proposed course of action**: Create Mobility-Cycle-[Date].md file with this structure.

Please respond: yes/no/other
```

**Wait for user approval before creating cycle file.**

### Phase 2: Create Detailed Mobility Cycle File

**After approval, create**: `Physical Training/Mobility-Cycle-[Date].md`

```markdown
# Mobility Cycle - [Start Date] to [End Date]

**Synchronized with**: Strength Cycle [Date]
**Schedule**: Integrated (pre/post workout) + 2 standalone sessions per week
**Current Week**: 1 of 6

**Last Updated**: [Date]
**Next Assessment**: [Date + 6 weeks]

---

## Cycle Goals

### Priority Mobility Areas (from Benchmark)

1. **[Area]**
   - Current: [Score]
   - Target: [Goal]
   - Success Metric: [How to measure, e.g., "Knee-to-wall 5cm → 10cm"]

2. **[Area]**
   - Current: [Score]
   - Target: [Goal]
   - Success Metric: [...]

3. **[Area]**
   - Current: [Score]
   - Target: [Goal]
   - Success Metric: [...]

### Functional Outcomes
- [e.g., "Achieve heels-down overhead squat"]
- [e.g., "Eliminate forward lean in squat"]
- [e.g., "Symmetric shoulder mobility both sides"]

---

## Cycle Overview

### Week 1-2: Foundation
**Focus**: Learn assessment positions, establish baseline ROM
**Methods**: Static stretching, active ROM, breathing work
**Volume**: 10-15 min pre/post workout, 30 min standalone 2×/week
**Intensity**: Comfortable stretch, no forcing

### Week 3-4: Development
**Focus**: Increase ROM, add positional strength at end ranges
**Methods**: Loaded stretching, PAILs/RAILs, eccentric emphasis
**Volume**: 10-15 min pre/post workout, 40 min standalone 2×/week
**Intensity**: Working into deeper ranges, controlled discomfort

### Week 5: Integration
**Focus**: Demonstrate improved ROM under load in training
**Methods**: Full ROM lifts, mobility-focused accessory work
**Volume**: 10 min pre/post workout, 40 min standalone 2×/week
**Intensity**: Maintaining quality in fatigued state

### Week 6: Reassessment
**Focus**: Retest benchmarks, document progress
**Methods**: Return to original test positions, compare scores
**Volume**: 5-10 min pre/post workout, 30 min retest session
**Intensity**: Assessment mode, not pushing limits

---

## Daily Protocols

### Pre-Workout Mobility Prep

**Purpose**: Prime movement patterns for day's lifts, reduce injury risk

#### [Strength Day 1 - e.g., "Lower Body Day"]

**Duration**: 8-10 minutes
**Equipment**: Foam roller, band (if available)

**Protocol**:
1. **Ankle Mobilization** (Priority Area) - 2 min per side
   - Knee-to-wall stretch: 3 × 30 sec hold each ankle
   - Calf stretch against wall: 2 × 45 sec
   - **Cue**: Feel stretch in lower calf/Achilles

2. **Hip Flexor Opening** (if squatting today) - 3 min
   - Couch stretch or kneeling hip flexor: 90 sec per side
   - **Cue**: Squeeze glute to increase stretch

3. **Deep Squat Hold** (movement prep) - 2 min
   - Bodyweight squat hold: 3 × 30-40 sec
   - Rock side to side, work into hips
   - **Cue**: Heels down, chest up

4. **Activation** - 2 min
   - Glute bridges: 2 × 10
   - Band walks (if available): 2 × 10 each direction

**Transition**: Ready to start strength workout

---

#### [Strength Day 2 - e.g., "Upper Body Day"]

**Duration**: 8-10 minutes

**Protocol**:
1. **Shoulder Mobilization** (Priority Area) - 3 min
   - Wall angels: 2 × 10 reps
   - Doorway pec stretch: 90 sec per side
   - **Cue**: Keep lower back flat, focus on scapular movement

2. **Thoracic Extension** (for overhead lifts) - 3 min
   - Foam roll thoracic spine: 2 min
   - Cat-cow on hands and knees: 2 × 10 reps
   - **Cue**: Move through upper back, not lower back

3. **Wrist and Elbow Prep** - 2 min
   - Wrist circles: 10 each direction
   - Forearm stretches: 30 sec flexors, 30 sec extensors

4. **Activation** - 2 min
   - Band pull-aparts: 2 × 15
   - Scapular push-ups: 2 × 10

**Transition**: Ready for pressing/pulling work

---

[Repeat pre-workout prep for each strength training day]

---

### Post-Workout Mobility Work

**Purpose**: Cool down, address tissues stressed by training, work priority areas

#### After [Lower Body Day]

**Duration**: 12-15 minutes

**Protocol**:
1. **Cool-Down** (3 min)
   - Light walking or easy bike: 2-3 min
   - Breathing: Focus on downregulation

2. **Targeted Stretching** (8 min)
   - Hamstring stretch: 2 × 60 sec per leg
   - Quad stretch: 2 × 60 sec per leg
   - Pigeon pose (hip external rotation): 90 sec per side
   - **Cue**: Long, relaxed holds, breathe into stretch

3. **Priority Area Work - Ankles** (4 min)
   - Ankle dorsiflexion loaded stretch: 2 × 90 sec per side
     - [Specific method: e.g., "Half-kneeling with weight pushing knee forward"]
   - **Cue**: Feel stretch deep in calf, maintain heel down

**End**: Note any areas of unusual tightness or soreness

---

#### After [Upper Body Day]

**Duration**: 12-15 minutes

**Protocol**:
1. **Cool-Down** (3 min)
   - Arm circles, shoulder rolls
   - Breathing reset

2. **Targeted Stretching** (7 min)
   - Doorway pec stretch: 2 × 90 sec per side
   - Lat stretch (hang from bar or wall): 2 × 60 sec
   - Thread the needle (thoracic rotation): 60 sec per side
   - **Cue**: Relax into end ranges, no forcing

3. **Priority Area Work - Shoulders** (5 min)
   - Sleeper stretch (if internal rotation limited): 90 sec per side
   - Cross-body shoulder stretch: 90 sec per side
   - Overhead reach with band assistance: 2 × 45 sec

**End**: Note shoulder mobility feel/changes

---

[Repeat post-workout protocols for each training day]

---

### Standalone Mobility Sessions

**2× per week on non-strength days or after easy sessions**

#### Session A: Lower Body Focus

**Duration**: 35-45 minutes
**Equipment**: Foam roller, yoga mat, band (optional)

**Structure**:

1. **Warm-Up** (5 min)
   - Cat-cow: 2 × 10
   - Bird dog: 2 × 10 per side
   - Deep squat hold: 2 × 60 sec

2. **Priority Area 1 - [e.g., Ankles]** (12 min)
   - Calf smash with ball: 3 min per side
   - Banded ankle distraction: 3 min per side
   - Weighted ankle dorsiflexion: 3 × 90 sec per side
   - **Goal**: Improve knee-to-wall distance

3. **Priority Area 2 - [e.g., Hip Flexors]** (10 min)
   - Couch stretch: 3 × 90 sec per side
   - Lunge with rotation: 2 × 10 per side
   - 90/90 hip transition: 3 min practice
   - **Goal**: Pass Thomas test, improve hip internal rotation

4. **Hamstring & Posterior Chain** (8 min)
   - Active straight leg raise: 3 × 10 per leg
   - Weighted toe touch holds: 3 × 60 sec
   - Straddle stretch: 2 × 90 sec
   - **Goal**: Palms to floor in toe touch

5. **Cool-Down** (5 min)
   - Supine figure-4 stretch: 2 min per side
   - Happy baby: 2 min
   - Breathing focus

**Tracking**: Note any improvements or struggles in Cycle Progress Notes

---

#### Session B: Upper Body Focus

**Duration**: 35-45 minutes

**Structure**:

1. **Warm-Up** (5 min)
   - Arm circles: forward/back, 20 each
   - Scapular wall slides: 2 × 10
   - Thoracic rotation on floor: 2 × 10 per side

2. **Priority Area 3 - [e.g., Shoulders]** (12 min)
   - Doorway pec smash: 3 min per side
   - Banded shoulder distraction: 3 min per side
   - Overhead reach progressions: 3 × 60 sec holds
   - **Goal**: Pass Apley scratch test both sides

3. **Thoracic Spine** (10 min)
   - Foam roll t-spine: 4 min
   - Thread the needle: 2 × 90 sec per side
   - Thoracic rotation (seated with stick): 3 × 10 per side
   - **Goal**: 45+ degrees rotation each direction

4. **Neck & Upper Traps** (8 min)
   - Neck stretches (all 4 directions): 60 sec each
   - Upper trap stretch: 2 × 90 sec per side
   - Chin tucks: 3 × 10
   - **Goal**: Reduce tension, improve posture

5. **Cool-Down** (5 min)
   - Child's pose: 2 min
   - Supine twist: 90 sec per side
   - Breathing focus

**Tracking**: Note shoulder ROM changes

---

## Progression Guidelines

### Week-to-Week Progression

**Weeks 1-2 (Foundation)**:
- Focus: Learn positions, comfortable holds
- Duration: Start with 30-45 sec holds
- Intensity: "Comfortable stretch" = 4-5/10 sensation

**Weeks 3-4 (Development)**:
- Focus: Increase hold times, add load
- Duration: Progress to 60-90 sec holds
- Intensity: "Working stretch" = 6-7/10 sensation
- Add: PAILs/RAILs (push into stretch at end range)

**Week 5 (Integration)**:
- Focus: Maintain ROM under load in strength work
- Duration: Same as Week 4
- Intensity: 6-7/10, but with fatigue from strength training
- Add: Mobility-focused accessory exercises in strength sessions

**Week 6 (Reassessment)**:
- Focus: Return to test positions, measure progress
- Duration: Reduce to 30-45 sec assessment holds
- Intensity: Not pushing limits, just demonstrating ROM

### When to Progress a Drill

**Criteria**:
- Can hold position comfortably for prescribed duration
- Breathing is controlled (not holding breath)
- No sharp pain (dull stretch sensation is OK)
- Consistent performance across multiple sessions

**How to Progress**:
- Add time (30 sec → 45 sec → 60 sec)
- Add load (bodyweight → light weight → heavier)
- Add complexity (static → dynamic → loaded)
- Add range (partial → full ROM)

**Example: Ankle Mobility Progression**
- Week 1: Bodyweight knee-to-wall, 30 sec
- Week 2: Bodyweight knee-to-wall, 60 sec
- Week 3: Weighted (5kg plate on knee), 45 sec
- Week 4: Weighted (5kg plate), 90 sec
- Week 5: Weighted (10kg), 60 sec

---

## Integration with Strength Cycle

**The mobility cycle exists to support strength training, not compete with it.**

### Fatigue Management

**Pre-workout**: Brief (8-10 min), activation-focused, not fatiguing
**Post-workout**: Longer (12-15 min), relaxation-focused, aid recovery
**Standalone**: On rest days or after light activity, can go deeper

### Priorities During Strength Cycle

**If time limited**: Do pre-workout prep (non-negotiable)
**If recovered well**: Add post-workout work
**If feeling beat up**: Skip standalone session, prioritize rest

### Adjustments Based on Strength Training

**If squat day was brutal**: Post-workout lower body work shorter, gentler
**If shoulders sore**: Extra time on shoulder cool-down
**If generally fatigued**: Reduce standalone session duration or frequency

**Communication channel**: Use Cycle Progress Notes to track adjustments

---

## Progress Tracking & Reassessment

### Mid-Cycle Check (End of Week 3)

**Quick Retest**:
- [Priority Area 1]: Retest measurement
- [Priority Area 2]: Retest measurement
- [Priority Area 3]: Retest measurement

**Expected Progress**:
- Small improvements (10-20% better than baseline)
- If no progress: Increase frequency or modify methods (use Communication folder to discuss)

### End of Cycle Assessment (Week 6)

**Full Retest** (replicate benchmark tests):
- Overhead squat: Pass/Fail
- Toe touch: Distance
- Ankle R/L: Measurements
- Shoulder Apley R/L: Status
- [Any optional tests from original benchmark]

**Document in Communication folder**:

```markdown
# Mobility Cycle Results - [Date]

## Measurements: Baseline vs. Week 6

| Test | Baseline | Week 6 | Change | Status |
|------|----------|--------|--------|--------|
| [Test] | [Value] | [Value] | [+/- X] | [Improved/Maintained/Regressed] |

## Analysis

**What Worked**:
- [Effective protocols or methods]

**What Didn't**:
- [Areas that didn't improve as expected]

**Next Cycle Recommendations**:
- [Adjustments for next 6 weeks]

**Proposed course of action**: Design next mobility cycle with these findings.
```

---

## Cycle Progress Notes

[User editable section]

**Week 1**:
- Sessions completed: [X/X]
- Observations:
  -

**Week 2**:
- Sessions completed: [X/X]
- Observations:
  -

**Week 3 (Mid-Cycle Check)**:
- Sessions completed: [X/X]
- Retests: [Results]
- Observations:
  -

[Continue for Weeks 4-6]

---

## References Applied

This mobility cycle was designed using:
- Comprehensive Mobility & Flexibility Assessment Framework
- Kelly Starrett's Mobility Principles
- Mobility Plan for Masters CrossFit Athletes
- Pete Egoscue's Postural Alignment Method (if applicable)
- Benchmark-Results [Date]
- Strength-Cycle [Date] for coordination

---

## Next Steps

**During This Cycle**:
- Use `physical-mobility-session-design` skill to generate daily mobility work
- Skill will reference this cycle and adapt to context (pre/post/standalone)

**After Week 6**:
- Complete reassessment
- Document results in Communication folder
- Design next mobility cycle with updated priorities
```

## Communication Protocol Integration

**For every decision, document in Communication file:**

1. **Sources**: Benchmark results, frameworks consulted
2. **Analysis**: Why prioritize Area X over Y, why Method Z chosen
3. **Conclusion**: Proposed mobility structure
4. **Request**: "Proposed course of action is [X]. Please respond: yes/no/other"

**User control points:**
- Priority area ranking (can adjust from benchmark auto-ranking)
- Standalone session frequency (2× is recommended, can reduce to 1× or increase to 3×)
- Specific drills (can substitute preferred variations)

## Common Mistakes

### ❌ Mobility Without Strength Context
Designing mobility work without reading strength cycle. **Mobility must support and coordinate with strength training.**

### ❌ Too Much Volume
Making mobility sessions too long or frequent, interfering with recovery. **Pre-workout brief (8-10 min), standalone max 45 min, manage fatigue.**

### ❌ Ignoring Priority Areas
Doing "general mobility" without targeting benchmark failures. **Focus on top 3 limitations, make them measurably better.**

### ❌ Static Programming
Not adjusting based on how body responds. **Track progress, modify if methods not working.**

### ❌ No Progression
Doing same stretches at same intensity all 6 weeks. **Progressive overload applies to mobility - increase time, load, or complexity.**

## Online Research Protocol

**When to research:**
- Unfamiliar mobility drill mentioned in frameworks
- Need video demonstration reference for proper form
- User reports pain during specific movement (need safety check)
- Alternative methods for limited equipment

**Process:**
1. Note research need in Communication file
2. Use WebSearch for current mobility science or technique tutorials
3. Cite sources in analysis
4. Integrate findings into cycle

## Success Criteria

**Mobility cycle is complete when:**
- ✅ Benchmark mobility data analyzed
- ✅ Top 3 priority areas identified with rationale
- ✅ Strength cycle reviewed for coordination
- ✅ Mobility frameworks loaded and applied
- ✅ Analysis with transparent reasoning in Communication file
- ✅ User approved proposed structure
- ✅ Mobility-Cycle-[Date].md file created in Physical Training folder
- ✅ Pre/post workout protocols specified for each training day
- ✅ 2 standalone sessions detailed (A and B)
- ✅ Progression guidelines clear
- ✅ Mid-cycle and end-cycle reassessment plans defined

**User should feel:** Clear on mobility priorities, understands how it supports strength training, ready to improve ROM.
