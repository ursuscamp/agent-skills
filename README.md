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

## Shared config

Some skill scripts read a shared JSON config file for non-interactive defaults and secrets:

- `~/.config/agent-skills/config.json`

This file lives on your machine, outside the repo, so `install-skills` will not create or sync it.

Use sections to keep values organized by skill:

```json
{
  "jenkins": {
    "url": "https://jenkins.example.com",
    "user": "your-user",
    "token": "your-api-token"
  },
  "jira": {
    "bearer_token": "your-bearer-token",
    "basic_user": "user@example.com",
    "basic_token": "your-api-token",
    "project": "ENG",
    "output_dir": "/tmp/jira-downloads"
  },
  "defaults": {
    "output_dir": "/tmp/shared-downloads"
  }
}
```

Scripts read their skill section first, then `defaults`, then top-level keys. That keeps one file usable across skills without forcing every script to share the same schema.

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

- [`jira`](./skills/jira/SKILL.md) - Jira workflows via the local `jira` CLI, including issue search, editing, comments, sprint/epic operations, and attachment downloads with shared config
- [`github`](./skills/github/SKILL.md) - GitHub workflows via the local `gh` CLI, including auth, repo targeting, issues, pull requests, workflows, releases, and API calls
- [`jenkins`](./skills/jenkins/SKILL.md) - Jenkins workflows for branch-aware build lookup, failure and test inspection, console troubleshooting, and triggering parameterized builds from shared config
- [`spec-dev`](./skills/spec-dev/SKILL.md) - staged spec-driven development workflow for features and bugs, starting with an interrogation phase
- [`neovim-plugin-dev`](./skills/neovim-plugin-dev/SKILL.md) - Neovim expertise and plugin development workflow with cached local help docs
- [`playwright`](./skills/playwright/SKILL.md) - browser automation workflow for the Playwright coding-agent CLI, including snapshots, sessions, captures, and advanced debugging
- [`web-search`](./skills/web-search/SKILL.md) - live web search and page fetch workflow via Exa's hosted MCP server using `npx mcporter` (`web_search_exa`, `web_fetch_exa`)

## Adding a new skill

1. Create a new folder under [`skills/`](./skills).
2. Add a `SKILL.md` file to that folder.
3. Run `./install-skills` to publish it to the shared skills directory, or `./install-skills --kiro` to publish it to Kiro.
4. If needed, run `./install-skills --ignore <skill-name>` to keep a skill excluded for that target going forward.
