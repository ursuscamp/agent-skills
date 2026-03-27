---
name: spec-dev
description: Use when the user wants staged spec-driven development in a generic workflow, including requirements, design, bug reports, task plans, and implementation gated by explicit confirmation between stages.
---

# Spec-Driven Development

Use this skill when a user wants to plan work through specs before implementation.

## What this skill does

This skill supports a staged spec-driven workflow in a generic, tool-agnostic form:

- Feature flow: `requirements.md` -> `design.md` -> `tasks.md` -> implementation
- Bug flow: `bug-report.md` -> `tasks.md` -> implementation
- After each file, stop and ask for confirmation before continuing
- If the user says "fast forward" or "do all stages", generate all remaining spec files, then stop before implementation

## Non-negotiable rule

Before creating any spec file for a new stage, ask for confirmation and wait for the user's answer.

Valid confirmations include `yes`, `proceed`, `continue`, `ready`, or `fast forward`.

## Workspace layout

Store active specs in:

- `specs/in-progress/[slug]/requirements.md`
- `specs/in-progress/[slug]/design.md`
- `specs/in-progress/[slug]/tasks.md`
- `specs/in-progress/[slug]/bug-report.md`

When implementation is complete, ask:

`Ready to move to completed folder?`

Only after confirmation, move the spec folder to:

- `specs/complete/[slug]/`

## Slug format

Generate slugs as:

- `YYYYMMDDHHmm-short-feature-name`

Example:

- `202603241045-user-login`

## Workflow

### Features

1. Load `specs/glossary.md` if it exists. If it does not exist, continue without it and create/update it only when needed.
2. Confirm scope with the user if the request is materially ambiguous.
3. Create `requirements.md` using [`references/requirements.md`](references/requirements.md).
4. Stop and ask: `Ready for Design?`
5. Create `design.md` using [`references/design.md`](references/design.md).
6. Stop and ask: `Ready for Tasks?`
7. Create `tasks.md` using [`references/tasks.md`](references/tasks.md).
8. Stop and ask: `Ready to implement?`
9. Implement the work and update `tasks.md` as tasks are completed.

### Bugs

1. Load `specs/glossary.md` if it exists and use consistent project terminology.
2. Investigate enough to write a concrete bug report.
3. Create `bug-report.md` using [`references/bug-report.md`](references/bug-report.md).
4. Stop and ask: `Ready for Tasks?`
5. Create `tasks.md` using [`references/tasks.md`](references/tasks.md).
6. Stop and ask: `Ready to implement?`
7. Implement the fix and update `tasks.md` as tasks are completed.

## Fast forward mode

If the user explicitly asks to "fast forward" or "do all stages":

1. Generate all remaining spec documents in sequence.
2. Do not pause between spec documents.
3. Stop before implementation.
4. Ask for implementation confirmation.

## Glossary handling

When project-specific terms appear, use [`references/glossary.md`](references/glossary.md) to maintain `specs/glossary.md`.

Always:

- Check whether a term already exists before adding it
- Keep entries alphabetized
- Keep related-term links bidirectional when possible
- Prefer concrete examples from the actual project

## Implementation behavior

During implementation:

- Treat `tasks.md` as the canonical execution checklist
- Mark completed items as `[x]` immediately
- Update completion summary as progress changes
- Preserve the staged intent of the spec unless the user explicitly changes scope

## Writing guidance

- Be specific and testable
- Separate requirements from implementation details
- Call out assumptions and out-of-scope items
- Keep designs shallow at interfaces and deeper on responsibilities
- Include error states and verification paths

## References

- Requirements format: [`references/requirements.md`](references/requirements.md)
- Design format: [`references/design.md`](references/design.md)
- Tasks format: [`references/tasks.md`](references/tasks.md)
- Bug report format: [`references/bug-report.md`](references/bug-report.md)
- Glossary workflow: [`references/glossary.md`](references/glossary.md)
