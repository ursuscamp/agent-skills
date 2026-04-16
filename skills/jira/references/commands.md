# Jira Commands

Use this file when you need concrete command patterns for the local `jira` CLI.

## Setup and discovery

```bash
command -v jira
jira version
jira --help
jira init --help
jira me
jira serverinfo
jira project list
jira board list
```

## Issue search

```bash
jira issue list
jira issue list --plain --columns key,summary,status,assignee
jira issue list --plain --no-headers --columns key,summary
jira issue list --jql 'project = ENG AND assignee = currentUser() AND status != Done' --plain
jira issue list --created week --plain
jira issue list --updated -2d --plain
```

Notes:

- `jira issue list` supports relative filters like `today`, `week`, `month`, `year`, or periods such as `-10d`.
- Use `--paginate <from>:<limit>` when you need more than the default window.

## Issue details

```bash
jira issue view ENG-123
jira issue view ENG-123 --comments 5 --plain
jira issue view ENG-123 --raw
```

## Attachments

The local `jira` CLI does not expose a built-in attachment download command in this environment.
Use the helper script in this skill to bridge that gap:

```bash
python3 skills/jira/scripts/download_attachment.py ENG-123 --list
python3 skills/jira/scripts/download_attachment.py ENG-123 --attachment-name report.pdf --output-dir /tmp/jira-downloads
python3 skills/jira/scripts/download_attachment.py ENG-123 --attachment-id 10042 --header "Authorization: Bearer ..."
python3 skills/jira/scripts/download_attachment.py ENG-123 --attachment-id 10042 --basic-user user@example.com --basic-token secret
```

Notes:

- The script calls `jira issue view ISSUE-KEY --raw` unless `--metadata-file` is supplied.
- If the issue has multiple attachments, pass `--attachment-name` or `--attachment-id`.
- The script auto-uses `~/.config/agent-skills/config.json` when it contains `jira.bearer_token` or `jira.basic_user` plus `jira.basic_token`.
- Keep task defaults there too, such as `jira.project` and `jira.output_dir`.
- If attachment downloads return HTTP 401 or 403, retry with explicit auth headers or cookies.

## Create and update

```bash
jira issue create -p ENG -t Task -s "Add retry guard" -b "Description" --no-input
jira issue create -p ENG -t Story -s "Improve onboarding" --template /path/to/body.md --no-input
printf '%s\n' "Long description" | jira issue create -p ENG -t Bug -s "Investigate 500" --template -

jira issue edit ENG-123 -s "Updated summary" -b "Updated description" --no-input
jira issue edit ENG-123 -l backend -l urgent --no-input
jira issue edit ENG-123 --fix-version v1.2.0 --no-input
```

Notes:

- `jira issue edit` appends labels but replaces components.
- Prefix a label, component, or fix version with `-` to remove it, for example `--label -urgent`.

## Collaboration and workflow

```bash
jira issue comment add ENG-123 "Looking into this now"
printf '%s\n' "Multiline\ncomment" | jira issue comment add ENG-123 --template -

jira issue assign ENG-123 "$(jira me)"
jira issue assign ENG-123 default
jira issue assign ENG-123 x

jira issue move ENG-123 "In Progress"
jira issue move ENG-123 Done --comment "Shipped in 1.2.0"

jira issue worklog add ENG-123 "45m" --comment "Reviewed logs" --no-input
jira issue worklog add ENG-123 "2h" --started "2026-04-02 09:30:00" --timezone "America/New_York" --no-input
```

## Epics and sprints

```bash
jira epic list --table --plain
jira epic list ENG-456 --plain
jira epic add ENG-456 ENG-123 ENG-124

jira sprint list --table --plain
jira sprint list --current --plain
jira sprint list 123 --plain --columns key,summary,status
jira sprint add 123 ENG-123 ENG-124
```

## Releases and browser handoff

```bash
jira release list
jira open
jira open ENG-123
jira open ENG-123 --no-browser
```

## Help-first rule

Before using a command you have not used recently, inspect its live help:

```bash
jira <command> --help
jira <command> <subcommand> --help
```
