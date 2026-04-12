---
name: spec-intake
description: Use when a user wants to start a new feature or bug spec for spec-dev, but the request needs a focused interview first to resolve scope, constraints, edge cases, terminology, and acceptance criteria before writing any spec.
---

# Spec Intake

Use this skill to interview the user before creating a spec with `spec-dev`.

## Goal

Get the agent and user fully aligned on the request before any requirements, design, bug report, or task document is written.

## Workflow

1. Identify whether the request is a feature or a bug.
2. Ask the smallest useful set of questions first, usually 1-3 at a time.
3. Cover the parts that most often create spec churn:
   - desired outcome
   - current behavior or pain point
   - who is affected
   - constraints and non-goals
   - edge cases and failure modes
   - acceptance criteria
   - rollout, migration, or compatibility concerns
   - any project-specific terminology the user wants preserved
4. Prefer multiple-choice questions when they will collapse ambiguity quickly. Use open-ended questions when the space is still unclear.
5. After each answer, restate the updated understanding and call out any remaining unknowns.
6. Keep drilling until you can summarize the request without guessing.
7. Before handing off, give a concise confirmation summary and ask the user to confirm that the understanding is complete.
8. Once confirmed, invoke `spec-dev`:
   - feature request -> requirements flow
   - bug request -> bug report flow

## Interview Rules

- Do not write spec artifacts while the request is still being clarified.
- Do not move on when there are unresolved conflicts between possible interpretations.
- Separate facts, assumptions, and preferences.
- If the user is unsure about a detail, capture the ambiguity explicitly and propose the tradeoff.
- Keep the tone collaborative and precise, not ceremonial.

## Handoff Criteria

Treat the intake as complete only when all of these are true:

- The user goal is clear.
- The scope boundaries are clear.
- The important edge cases are known or acknowledged.
- The success criteria are testable.
- The main dependencies or constraints are identified.
- The user agrees that the summary matches their intent.

Then proceed with `spec-dev` using the clarified request.
