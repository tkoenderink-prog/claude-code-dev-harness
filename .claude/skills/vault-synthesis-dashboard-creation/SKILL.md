---
name: Synthesis Dashboard Creation
description: Dataview-powered dashboards transform vault into actionable system through project, area, and task views
when_to_use: when creating overview notes, project dashboards, area summaries, or need consolidated views
version: 1.0.0
languages: all
---

# Synthesis Dashboard Creation

## Overview

**Dashboards make knowledge actionable. Without them, you have a pile of notes.**

Obsidian Dataview transforms static notes into dynamic views that:
- Surface relevant information automatically
- Track progress across projects
- Consolidate tasks by context
- Show knowledge connections

**Core principle:** Mix manual insights (why/context) with Dataview queries (what/current state).

## When to Use

**Create dashboard when:**
- Starting new project (project dashboard)
- Managing area (area dashboard)
- Need task visibility (task rollup dashboard)
- Topic has 7+ notes (topic/MOC dashboard)
- Multiple projects in same domain (consolidated view)

**Update dashboard during:**
- Weekly review (skills/obsidian/vault-weekly-review Phase 4)
- Project milestones
- Significant vault changes

## Dashboard Types

### Type 1: Project Dashboard

**Purpose:** Track single project progress, tasks, resources

```markdown
---
type: project-dashboard
project: [[Project Name]]
auto-update: dataview
---

# 🚀 Project Name Dashboard

## Current Status
- **Phase**: Planning | Execution | Review
- **Progress**: ████░░░░░░ 40%
- **Next Milestone**: [[Milestone Name]] - Due: 2025-11-15
- **Health**: 🟢 On Track | 🟡 At Risk | 🔴 Blocked

## Definition of Done
<!-- From project note, keep visible -->
1. [ ] Specific outcome 1
2. [ ] Specific outcome 2
3. [ ] Specific outcome 3

## Active Tasks
\`\`\`dataview
TASK
FROM "01-PROJECTS/Project Name"
WHERE !completed
SORT priority DESC, due ASC
\`\`\`

## Recent Activity
\`\`\`dataview
LIST file.mtime AS "Modified"
FROM "01-PROJECTS/Project Name"
SORT file.mtime DESC
LIMIT 5
\`\`\`

## Resources
<!-- Manual: Key resources being used -->
- [[Resource 1]] - Purpose/usage
- [[Resource 2]] - Purpose/usage

## Blockers & Risks
<!-- Manual: Updated during review -->
| Issue | Impact | Mitigation | Status |
|-------|--------|------------|--------|
| Example blocker | High | Action plan | 🟡 Active |

## Weekly Progress Notes
<!-- Manual: Brief weekly updates -->
### Week {{date:ww}} ({{date:YYYY-MM-DD}})
- **Accomplished**:
- **Learned**:
- **Next week focus**:

## Key Links
- Project Plan: [[Project Name]]
- Related Area: [[Area Name]]
- Team/Stakeholders: [[Person 1]], [[Person 2]]
```

**When to create:** Immediately when starting project (part of project setup)

### Type 2: Area Dashboard

**Purpose:** Ongoing responsibility management, standards tracking

```markdown
---
type: area-dashboard
area: [[Area Name]]
auto-update: dataview
---

# 📊 Area Name Dashboard

## Area Overview
<!-- Manual: What this area is about -->
**Purpose**: [Responsibility definition]

**Current Focus**: [What you're prioritizing right now]

## Standards & Health
<!-- Manual: What "good" looks like -->
- **Standard 1**: [Metric/description] - 🟢/🟡/🔴
- **Standard 2**: [Metric/description] - 🟢/🟡/🔴
- **Standard 3**: [Metric/description] - 🟢/🟡/🔴

**Overall Health**: 🟢 Healthy | 🟡 Needs Attention | 🔴 At Risk

## Active Projects in This Area
\`\`\`dataview
TABLE
  status AS "Status",
  deadline AS "Deadline",
  priority AS "Priority"
FROM "01-PROJECTS"
WHERE contains(area, "[[Area Name]]") OR contains(tags, "area-tag")
AND status = "active"
SORT deadline ASC
\`\`\`

## Recurring Activities
<!-- Manual: Regular responsibilities -->
| Activity | Frequency | Last Done | Next Due | Status |
|----------|-----------|-----------|----------|--------|
| Example activity | Weekly | 2025-10-15 | 2025-10-22 | ✅ |

## Key Metrics
<!-- Manual or semi-automated -->
| Metric | Target | Current | Trend |
|--------|--------|---------|-------|
| Metric 1 | Goal | Actual | ↗️/→/↘️ |
| Metric 2 | Goal | Actual | ↗️/→/↘️ |

## Recent Notes
\`\`\`dataview
LIST file.ctime AS "Created"
FROM "02-AREAS/Area Name"
SORT file.ctime DESC
LIMIT 10
\`\`\`

## Sub-Areas & Structure
<!-- Manual: Navigate complex area -->
- [[Sub-Area 1]] - Description
- [[Sub-Area 2]] - Description

## Resources & References
\`\`\`dataview
TABLE
  type AS "Type"
FROM "03-RESOURCES"
WHERE contains(tags, "area-tag") OR contains(file.outlinks, [[Area Name]])
SORT file.name ASC
\`\`\`

## Review Notes
### {{date:YYYY-MM}} Review
<!-- Manual: Monthly/quarterly reflection -->
- **What's working**:
- **What needs improvement**:
- **Adjustments made**:

## Quick Actions
- [ ] Add new project: [[Template|New Project]]
- [ ] Log activity: [[Daily Note]]
- [ ] Review metrics: [External tool/spreadsheet]
```

**When to create:** When area has multiple projects or complex structure

### Type 3: Task Rollup Dashboard

**Purpose:** See all tasks across vault by context

```markdown
---
type: task-dashboard
auto-update: dataview
---

# ✅ Task Dashboard

Last updated: {{date:YYYY-MM-DD HH:mm}}

## Due Today
\`\`\`dataview
TASK
WHERE due = date(today)
AND !completed
SORT priority DESC
\`\`\`

## Due This Week
\`\`\`dataview
TASK
WHERE due >= date(today)
AND due <= date(today) + dur(7 days)
AND !completed
SORT due ASC
\`\`\`

## Overdue ⚠️
\`\`\`dataview
TASK
WHERE due < date(today)
AND !completed
SORT due ASC
\`\`\`

## High Priority
\`\`\`dataview
TASK
WHERE priority = "high"
AND !completed
SORT due ASC
\`\`\`

## By Project
\`\`\`dataview
TASK
WHERE !completed
AND contains(file.path, "PROJECTS")
GROUP BY file.link
SORT rows.due ASC
\`\`\`

## By Area
\`\`\`dataview
TASK
WHERE !completed
AND contains(file.path, "AREAS")
GROUP BY file.folder
SORT file.folder ASC
\`\`\`

## Waiting For
\`\`\`dataview
TASK
FROM "01-PROJECTS" OR "02-AREAS"
WHERE contains(text, "waiting") OR contains(text, "blocked")
AND !completed
\`\`\`

## Recently Completed (Last 7 Days)
\`\`\`dataview
TASK
WHERE completed
AND completion >= date(today) - dur(7 days)
SORT completion DESC
LIMIT 20
\`\`\`

## Summary Statistics
<!-- Manual update during weekly review -->
- **Total active tasks**: [Count]
- **Due this week**: [Count]
- **Overdue**: [Count]
- **Completed this week**: [Count]
```

**When to create:** When managing 20+ tasks across vault

### Type 4: Topic/MOC Dashboard

**Purpose:** Navigate topic with 7+ notes

```markdown
---
type: moc-dashboard
topic: Topic Name
---

# 📚 Topic Name MOC

*Comprehensive overview of [topic] across the vault*

Last reviewed: {{date:YYYY-MM-DD}}

## Core Concepts
<!-- Manual: Foundational notes -->
- [[Concept 1]] - Brief description
- [[Concept 2]] - Brief description
- [[Concept 3]] - Brief description

## Active Work
\`\`\`dataview
TABLE
  status AS "Status",
  deadline AS "Deadline"
FROM "01-PROJECTS"
WHERE contains(tags, "topic-tag") OR contains(file.outlinks, [[Topic Name]])
AND status = "active"
SORT deadline ASC
\`\`\`

## Learning Path
<!-- Manual: Recommended sequence -->
1. Start: [[Beginner Topic Note]]
2. Then: [[Intermediate Topic Note]]
3. Advanced: [[Advanced Topic Note]]

## All Notes on This Topic
\`\`\`dataview
LIST
FROM #topic-tag OR [[Topic Name]]
WHERE file.name != "Topic Name MOC"
SORT file.name ASC
\`\`\`

## Resources & References
\`\`\`dataview
TABLE
  type AS "Type",
  file.ctime AS "Added"
FROM "03-RESOURCES"
WHERE contains(tags, "topic-tag")
SORT file.ctime DESC
\`\`\`

## Recent Activity
\`\`\`dataview
LIST file.mtime AS "Modified"
FROM #topic-tag
SORT file.mtime DESC
LIMIT 10
\`\`\`

## Related Topics
<!-- Manual: Cross-topic connections -->
- [[Related Topic 1]] - Relationship
- [[Related Topic 2]] - Relationship

## External Resources
<!-- Manual: Books, courses, websites -->
- Resource name - Link/description
```

**When to create:** When topic reaches 7+ notes scattered across vault

## Dataview Query Patterns

### Essential Queries

| Goal | Dataview Query |
|------|---------------|
| **Active projects** | `FROM "01-PROJECTS" WHERE status = "active"` |
| **Recent notes** | `WHERE file.mtime > date(today) - dur(7 days)` |
| **By tag** | `FROM #tag-name` or `WHERE contains(tags, "tag-name")` |
| **By link** | `FROM [[Note Name]]` (all notes linking to it) |
| **Tasks due soon** | `TASK WHERE due <= date(today) + dur(7 days)` |
| **Tasks overdue** | `TASK WHERE due < date(today) AND !completed` |
| **Group by** | `GROUP BY file.folder` or `GROUP BY project` |
| **High priority** | `WHERE priority = "high"` |

### Common Patterns

**Filter by path:**
```dataview
FROM "01-Private/01-PROJECTS"
WHERE file.name != "Index"
```

**Combine conditions:**
```dataview
FROM "01-PROJECTS"
WHERE status = "active"
AND deadline <= date(today) + dur(30 days)
AND priority = "high"
```

**Table with specific fields:**
```dataview
TABLE
  status AS "Status",
  deadline AS "Due",
  priority AS "Priority"
FROM "01-PROJECTS"
SORT deadline ASC
```

**Group and count:**
```dataview
TABLE length(rows) AS "Count"
FROM "01-PROJECTS"
GROUP BY status
SORT status ASC
```

## Dashboard Maintenance

### Manual Sections (Update Weekly)

- **Current Status** (Phase, Progress %, Health)
- **Standards & Health** (Green/yellow/red indicators)
- **Blockers & Risks** (Active issues)
- **Progress Notes** (Weekly/monthly updates)
- **Review Notes** (Reflections, adjustments)

### Dataview Sections (Auto-Update)

- **Task lists** (due dates, priorities)
- **Recent notes** (modifications, creations)
- **Project lists** (active, by area)
- **Resources** (tagged, linked)

### Verification

Before considering dashboard complete:

- [ ] **Dataview queries working?**
  - Open in Obsidian
  - Verify each query displays results
  - Fix syntax errors

- [ ] **Manual sections filled?**
  - Status/health indicators set
  - Context/purpose written
  - Initial metrics recorded

- [ ] **Dashboard linked from relevant notes?**
  - Project → Dashboard link in project note
  - Area → Dashboard in area folder
  - Main → Dashboard from main Dashboard.md

## Dashboard Design Principles

### Principle 1: Manual + Dataview Balance

```markdown
❌ BAD: All Dataview (no context)
# Dashboard
\`\`\`dataview
LIST FROM "PROJECTS"
\`\`\`

✅ GOOD: Context + Data
# Dashboard

**Current Focus**: Consolidating family support systems

**Why This Matters**: Coordinating Kai's care requires visibility across
health, education, and financial projects.

\`\`\`dataview
TABLE status, deadline
FROM "01-PROJECTS"
WHERE contains(tags, "family")
\`\`\`
```

**Principle:** Humans provide why/context, Dataview provides what/current.

### Principle 2: Actionability

Every dashboard should answer:
- What should I do today? (Tasks, next actions)
- What needs attention? (Health indicators, overdue)
- What's changing? (Recent activity, trends)

### Principle 3: Progressive Disclosure

```markdown
## High-Level Status
[Quick overview with health indicators]

## Active Work
[Current projects/tasks]

## Detailed Views
[Comprehensive tables, all notes]

## Historical Data
[Completed items, past performance]
```

**Top = most urgent/relevant, Bottom = reference/historical**

## Integration with Other Skills

**Uses:**
- skills/obsidian/vault-obsidian-linking-strategy (Linking dashboard to content)
- skills/obsidian/vault-creating-obsidian-notes (Dashboard creation workflow)

**Called by:**
- skills/obsidian/vault-weekly-review (Dashboard updates Phase 4)

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| **Only Dataview** | No context, looks like database dump | Add manual insights, why this matters |
| **Only manual** | Goes stale quickly, requires constant updates | Add Dataview for current data |
| **Complex queries** | Slow rendering, hard to maintain | Keep queries simple, use multiple simple queries |
| **No links to dashboard** | Dashboard orphaned, never seen | Link from project notes, main dashboard, MOCs |
| **Stale manual sections** | Health shows green when actually red | Update during weekly review (Phase 4) |

## Red Flags - Improve Dashboard

If you catch yourself:
- "Dashboard shows outdated information" → Add Dataview for that section
- "Dashboard is just a list of tasks" → Add context, why, focus areas
- "Can't find the dashboard" → Link prominently from related notes
- "Dashboard takes 30 sec to load" → Simplify queries, reduce scope
- "Never look at this dashboard" → Missing actionable info or too generic

**ALL mean: Redesign dashboard following principles above**

## Success Criteria

You know dashboard works when:
- Open it at least weekly (it's useful)
- Manual sections stay current (updated during reviews)
- Dataview sections show live data (queries working)
- Answers "what should I do?" (actionable)
- Helps make decisions (relevant insights)

## Time Investment

- **Create project dashboard**: 10-15 minutes
- **Create area dashboard**: 15-20 minutes
- **Create task rollup**: 10 minutes
- **Create MOC dashboard**: 20-30 minutes

- **Update during weekly review**: 2-5 minutes per dashboard

**ROI:** 15 minutes creating saves hours searching/organizing manually

## Remember

**Dashboards transform notes into a system. Without dashboards, you have a pile of information.**

Manual context + Dataview current state = Actionable insights

Create dashboards. Update them weekly. Use them daily.
