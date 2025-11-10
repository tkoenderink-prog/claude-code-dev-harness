#!/bin/bash

# Source and destination
SRC="$HOME/.claude/skills"
DEST="./skills"

# Skills to migrate (all 38)
SKILLS=(
  "collision-zone-thinking"
  "context-aware-reasoning"
  "creating-obsidian-notes"
  "deep-dive-research"
  "discovering-relevant-frameworks"
  "discovering-vault-knowledge"
  "domain-specific-application"
  "gardening-skills-wiki"
  "inversion-exercise"
  "maintaining-book-notes"
  "maintaining-influential-people-notes"
  "maintaining-mental-model-notes"
  "meta-pattern-recognition"
  "mitigation-strategies"
  "mobility-cycle-design"
  "mobility-session-design"
  "moving-notes-safely"
  "obsidian-linking-strategy"
  "para-classification-decisions"
  "physical-training-benchmark-week"
  "pre-decision-checklist"
  "preserving-productive-tensions"
  "pulling-updates-from-skills-repository"
  "quick-recognition"
  "remembering-conversations"
  "retrieving-journal-entries"
  "scale-game"
  "simplification-cascades"
  "solving-with-frameworks"
  "strength-cycle-design"
  "strength-workout-design"
  "synthesis-dashboard-creation"
  "thinking-through-a-decision"
  "tracing-knowledge-lineages"
  "understanding-with-frameworks"
  "using-skills"
  "vault-weekly-review"
  "when-stuck"
)

# Copy each skill
copied=0
missing=0

for skill in "${SKILLS[@]}"; do
  if [ -d "$SRC/$skill" ]; then
    echo "Copying $skill..."
    cp -r "$SRC/$skill" "$DEST/"
    ((copied++))
  else
    echo "WARNING: $skill not found in $SRC"
    ((missing++))
  fi
done

echo ""
echo "Migration complete:"
echo "  Copied: $copied skills"
echo "  Missing: $missing skills"
