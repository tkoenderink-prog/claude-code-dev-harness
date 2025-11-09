# Decision Framework

Reusable decision logic for autonomous operation.

## Decision Categories

### 1. Autonomous Decisions (95%)
Make without user input when:
- Clear technical solution exists
- Follows established patterns
- Within defined constraints
- Reversible with low impact
- Time-sensitive but not critical

### 2. Batched Decisions (4%)
Accumulate and batch when:
- Multiple valid approaches exist
- Preferences unclear
- Medium impact on timeline
- Could benefit from user context
- Not blocking immediate progress

### 3. Immediate Escalation (1%)
Escalate immediately when:
- Security implications
- Financial impact
- Legal/compliance issues
- Production deployment
- Breaking API changes

## Decision Matrix

```python
def evaluate_decision(decision):
    score = 0

    # Factors increasing autonomy
    if has_precedent(decision):
        score += 30
    if is_reversible(decision):
        score += 25
    if follows_patterns(decision):
        score += 20
    if low_risk(decision):
        score += 15

    # Factors requiring escalation
    if security_impact(decision):
        score -= 50
    if financial_impact(decision):
        score -= 40
    if external_dependency(decision):
        score -= 30
    if unclear_requirements(decision):
        score -= 20

    # Thresholds
    if score >= 50:
        return "AUTONOMOUS"
    elif score >= 0:
        return "BATCH"
    else:
        return "ESCALATE"
```

## Decision Documentation

Every decision must record:
```yaml
decision:
  id: uuid
  timestamp: datetime
  category: technical|business|process
  question: "What was decided"
  options:
    - option: "Option A"
      pros: ["pro1", "pro2"]
      cons: ["con1", "con2"]
      risk: low|medium|high
  chosen: "Option A"
  rationale: "Why this was chosen"
  decided_by: orchestrator|user|specialist
  confidence: 0.0-1.0
  reversible: true|false
  impact: low|medium|high
```

## Learning from Decisions

After each decision:
1. Record in decisions.yaml
2. Extract pattern if repeated
3. Update confidence scores
4. Adjust thresholds based on outcomes

## Default Actions

When user doesn't respond to batched questions:
1. Wait for configured timeout (default: 30min)
2. Apply recommended option
3. Document as "default-applied"
4. Continue with execution
5. Report in next interaction

## Confidence Scoring

```python
def calculate_confidence(decision):
    confidence = 0.5  # Base confidence

    # Boost factors
    if similar_past_decision_succeeded():
        confidence += 0.2
    if clear_technical_best_practice():
        confidence += 0.15
    if all_tests_pass():
        confidence += 0.1
    if documentation_exists():
        confidence += 0.05

    # Reduction factors
    if new_technology():
        confidence -= 0.2
    if conflicting_patterns():
        confidence -= 0.15
    if high_complexity():
        confidence -= 0.1

    return min(max(confidence, 0.0), 1.0)
```

## Usage in Agents

```python
from prompts.decision_framework import evaluate_decision

decision = {
    "question": "Which testing framework to use?",
    "options": ["Jest", "Mocha", "Vitest"],
    "context": {...}
}

action = evaluate_decision(decision)

if action == "AUTONOMOUS":
    make_decision(decision)
elif action == "BATCH":
    add_to_batch(decision)
else:
    escalate_immediately(decision)
```