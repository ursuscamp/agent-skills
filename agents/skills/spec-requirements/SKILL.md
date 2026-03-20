---
name: spec-requirements
description: Defines the format and structure for feature requirements documentation
---

## What I do

When you create or update a `requirements.md` file for a feature specification, follow this exact structure. This skill ensures requirements are complete, testable, and clearly communicated.

## Required Sections

Every `requirements.md` MUST include these sections in order:

### 1. Title

```markdown
# [Feature Name]
```

### 2. Summary

2-3 sentence overview of what this feature accomplishes.

### 3. Problem Statement

Why this feature is needed. Describe the pain point, gap, or opportunity. Include:
- Current state
- Why it matters
- Impact of not solving it

### 4. User Stories

Format as "As a [persona], I want [goal], so that [benefit]."

List in priority order. Include 2-5 user stories.

### 5. Functional Requirements

Numbered checklist of what the system must do. Each requirement should be:
- **Atomic** - One behavior per item
- **Verifiable** - Can be tested/confirmed
- **Clear** - No ambiguity

Format:
```markdown
## Functional Requirements

- [ ] **REQ-001**: [Requirement description]
- [ ] **REQ-002**: [Requirement description]
```

### 6. Non-Functional Requirements

Address these categories when applicable:
- **Performance**: Response times, throughput, resource limits
- **Security**: Authentication, authorization, data protection
- **Scalability**: Expected load, growth projections
- **Reliability**: Availability targets, error handling
- **Compatibility**: Browser support, API versions, backward compatibility
- **Usability**: Accessibility, UX expectations

### 7. Acceptance Criteria

Numbered checklist. Each criterion must be:
- **Specific** - Precise behavior described
- **Measurable** - Can verify completion
- **Testable** - Can write automated tests

Format:
```markdown
## Acceptance Criteria

- [ ] **AC-001**: [Criterion description]
- [ ] **AC-002**: [Criterion description]
```

### 8. Out of Scope

Explicitly list what is NOT included in this feature. This prevents scope creep and sets clear boundaries.

### 9. Assumptions

Document known assumptions about:
- Technical environment
- User behavior
- Third-party services
- Data availability

### 10. Dependencies

List external dependencies:
- **Internal**: Other features, services, teams
- **External**: Third-party APIs, libraries, infrastructure
- **Blocked by**: Prerequisites that must be complete first

## Quality Guidelines

1. **Be specific** - Avoid vague language like "support multiple users" → specify "support up to 100 concurrent users"
2. **Include edge cases** - Document error states, invalid inputs, boundary conditions
3. **Focus on outcomes** - Describe what happens, not how it's implemented
4. **Number references** - Use REQ-XXX and AC-XXX for traceability

## Example

See a complete example at the end of requirements.md when generated.
