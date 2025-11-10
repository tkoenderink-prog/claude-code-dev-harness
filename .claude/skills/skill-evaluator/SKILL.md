# Skill Evaluator

## Metadata
- **Category:** Meta / Quality Assurance
- **Complexity:** Expert
- **Time Estimate:** 10-15 minutes per skill
- **Version:** 1.0.0
- **Created:** 2025-11-10

## Purpose
Systematically evaluate AI agent skills using research-backed criteria. Produces objective 0-100 scores across five dimensions to identify high-quality skills, detect low-quality implementations, and guide improvement efforts.

## When to Use
- Evaluating newly created skills before adding to library
- Auditing existing skill library for quality issues
- Comparing multiple skills that serve similar purposes
- Deciding whether to keep, improve, or remove a skill
- Prioritizing skill improvement efforts
- Conducting regular skill library health checks

## Evaluation Framework

### Five Dimensions (20 points each, 100 total)

#### Dimension A: Functional Correctness (0-20)
Does the skill accomplish its stated purpose reliably?

**Scoring Criteria:**
- **18-20 (Exemplary)**: Clear purpose, comprehensive coverage, handles edge cases, robust error guidance
- **14-17 (Strong)**: Clear purpose, good coverage, most edge cases handled
- **10-13 (Good)**: Purpose clear, basic coverage, some edge cases missing
- **6-9 (Adequate)**: Purpose somewhat clear, basic coverage only, many gaps
- **3-5 (Weak)**: Purpose unclear, minimal coverage, significant gaps
- **0-2 (Poor)**: Purpose absent/confused, doesn't deliver value

**Assessment Questions:**
- Does it clearly state what problem it solves?
- Does the content deliver on that promise?
- Are edge cases and limitations addressed?
- Would following this skill produce the intended outcome?

---

#### Dimension B: Clarity & Usability (0-20)
How easy is it for agents and users to understand and apply?

**Scoring Criteria:**
- **18-20 (Exemplary)**: Crystal clear, excellent examples, logical structure, perfect documentation
- **14-17 (Strong)**: Very clear, good examples, well-structured, complete docs
- **10-13 (Good)**: Clear enough, some examples, decent structure
- **6-9 (Adequate)**: Somewhat clear, few examples, structure could improve
- **3-5 (Weak)**: Confusing, no examples, poor structure
- **0-2 (Poor)**: Incomprehensible, no structure, unusable

**Assessment Questions:**
- Is the skill name semantically clear and descriptive?
- Are usage instructions comprehensive and unambiguous?
- Are there concrete examples showing application?
- Is the structure logical and easy to navigate?
- Are all parameters/inputs clearly documented?

---

#### Dimension C: Modularity & Composability (0-20)
How well does the skill integrate with other skills and follow single-responsibility principle?

**Scoring Criteria:**
- **18-20 (Exemplary)**: Single clear purpose, zero overlap, highly reusable, clear dependencies
- **14-17 (Strong)**: Focused purpose, minimal overlap, reusable, dependencies documented
- **10-13 (Good)**: Mostly focused, some overlap, somewhat reusable
- **6-9 (Adequate)**: Multiple purposes, noticeable overlap, limited reuse
- **3-5 (Weak)**: Unfocused, significant overlap, hard to reuse
- **0-2 (Poor)**: Completely unfocused, massive overlap, not reusable

**Assessment Questions:**
- Does it do one thing well, or multiple things poorly?
- Does it overlap with other skills? How much?
- Can it be easily composed with other skills?
- Are dependencies clearly stated?
- Could this be broken into smaller, more focused skills?

---

#### Dimension D: Performance & Efficiency (0-20)
How efficiently does the skill operate in terms of cognitive load, execution time, and resource usage?

**Scoring Criteria:**
- **18-20 (Exemplary)**: Minimal cognitive load, efficient approach, optimal length, actionable
- **14-17 (Strong)**: Low cognitive load, good efficiency, appropriate length
- **10-13 (Good)**: Moderate load, acceptable efficiency, reasonable length
- **6-9 (Adequate)**: High load, some inefficiency, could be more concise
- **3-5 (Weak)**: Very high load, inefficient, too long or too short
- **0-2 (Poor)**: Overwhelming, extremely inefficient, wrong length

**Assessment Questions:**
- Is the skill an appropriate length? (Not too verbose, not too brief)
- Does it minimize cognitive load on the agent?
- Are instructions actionable and direct?
- Does it avoid unnecessary complexity?
- Is the approach efficient for the problem?

---

#### Dimension E: Domain Coverage & Specialization (0-20)
How well does the skill cover its domain with appropriate specialization level?

**Scoring Criteria:**
- **18-20 (Exemplary)**: Perfect depth/breadth balance, clear boundaries, ideal specialization
- **14-17 (Strong)**: Good coverage, clear boundaries, appropriate specialization
- **10-13 (Good)**: Adequate coverage, mostly clear boundaries, decent specialization
- **6-9 (Adequate)**: Incomplete coverage, fuzzy boundaries, wrong specialization level
- **3-5 (Weak)**: Poor coverage, no boundaries, too broad or too narrow
- **0-2 (Poor)**: No coverage, undefined boundaries, completely wrong level

**Assessment Questions:**
- Does it cover its domain with appropriate depth?
- Is it too general (lacks depth) or too specific (limited applicability)?
- Are the boundaries of its domain clear?
- Is the specialization level right for the problem?
- Are there obvious gaps in domain coverage?

---

## Evaluation Process

### Step 1: Read the Skill
- Load the skill file completely
- Understand its stated purpose and scope
- Note first impressions of quality

### Step 2: Evaluate Each Dimension
For each dimension (A-E):
1. Review the scoring criteria above
2. Answer the assessment questions
3. Assign a score from 0-20
4. Write 2-3 sentence justification

### Step 3: Calculate Total Score
- Sum all five dimension scores (max 100)
- Apply overall rating:
  - 90-100: Exemplary (gold standard)
  - 80-89: Strong (minor improvements only)
  - 70-79: Good (some improvements needed)
  - 60-69: Adequate (needs significant improvement)
  - 50-59: Weak (consider redesign)
  - 0-49: Poor (remove or completely rewrite)

### Step 4: Identify Issues
List specific problems found:
- Critical issues (blockers)
- Major issues (significantly impact quality)
- Minor issues (polish needed)

### Step 5: Provide Recommendations
Suggest concrete improvements:
- Quick wins (easy, high impact)
- Medium-term improvements
- Long-term strategic changes

---

## Output Format

```markdown
# Skill Evaluation: [Skill Name]

**Evaluated:** [Date]
**Evaluator:** [Agent/Human Name]
**Skill Path:** [Path to skill file]

## Overall Score: [X]/100 - [Rating]

### Dimension Scores

**A. Functional Correctness: [X]/20**
[2-3 sentence justification]

**B. Clarity & Usability: [X]/20**
[2-3 sentence justification]

**C. Modularity & Composability: [X]/20**
[2-3 sentence justification]

**D. Performance & Efficiency: [X]/20**
[2-3 sentence justification]

**E. Domain Coverage & Specialization: [X]/20**
[2-3 sentence justification]

---

## Issues Identified

### Critical Issues
- [Issue 1]
- [Issue 2]

### Major Issues
- [Issue 3]
- [Issue 4]

### Minor Issues
- [Issue 5]
- [Issue 6]

---

## Recommendations

### Quick Wins (1-2 hours)
1. [Recommendation]
2. [Recommendation]

### Medium-Term (4-8 hours)
1. [Recommendation]
2. [Recommendation]

### Long-Term (Strategic)
1. [Recommendation]
2. [Recommendation]

---

## Summary

[2-3 paragraph summary of the evaluation, highlighting key strengths and most important improvements needed]

## Decision

- [ ] **Keep as-is** (score ≥80)
- [ ] **Improve** (score 60-79)
- [ ] **Major redesign** (score 50-59)
- [ ] **Remove/replace** (score <50)
```

---

## Research Foundation

This evaluation framework is based on research from 40+ sources including:

### Key Research Findings

1. **The 10-20-4 Rule** (LangChain, Google Cloud, 2024)
   - Max 10-20 tools per agent for reliable performance
   - Max 3-4 tools per task to avoid cognitive overload
   - Systems with 50+ tools: 10-20% success rate
   - Systems with focused sets: 50%+ success rate

2. **Modularity Over Monolithism** (Agent S2, arXiv 2024)
   - Modular frameworks with suboptimal models outperform best standalone models
   - Specialized skills > generalist capabilities
   - Single-purpose tools reduce confusion and misuse

3. **Documentation is Critical** (AutoGen, Microsoft Research)
   - Agents select tools primarily based on names and descriptions
   - Poor documentation = tool misuse or non-use
   - 100% documentation completeness is non-negotiable

4. **Overlap Destroys Performance** (Berkeley AI Research)
   - When multiple skills solve the same problem, agents get confused
   - Target: <5% overlap across skill library
   - Clear boundaries and unique purposes essential

5. **Cognitive Load Matters** (UC Berkeley, 2024)
   - Each additional tool adds cognitive complexity
   - Verbose descriptions slow processing, brief descriptions cause misuse
   - Optimal length varies by complexity: 50-300 lines for most skills

### Sources
- LangChain Documentation & Case Studies (2024)
- AutoGen Multi-Agent Framework (Microsoft Research)
- Agent S2: Modular Multi-Agent Systems (arXiv 2024)
- Google Cloud Agent Builder Best Practices
- Berkeley AI Research: Tool Selection in LLMs
- 35+ additional academic and industry sources

---

## Examples

### Example 1: High-Quality Skill (Score: 92/100)

**Skill:** `dev-test-driven-development`
**Scores:** A:19, B:18, C:19, D:18, E:18

**Why High Quality:**
- Crystal clear RED-GREEN-REFACTOR methodology
- Comprehensive examples for each phase
- Perfect single-purpose focus (TDD only)
- Efficient 365 lines with no fluff
- Complete coverage of TDD domain

**Minor Improvements:**
- Add section on TDD in legacy codebases
- Include common pitfalls and how to avoid them

---

### Example 2: Template Skill (Score: 34/100)

**Skill:** `caching-strategies`
**Scores:** A:6, B:8, C:7, D:7, E:6

**Why Low Quality:**
- 77-line generic template with no real content
- No specific caching examples or patterns
- Overlaps with performance-optimization and database-design
- Too generic to be actionable
- Missing critical implementation details

**Recommendations:**
- Option 1: Expand with real Redis/Memcached examples (8 hours)
- Option 2: Merge into performance-optimization skill
- Option 3: Remove entirely (replace with link to external resource)

---

### Example 3: Medium-Quality Skill (Score: 68/100)

**Skill:** `api-design`
**Scores:** A:14, B:13, C:14, D:13, E:14

**Why Medium Quality:**
- Clear purpose and good REST/GraphQL coverage
- Could use more concrete examples
- Some overlap with api-documentation skill
- Slightly verbose in places
- Good but not great domain coverage

**Quick Wins:**
- Add 2-3 complete API examples (REST + GraphQL)
- Clarify boundary with api-documentation skill
- Trim verbose sections by 20%
- Add security considerations section

---

## Common Patterns

### Signs of High-Quality Skills
✅ Clear, focused purpose statement
✅ Comprehensive examples and use cases
✅ Logical structure with clear sections
✅ Appropriate length for complexity
✅ Unique value (no overlap with other skills)
✅ Complete documentation (when, why, how)
✅ Realistic and actionable guidance

### Red Flags for Low-Quality Skills
🚩 Generic template language ("strategies", "patterns" without specifics)
🚩 77-line length (indicates unconverted template)
🚩 No concrete examples or code snippets
🚩 Overlaps significantly with other skills
🚩 Unclear when to use vs. other similar skills
🚩 Too broad (tries to cover too much)
🚩 Too narrow (limited applicability)
🚩 Missing trigger conditions (when to use)

---

## Calibration Guide

To ensure consistent scoring across evaluations:

### Functional Correctness (Dimension A)
- **20 points:** Comprehensive framework like `dev-test-driven-development` (365 lines)
- **15 points:** Solid guidance like `code-organization` (100-200 lines)
- **10 points:** Basic coverage like medium-quality skill templates
- **5 points:** Minimal guidance, major gaps
- **0 points:** No useful content

### Clarity & Usability (Dimension B)
- **20 points:** `dev-systematic-debugging` - crystal clear structure, perfect examples
- **15 points:** Clear instructions, good examples, well-structured
- **10 points:** Understandable but could be clearer
- **5 points:** Confusing, hard to follow
- **0 points:** Incomprehensible

### Modularity & Composability (Dimension C)
- **20 points:** Single focused purpose, zero overlap, clear dependencies
- **15 points:** Mostly focused, minimal overlap
- **10 points:** Some overlap or scope creep
- **5 points:** Significant overlap, unclear boundaries
- **0 points:** Massive overlap, unfocused

### Performance & Efficiency (Dimension D)
- **20 points:** Optimal length, minimal cognitive load, highly actionable
- **15 points:** Good efficiency, appropriate length
- **10 points:** Acceptable but could be more efficient
- **5 points:** Too verbose or too brief, high cognitive load
- **0 points:** Extremely inefficient

### Domain Coverage & Specialization (Dimension E)
- **20 points:** Perfect depth/breadth for domain, clear boundaries
- **15 points:** Good coverage, appropriate specialization
- **10 points:** Adequate coverage, some gaps
- **5 points:** Poor coverage, wrong specialization level
- **0 points:** No useful domain coverage

---

## Best Practices for Evaluation

### 1. Be Objective
- Base scores on criteria, not personal preference
- Use examples to calibrate scoring
- Compare to other skills for consistency

### 2. Be Thorough
- Read the entire skill before scoring
- Answer all assessment questions
- Justify every score with evidence

### 3. Be Constructive
- Focus on actionable improvements
- Prioritize by impact (quick wins first)
- Suggest specific changes, not just "improve X"

### 4. Be Consistent
- Use the same rubric for all skills
- Calibrate regularly against examples
- Document reasoning for borderline scores

### 5. Consider Context
- Evaluate relative to stated purpose
- Consider target audience (beginner vs expert)
- Account for domain complexity

---

## Quality Thresholds

### For Skill Library Inclusion
- **Minimum Score:** 60/100 (Adequate)
- **Target Score:** 70/100 (Good)
- **Excellence:** 80/100+ (Strong/Exemplary)

### For Different Skill Types
- **Meta Skills:** Target 75+ (need higher quality)
- **Core Development:** Target 70+ (frequently used)
- **Specialized:** Target 65+ (less frequently used)
- **Experimental:** Accept 60+ (temporary, will improve)

---

## Evaluation Tips

### Quick Evaluation (5 minutes)
Focus on red flags and obvious issues for fast triage:
1. Check length (77 lines = likely template)
2. Scan for examples (none = probably weak)
3. Check for specificity (generic = low value)
4. Estimate total score, flag for full eval if borderline

### Full Evaluation (15 minutes)
Complete systematic evaluation using all five dimensions

### Batch Evaluation
When evaluating multiple skills:
1. Group by category/type
2. Evaluate 5-10 skills in one session
3. Compare within groups for consistency
4. Take breaks to avoid evaluation fatigue

---

## Maintenance & Improvement

### Regular Skill Audits
- **Monthly:** Quick evaluation of new skills
- **Quarterly:** Full evaluation of random 20% sample
- **Annually:** Complete library re-evaluation

### Continuous Improvement
- Track scores over time
- Measure impact of improvements
- Identify patterns in low-scoring skills
- Refine evaluation criteria based on experience

### Community Feedback
- Collect usage data (which skills are actually used?)
- Gather user feedback on skill quality
- Incorporate insights into evaluations
- Update scoring criteria as needed

---

## Limitations

This evaluation framework:
- ✅ Provides objective, research-based assessment
- ✅ Identifies quality issues systematically
- ✅ Guides improvement efforts effectively
- ❌ Cannot measure real-world usage patterns (need analytics)
- ❌ Cannot predict agent success rates (need testing)
- ❌ Is subjective within dimensions (human judgment required)

Use evaluation scores as one input to decision-making, not the only input.

---

## See Also

Related skills:
- `cc-writing-skills` - How to create high-quality skills
- `cc-gardening-skills-wiki` - Maintaining skill library health
- `dev-systematic-debugging` - Example of high-quality skill structure

Related documentation:
- `.claude-state/skill-systems-research-report.md` - Full research findings
- `SKILLS_CATALOG_REPORT.md` - Current skill inventory
- `skills_catalog.json` - Machine-readable catalog

---

## Version History

**v1.0.0** (2025-11-10)
- Initial release
- Five-dimension evaluation framework
- Research-backed scoring criteria
- Comprehensive examples and calibration guide

---

## License

This skill is part of the Claude Code Professional Autonomy Harness and is available under the same license as the parent project.
