# agent-skills

This repository contains local agent skill definitions plus a small installer script that syncs them into the shared agent skills directory.

## What’s here

- [`skills/`](./skills) - source skill folders for this repo
- [`install-skills`](./install-skills) - syncs local skills into the shared skills directory

## How it works

`install-skills` looks for subdirectories under [`skills/`](./skills) that contain a `SKILL.md` file. Each matching skill is copied into:

- `~/.agents/skills/<skill-name>` by default

You can override the target location with:

- `AGENTS_HOME`
- `AGENTS_SKILLS_DIR`

The script also removes installed skills that no longer exist in the source tree, so the destination stays in sync.

## Usage

```bash
./install-skills --once
```

Run it without `--once` to keep watching for changes and resync automatically.

## Current skills

- [`jira`](./skills/jira/SKILL.md) - Jira workflows via the local `jira` CLI, including issue search, editing, comments, and sprint/epic operations
- [`github`](./skills/github/SKILL.md) - GitHub workflows via the local `gh` CLI, including auth, repo targeting, issues, pull requests, workflows, releases, and API calls
- [`spec-dev`](./skills/spec-dev/SKILL.md) - staged spec-driven development workflow for features and bugs
- [`neovim-plugin-dev`](./skills/neovim-plugin-dev/SKILL.md) - Neovim expertise and plugin development workflow with cached local help docs
- [`playwright-cli`](./skills/playwright-cli/SKILL.md) - browser automation workflow for the Playwright coding-agent CLI, including snapshots, sessions, captures, and advanced debugging

## Adding a new skill

1. Create a new folder under [`skills/`](./skills).
2. Add a `SKILL.md` file to that folder.
3. Run `./install-skills --once` to publish it to the shared skills directory.
