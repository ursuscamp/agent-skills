# agent-skills

This repository contains local agent skill definitions plus a small installer script that syncs them into the shared agent skills directory.

## What’s here

- [`skills/`](./skills) - source skill folders for this repo
- [`install-skills`](./install-skills) - syncs local skills into the shared skills directory

## How it works

`install-skills` looks for subdirectories under [`skills/`](./skills) that contain a `SKILL.md` file. Each matching skill is copied into:

- `~/.agents/skills/<skill-name>` by default
- `~/.kiro/skills/<skill-name>` when you pass `--kiro`

You can override the target location with:

- `AGENTS_HOME`
- `AGENTS_SKILLS_DIR`

The script also removes installed skills that no longer exist in the source tree, and it prunes skills that are on that target's ignore list, so the destination stays in sync.

## Usage

```bash
./install-skills
```

```bash
./install-skills --kiro
```

```bash
./install-skills --ignore github
```

Use `--watch` when you want to keep watching for changes and resync automatically.

`--ignore <skill-name>` is persistent for the selected target. If you ignore `github` on the default target, future default syncs will keep skipping it even if you omit the flag. The Kiro target keeps its own separate ignore list.

## Current skills

- [`jira`](./skills/jira/SKILL.md) - Jira workflows via the local `jira` CLI, including issue search, editing, comments, and sprint/epic operations
- [`github`](./skills/github/SKILL.md) - GitHub workflows via the local `gh` CLI, including auth, repo targeting, issues, pull requests, workflows, releases, and API calls
- [`jenkins`](./skills/jenkins/SKILL.md) - Jenkins workflows for branch-aware build lookup, failure and test inspection, console troubleshooting, and triggering parameterized builds
- [`spec-dev`](./skills/spec-dev/SKILL.md) - staged spec-driven development workflow for features and bugs, starting with an interrogation phase
- [`neovim-plugin-dev`](./skills/neovim-plugin-dev/SKILL.md) - Neovim expertise and plugin development workflow with cached local help docs
- [`playwright`](./skills/playwright/SKILL.md) - browser automation workflow for the Playwright coding-agent CLI, including snapshots, sessions, captures, and advanced debugging

## Adding a new skill

1. Create a new folder under [`skills/`](./skills).
2. Add a `SKILL.md` file to that folder.
3. Run `./install-skills` to publish it to the shared skills directory, or `./install-skills --kiro` to publish it to Kiro.
4. If needed, run `./install-skills --ignore <skill-name>` to keep a skill excluded for that target going forward.
