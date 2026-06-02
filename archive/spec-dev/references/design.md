# Design Format

Use this structure for `design.md`:

1. `# [Feature Name] - Technical Design`
2. `## Architecture Overview`
3. `## Interface Design`
4. `## Data Models`
5. `## Key Components`
6. `## User Interaction`
7. `## External Dependencies`
8. `## Error Handling`
9. `## Security`
10. `## Configuration`
11. `## Component Interactions`
12. `## Platform Considerations`

## Rules

- Keep interface descriptions shallow: describe what the interface does, not how it works internally.
- Include signatures, request/response shapes, parameter constraints, and protocols where relevant.
- For data models, document fields, types, constraints, and schema changes.
- For key components, describe responsibilities, public API, and dependencies.
- Use pseudocode only for truly complex algorithms.
- Include recovery strategies for expected failures.
- Document authentication, authorization, input validation, secrets handling, and least-privilege concerns as applicable.
