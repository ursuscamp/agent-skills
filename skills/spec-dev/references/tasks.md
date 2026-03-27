# Tasks Format

Use this structure for `tasks.md`:

1. `# [Feature Name] - Implementation Tasks`
2. `## Overview`
3. One or more implementation sections such as:
   - `## Backend`
   - `## Frontend`
   - `## Infrastructure`
   - `## Testing`
4. Completion summary table

## Checklist format

Top-level tasks:

```markdown
- [ ] **1.** Task description
```

Subtasks:

```markdown
  - [ ] **1.1** Subtask description
```

Sub-subtasks:

```markdown
    - [ ] **1.1.1** Sub-subtask description
```

## Rules

- Use `tasks.md` as the actual execution checklist.
- Mark tasks complete immediately by changing `[ ]` to `[x]`.
- Keep each task specific enough to finish in roughly 1-4 hours.
- Include dependency notes when needed:
  - `(depends on: 1.1)`
- Include test notes when helpful:
  - `(test: verify endpoint returns 200)`
- Recalculate the completion summary as work progresses.
