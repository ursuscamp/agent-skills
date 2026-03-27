# Requirements Format

Use this structure for `requirements.md`:

1. `# [Feature Name]`
2. `## Summary`
3. `## Problem Statement`
4. `## User Stories`
5. `## Functional Requirements`
6. `## Non-Functional Requirements`
7. `## Acceptance Criteria`
8. `## Out of Scope`
9. `## Assumptions`
10. `## Dependencies`

## Rules

- User stories should follow: `As a [persona], I want [goal], so that [benefit].`
- Functional requirements must be atomic, clear, and verifiable.
- Number functional requirements as checkboxes:
  - `- [ ] **REQ-001**: Description`
- Number acceptance criteria as checkboxes:
  - `- [ ] **AC-001**: Description`
- Requirements should describe outcomes, not implementation details.
- Include important edge cases, invalid inputs, and boundary conditions.

## Non-functional categories

Address these when relevant:

- Performance
- Security
- Scalability
- Reliability
- Compatibility
- Usability
