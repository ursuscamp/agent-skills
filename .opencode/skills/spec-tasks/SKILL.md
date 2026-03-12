---
name: spec-tasks
description: Defines the format for implementation task checklists in spec-driven development
compatibility: opencode
metadata:
  audience: developers
  workflow: spec-driven-development
---

## What I do

When you create or update a `tasks.md` file, follow this exact format. This file serves as the execution plan - complete tasks by marking them with `[x]`. Do NOT use OpenCode's todo tool; use this file instead.

## Required Structure

### 1. Header

```markdown
# [Feature Name] - Implementation Tasks
```

### 2. Overview Section

Brief summary of the implementation:
- Estimated total tasks
- Key milestones
- Dependencies overview

### 3. Implementation Checklist

The core of this file. Format as markdown checklist with sub-checklists.

#### Task Numbering

- Use **1., 2., 3.** for top-level tasks
- Use **1.1, 1.2, 1.3** for subtasks (indented 2 spaces)
- Use **1.1.1, 1.1.2** for sub-subtasks if needed (indented 4 spaces)

#### Checkbox Format

```markdown
- [ ] **1.** [Task description]
  - [ ] **1.1** [Subtask description]
  - [ ] **1.2** [Subtask description]
    - [ ] **1.2.1** [Sub-subtask description]
- [ ] **2.** [Task description]
```

- `[ ]` = incomplete
- `[x]` = complete

#### Task Attributes

Each task should include (inline, after description):
- **(depends on: #N)** - Task dependency reference
- **(test: <approach>)** - How to test this task

Example:
```markdown
- [ ] **1.** Set up database schema
  - [ ] **1.1** Create users table (test: verify table exists)
  - [ ] **1.2** Add indexes for email, created_at (depends on: 1.1)
```

### 4. Task Grouping

Group tasks by module/component. Use headings:

```markdown
## Backend

## Frontend

## Infrastructure

## Testing
```

### 5. Completion Summary

At the end of the file, include:

```markdown
---

## Completion Summary

| Phase | Tasks | Completed | Progress |
|-------|-------|-----------|----------|
| Backend | 12 | 8 | 67% |
| Frontend | 8 | 2 | 25% |
| Total | 20 | 10 | 50% |
```

## Task Naming Conventions

### Good Task Names
- "Create user model with name, email, password fields"
- "Add POST /api/users endpoint"
- "Write unit tests for UserService.validate()"

### Bad Task Names
- "Work on backend" (too vague)
- "Fix bugs" (not specific)
- "Do testing" (no scope)

## Example Complete Structure

```markdown
# User Authentication - Implementation Tasks

## Overview

Total: 15 tasks
Estimated completion: 2 days
Prerequisites: None

## Backend

- [ ] **1.** Set up authentication service
  - [ ] **1.1** Create AuthService class (test: instantiate service)
  - [ ] **1.2** Configure JWT settings (depends on: 1.1)
  - [ ] **1.3** Add token refresh logic (depends on: 1.2)
- [ ] **2.** Create user authentication endpoints
  - [ ] **2.1** POST /auth/login endpoint
    - [ ] **2.1.1** Validate credentials (test: mock request with valid/invalid creds)
    - [ ] **2.1.2** Return JWT token (test: verify token in response)
  - [ ] **2.2** POST /auth/logout endpoint (depends on: 2.1)
  - [ ] **2.3** POST /auth/refresh endpoint (depends on: 2.1)
- [ ] **3.** Add password hashing
  - [ ] **3.1** Implement bcrypt compare (test: verify hash verification)
  - [ ] **3.2** Add password validation rules (test: test various passwords)

## Frontend

- [ ] **4.** Create login form component
  - [ ] **4.1** Add email input field
  - [ ] **4.2** Add password input field
  - [ ] **4.3** Add submit button with loading state
- [ ] **5.** Implement authentication state management
  - [ ] **5.1** Create auth context
  - [ ] **5.2** Store JWT in localStorage (test: verify token persistence)

## Testing

- [ ] **6.** Write unit tests
  - [ ] **6.1** Test AuthService.validateCredentials()
  - [ ] **6.2** Test password hashing
- [ ] **7.** Write integration tests
  - [ ] **7.1** Test login flow end-to-end
  - [ ] **7.2** Test token refresh flow

---

## Completion Summary

| Phase | Tasks | Completed | Progress |
|-------|-------|-----------|----------|
| Backend | 8 | 0 | 0% |
| Frontend | 4 | 0 | 0% |
| Testing | 3 | 0 | 0% |
| **Total** | **15** | **0** | **0%** |
```

## Important Rules

1. **Never use the todo tool** - This file IS your todo list
2. **Mark tasks complete immediately** - As soon as a task is done, update `[ ]` to `[x]`
3. **Update summary on completion** - Recalculate progress when marking complete
4. **Check dependencies** - Don't start a task if its dependencies aren't done
5. **Be specific** - Each task should be completable in 1-4 hours max
6. **Include testing** - Every feature task should have a test task
