---
name: project-glossary
description: Defines format and workflow for maintaining a project glossary of terms used in spec-driven development
---

## What I do

I define how the spec agent creates, updates, and maintains a glossary of project-specific terms. The glossary ensures consistent terminology across all spec documents (requirements.md, design.md, tasks.md).

## Glossary File Location

All glossary entries live in: `spec/glossary.md` (project root)

This is the single source of truth for project terminology.

## Required Entry Format

Every glossary entry MUST follow this structure:

```markdown
## [Term Name]

**Definition:** [Clear, concise definition of the term]

**Context:** [When/where this term applies in your project - specific usage scenario]

**Example:** [Concrete usage example from your project - code snippet, user flow, etc.]

**Related Terms:** [comma-separated list of related glossary terms]
```

### Entry Requirements

1. **Alphabetical ordering** - Terms must be in alphabetical order within each category/section
2. **Bidirectional links** - When adding a term to "Related Terms", ensure the related term also references back
3. **No duplicates** - Check if term exists before adding; update existing entry if scope changes
4. **Rich examples** - Examples should be from actual project code, APIs, or user flows

## Entry Management Rules

### Adding New Terms

1. Check existing glossary for similar/related terms first
2. Verify term doesn't already exist (case-insensitive check)
3. Place in correct alphabetical position
4. Add bidirectional related term links
5. If term is domain-specific (e.g., "Stripe Customer"), consider prefixes

### Updating Existing Terms

- **Definition change**: Update the definition in place
- **New example**: Add to existing entry, keep examples current
- **Deprecation**: Mark as `**Deprecated:** [replacement term]` with note

### Validation

Before finalizing any spec document, verify:
- [ ] All terms in requirements.md are in glossary
- [ ] All terms in design.md are in glossary
- [ ] Related Terms links are bidirectional
- [ ] Examples are current and accurate

## Spec Agent Workflow Integration

### Stage 1: Before Writing Requirements

1. Load `spec/glossary.md`
2. Review existing terms relevant to the feature
3. Suggest applicable terms to include in requirements
4. Note any undefined terms that will need creation

### Stage 2: While Writing Requirements

1. Flag any undefined terms encountered
2. Use the `question` tool to ask: "Add [term] to glossary?"
3. If adding, create entry with:
   - Working definition (can refine later)
   - Context: "Used in requirements.md for [feature]"
   - Placeholder example: "[Example to be added in design phase]"
   - Related Terms: [linked terms]

### Stage 3: Before Design

1. Review all terms from requirements not yet in glossary
2. Enhance definitions with implementation context
3. Add concrete examples from expected implementation
4. Create Related Terms connections

### Stage 4: During Design

1. Add technical terms and component names
2. Update examples with actual interface signatures
3. Link data models to relevant terms

### Stage 5: After Implementation

1. Review terms for accuracy
2. Add any new terms discovered during implementation
3. Mark any temporary definitions as finalized

## Quality Guidelines

### Good Term Definitions

- **Good:** "A unique identifier generated for each user session, stored in an HTTP-only cookie"
- **Bad:** "A thing that tracks users" (too vague)

### Good Examples

- Include actual code snippets, API signatures, or CLI commands
- Show the term in context of your project
- Avoid generic placeholder examples

### Good Related Terms

- Link semantically related terms
- Include parent/child relationships (e.g., "User" → "Admin User")
- Include opposing terms if applicable (e.g., "Sync" → "Async")

## Important Rules

1. **Always check glossary first** - Before using a term, verify it exists
2. **Never duplicate** - If term exists, reference it; don't create new entry
3. **Bidirectional links** - Related Terms must go both ways
4. **Concrete examples** - Generic examples don't help; use actual project patterns
5. **Maintain alphabetical order** - Keep entries sorted for discoverability
6. **Load before spec creation** - Always load glossary when starting new requirements or design
