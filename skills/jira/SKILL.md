---
name: jira
description: Use when working with Jira through the local `jira` command line tool from `ankitpokhrel/jira-cli`, including configuring access, listing projects or boards, searching issues, viewing issue details, downloading attachments, creating or editing tickets, adding comments, transitioning status, managing epics or sprints, or logging work.
---

# Jira Workflow

Use this skill to ground Jira work in the locally installed CLI instead of guessing command syntax.

Start with the documented read path for the task, and only check `--help` when you need an unfamiliar flag or the installed CLI seems different from the examples here.

Prefer read-only discovery first, then write operations only after the user clearly asks for them.

## Quick Start

1. Verify the CLI exists with `command -v jira`.
2. Verify configuration with `jira me` or `jira serverinfo`.
3. If the CLI is not configured, use `jira init` and follow the prompts or pass flags explicitly.
4. Discover the current project, board, or issue state before changing anything.
5. For scripted or machine-readable output, prefer `--plain` or `--raw` over the default interactive views.

## Working Style

- Prefer explicit project scoping with `-p <PROJECT>` when the task mentions a project or when multiple projects may be configured.
- Prefer non-interactive flags such as `--no-input`, `--plain`, `--no-headers`, and `--raw` when you need deterministic output or are driving the CLI from an automated workflow.
- Check `jira <command> <subcommand> --help` before using less common flags or when the installed CLI appears to differ from the examples here.
- Summarize the planned mutation before running create, edit, move, comment, sprint-add, epic-add, or worklog commands unless the user already asked for that exact action.
- When the user asks for "today", "this week", or similar relative periods, translate that into the CLI's supported date filters or use exact dates when that avoids ambiguity.

## Common Tasks

### Configure Jira CLI

- Inspect setup help with `jira init --help`.
- Typical verification flow:

```bash
jira me
jira project list
jira board list
```

The Jira CLI config path shown by this installation is `/Users/rbreen/.config/.jira/.config.yml`.

### Search and inspect issues

- Use `jira issue list` for filtered search.
- Use `jira issue view ISSUE-123 --plain` for a single issue.
- Prefer table/plain output when you need to summarize several issues.

Examples:

```bash
jira issue list --plain --columns key,summary,status,assignee
jira issue list --jql 'assignee = currentUser() AND status != Done' --plain
jira issue view ISSUE-123 --comments 5 --plain
```

### Download attachments

- The CLI does not expose a built-in attachment download command in this environment.
- Use [`scripts/download_attachment.py`](scripts/download_attachment.py) to fetch attachment metadata via `jira issue view --raw` and then download the selected attachment over HTTP.
- Select the attachment with `--attachment-name` or `--attachment-id`. If the issue has exactly one attachment, the script can pick it automatically.
- The script can auto-authenticate from `~/.config/agent-skills/config.json` using `jira.bearer_token` or `jira.basic_user` plus `jira.basic_token`.
- Put other defaults there too, such as `jira.project` or `jira.output_dir`.
- Pass auth explicitly when needed:
  - `--header 'Authorization: Bearer ...'`
  - `--basic-user <email> --basic-token <token>`
  - `--cookie 'name=value'`
- Prefer `--output-dir` to keep downloads organized per task.

Examples:

```bash
python3 skills/jira/scripts/download_attachment.py ENG-123 --attachment-name report.pdf --output-dir /tmp/jira-downloads
python3 skills/jira/scripts/download_attachment.py ENG-123 --attachment-id 10042 --basic-user user@example.com --basic-token secret
python3 skills/jira/scripts/download_attachment.py ENG-123 --header "Authorization: Bearer bearer-token"
```

### Create and edit issues

- Use `jira issue create` with explicit flags for summary, type, body, assignee, labels, and priority.
- Use `jira issue edit` for updates.
- Prefer `--template -` or a file when the description is multiline.
- Use `--no-input` when you want the command to fail fast instead of prompting interactively.

Examples:

```bash
jira issue create -p ENG -t Task -s "Add retry guard" -b $'Context\n\nAcceptance criteria' --no-input
printf '%s\n' "Detailed description" | jira issue create -p ENG -t Story -s "Improve onboarding" --template -
jira issue edit ENG-123 -s "Updated summary" -l backend -l urgent --no-input
```

### Comment, assign, transition, and log work

- Add comments with `jira issue comment add`.
- Assign with `jira issue assign`.
- Transition state with `jira issue move`.
- Log time with `jira issue worklog add`.

Examples:

```bash
jira issue comment add ENG-123 $'Investigated root cause\n\nWaiting on deploy'
jira issue assign ENG-123 "$(jira me)"
jira issue move ENG-123 "In Progress"
jira issue worklog add ENG-123 "1h 30m" --comment "Investigated flaky test" --no-input
```

### Epics, sprints, and releases

- Use `jira epic list` to list epics or issues in an epic.
- Use `jira epic add` to attach issues to an epic.
- Use `jira sprint list --table --plain` to inspect sprint IDs and current state.
- Use `jira sprint add` to add issues to a sprint.
- Use `jira release list` to inspect project versions.

## Output Modes

The CLI defaults to interactive explorers for several commands. For terminal automation and concise summaries:

- Use `--plain` for plain text tables.
- Add `--no-headers` when you only need rows.
- Use `--columns` to reduce noise.
- Use `--raw` when JSON is available and you need structured data.
- Avoid assuming `--raw` exists on every subcommand; check help first.

## References

- Common commands and patterns: [`references/commands.md`](references/commands.md)
