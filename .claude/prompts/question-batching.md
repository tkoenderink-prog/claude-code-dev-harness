# Question Batching Strategy

Intelligent question batching for minimal user interruption.

## Batching Rules

### Batch Triggers
1. **Count threshold**: 3+ questions accumulated
2. **Time threshold**: 2 hours since last batch
3. **Context switch**: Major task transition
4. **Milestone**: Sprint or phase completion

### Priority Levels
```python
PRIORITY_LEVELS = {
    "P0": "Blocker - Immediate escalation required",
    "P1": "Critical - Include in next batch",
    "P2": "Important - Can wait for full batch",
    "P3": "Nice to know - Include if space"
}
```

### Batching Algorithm
```python
def should_batch_now(questions, last_batch_time):
    # P0 bypasses batching
    if any(q.priority == "P0" for q in questions):
        return True

    # Count threshold
    if len(questions) >= 3:
        return True

    # Time threshold
    if (datetime.now() - last_batch_time).hours >= 2:
        if len(questions) > 0:
            return True

    # Context switch with questions
    if context_switching() and len(questions) > 0:
        return True

    return False
```

## Question Format

### Individual Question Structure
```yaml
question:
  id: uuid
  priority: P0|P1|P2|P3
  category: technical|business|process
  summary: "Brief question"
  context: "Detailed context"
  options:
    - label: "Option A"
      description: "Full description"
      recommended: true
      impact: "What happens if chosen"
    - label: "Option B"
      description: "Alternative approach"
      impact: "Different outcome"
  default_action: "Option A"
  timeout: 30m
  created_at: timestamp
```

### Batch Presentation Template
```markdown
## Decision Batch - {timestamp}

**Context**: {current_project_state}
**Batch Size**: {question_count}
**Response Needed By**: {timeout}

---

### Question 1: {category} - {priority}
**{summary}**

{context}

**Options:**
- **A: {option_a_label}** {recommended_badge}
  {option_a_description}
  Impact: {option_a_impact}

- **B: {option_b_label}**
  {option_b_description}
  Impact: {option_b_impact}

**Recommendation**: Option {recommended}
**Default**: Will proceed with {default} if no response by {timeout}

---

### Question 2: ...

---

### Quick Answers Format
For efficiency, you can respond with:
```
1: A
2: B (with modification: ...)
3: Default
```

Or provide detailed feedback for specific questions.
```

## Batching Windows

### Optimal Times
- Morning batch: 9:00 AM - 10:00 AM
- Afternoon batch: 2:00 PM - 3:00 PM
- End-of-day: 5:00 PM - 6:00 PM

### Anti-patterns to Avoid
- Never batch during deep work (10 AM - 12 PM)
- Avoid dinner time (6 PM - 8 PM)
- Skip weekends unless critical

## Response Processing

```python
def process_batch_response(response, questions):
    for question_id, answer in parse_response(response):
        question = find_question(question_id, questions)

        if answer == "default":
            action = question.default_action
        elif answer in question.options:
            action = answer
        else:
            action = parse_custom_answer(answer)

        execute_decision(question, action)
        record_decision(question, action, "user")
```

## Learning and Optimization

### Pattern Detection
```python
def learn_from_responses(decisions):
    patterns = {}

    for decision in decisions:
        key = (decision.category, decision.question_type)
        if key not in patterns:
            patterns[key] = []
        patterns[key].append(decision.chosen)

    # If consistent pattern, auto-decide in future
    for key, choices in patterns.items():
        if len(choices) >= 3 and len(set(choices)) == 1:
            create_auto_decision_rule(key, choices[0])
```

### Batch Effectiveness Metrics
- Response rate: % of batches answered
- Response time: Average time to respond
- Default rate: % using default actions
- Pattern emergence: Rules learned/week

## Integration Example

```python
# In orchestrator.md
from prompts.question_batching import BatchManager

batch_manager = BatchManager()

# Add question
batch_manager.add_question(
    priority="P2",
    category="technical",
    summary="Database choice",
    options=["PostgreSQL", "MySQL"],
    default="PostgreSQL"
)

# Check if should send
if batch_manager.should_send_batch():
    response = batch_manager.send_batch()
    batch_manager.process_response(response)
```

## Emergency Override

For true emergencies:
```python
def emergency_escalation(question):
    if question.is_security_issue():
        send_immediate_alert()
        bypass_all_batching()
        require_immediate_response()
```