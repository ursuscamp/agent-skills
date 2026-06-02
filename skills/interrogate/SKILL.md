---
name: interrogate
description: Use when any software development request needs to be clarified before work begins, with a bias toward exploring the codebase first and asking one question at a time until the user and agent are fully aligned.
---

# Interrogate

Use this skill when a software development request needs tighter alignment before implementation.

## What this skill does

- Explore the codebase, docs, tests, and existing patterns first when the answer can be learned locally
- Ask exactly one question at a time
- Focus on the highest-risk unknowns first
- Restate the current understanding after each answer
- Keep asking until the request, constraints, and success criteria are fully aligned

## Workflow

1. Inspect the repository for relevant code, docs, tests, and conventions.
2. If the needed information is not available locally, ask one focused question.
3. After each answer, summarize the current understanding in one short paragraph.
4. Identify the next most important unknown and ask the next single question.
5. Continue until there are no material ambiguities left.

## Question style

- Prefer open-ended questions when they help surface intent
- Use multiple-choice only when it reduces ambiguity materially
- Avoid bundling multiple decisions into one question
- Keep the conversation moving toward concrete decisions

## Outcome

Stop only when the plan, scope, constraints, and expected result are clear enough to proceed confidently.
