---
name: github
description: Use when Codex needs to work with GitHub through the local `gh` GitHub CLI, including authentication, repository inspection, issue and pull request workflows, release and workflow inspection, GitHub API or GraphQL calls, browsing, search, and repository-scoped automation from the terminal.
---

# GitHub CLI Workflow

Use this skill to ground GitHub work in the locally installed `gh` CLI instead of guessing command syntax or reaching for raw API calls too early.

Start by checking the exact command surface in the current environment:

```bash
command -v gh
gh --version
gh --help
```

## Quick Start

1. Verify authentication with `gh auth status`.
2. Confirm repository targeting before acting with `git remote -v`, `gh repo set-default --view`, or explicit `-R OWNER/REPO`.
3. Prefer read-only discovery commands first, then mutations only after the user clearly asks for them.
4. Prefer `--json` with `--jq` or `--template` when you need deterministic summaries or machine-readable output.
5. Check `gh <command> <subcommand> --help` before using uncommon flags or less-frequent subcommands.

## Working Style

- Prefer explicit repository scoping with `-R OWNER/REPO` when outside a cloned repo, when multiple remotes exist, or when there is any ambiguity.
- Prefer `gh repo set-default OWNER/REPO` or `GH_REPO=OWNER/REPO` for repeated work against one repository.
- Use `gh auth status` before assuming which account or token scope is active.
- Summarize the planned mutation before running create, edit, close, merge, review, or delete commands unless the user already requested that exact action.
- Prefer `gh api` only when a higher-level `gh issue`, `gh pr`, `gh repo`, `gh workflow`, or `gh run` command does not expose the needed operation cleanly.
- Use `GH_PROMPT_DISABLED=1` plus explicit flags when you need non-interactive behavior.

## Common Workflows

### Authenticate and inspect context

- Use `gh auth login` to add an account.
- Use `gh auth switch` when multiple accounts are configured.
- Use `gh auth refresh -s <scope>` when a command needs extra scopes such as `project`.
- Use `gh auth setup-git` when git operations should reuse GitHub CLI auth.

### Target the right repository

- In a cloned repo, `gh` usually infers the target from git remotes.
- Outside a repo, or when inference is risky, pass `-R OWNER/REPO`.
- For repeated work in one checkout, use `gh repo set-default OWNER/REPO`.

### Inspect repositories, issues, and pull requests

- Use `gh repo view`, `gh issue list`, `gh issue view`, `gh pr list`, and `gh pr view` for normal inspection.
- Use `gh status` for a cross-repository view of relevant pull requests, issues, and notifications.
- Use `gh search repos`, `gh search issues`, or `gh search prs` when the target repository is not yet known.

### Create and update issues and pull requests

- Use explicit flags such as `--title`, `--body`, `--body-file`, `--label`, `--assignee`, and `--reviewer` to avoid interactive prompts.
- Use `gh pr create --fill` when the branch history has a clean title and body source, then override with `--title` or `--body` if needed.
- Use `gh pr review --approve`, `--comment`, or `--request-changes` for review state changes.
- Mention `Fixes #123` or `Closes #123` in PR bodies when the merge should close an issue.

### Inspect workflows, runs, releases, and browser views

- Use `gh workflow list` and `gh run list` or `gh run view` to inspect GitHub Actions state.
- Use `gh release list` and `gh release view` for release work.
- Use `gh browse` or `--web` variants to hand off to the browser when the web UI is faster or clearer.

### Use structured output and API escape hatches

- Prefer `--json` over scraping terminal tables.
- Add `--jq` for lightweight filtering without requiring a separate `jq` install.
- Use `--template` when you need concise tabular or custom text output.
- Use `gh api repos/{owner}/{repo}/...` for REST calls and `gh api graphql` for GraphQL queries.
- Use `--paginate` and `--slurp` when traversing large result sets.

## Environment Notes

- `GH_TOKEN` or `GITHUB_TOKEN` can override stored auth for `github.com`.
- `GH_HOST` selects a GitHub Enterprise host when needed.
- `GH_REPO` sets the default repository in `[HOST/]OWNER/REPO` form.
- `GH_DEBUG=api` is useful when you need HTTP-level troubleshooting.
- `GH_PROMPT_DISABLED=1` disables interactive prompting for automation-oriented runs.

## References

- Command patterns and examples: [`references/commands.md`](references/commands.md)
