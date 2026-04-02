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

## Base specs directory

Resolve the base specs directory before reading or writing any spec artifact:

1. Check for a project file named `.specs-folder` at the repository root.
2. If it exists, read its contents and treat that path as the base specs directory.
3. If it does not exist, use `specs/` as the base specs directory.

The `.specs-folder` value takes precedence over the default. Treat it as a project-relative path unless the file clearly specifies an absolute path.

## Workspace layout

Store active specs in:

- `[base-specs-dir]/in-progress/[slug]/requirements.md`
- `[base-specs-dir]/in-progress/[slug]/design.md`
- `[base-specs-dir]/in-progress/[slug]/tasks.md`
- `[base-specs-dir]/in-progress/[slug]/bug-report.md`

When implementation is complete, ask:

`Ready to move to completed folder?`

Only after confirmation, move the spec folder to:

- `[base-specs-dir]/complete/[slug]/`

## Slug format

Generate slugs as:

- `YYYYMMDDHHmm-short-feature-name`

Example:

- `202603241045-user-login`

## Workflow

### Features

1. Resolve the base specs directory.
2. Load `[base-specs-dir]/glossary.md` if it exists. If it does not exist, continue without it and create/update it only when needed.
3. Confirm scope with the user if the request is materially ambiguous.
4. Create `requirements.md` using [`references/requirements.md`](references/requirements.md).
5. Stop and ask: `Ready for Design?`
6. Create `design.md` using [`references/design.md`](references/design.md).
7. Stop and ask: `Ready for Tasks?`
8. Create `tasks.md` using [`references/tasks.md`](references/tasks.md).
9. Stop and ask: `Ready to implement?`
10. Implement the work and update `tasks.md` as tasks are completed.

### Bugs

1. Resolve the base specs directory.
2. Load `[base-specs-dir]/glossary.md` if it exists and use consistent project terminology.
3. Investigate enough to write a concrete bug report.
4. Create `bug-report.md` using [`references/bug-report.md`](references/bug-report.md).
5. Stop and ask: `Ready for Tasks?`
6. Create `tasks.md` using [`references/tasks.md`](references/tasks.md).
7. Stop and ask: `Ready to implement?`
8. Implement the fix and update `tasks.md` as tasks are completed.

## Fast forward mode

If the user explicitly asks to "fast forward" or "do all stages":

1. Generate all remaining spec documents in sequence.
2. Do not pause between spec documents.
3. Stop before implementation.
4. Ask for implementation confirmation.

## Glossary handling

When project-specific terms appear, use [`references/glossary.md`](references/glossary.md) to maintain `[base-specs-dir]/glossary.md`.

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
