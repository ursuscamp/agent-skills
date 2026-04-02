# GitHub CLI Command Patterns

This reference reflects the local `gh` installation observed on April 2, 2026: `gh version 2.55.0`.
Re-check `gh --help` when exact flags matter.

## Install and discover

```bash
command -v gh
gh --version
gh --help
gh help reference
gh help formatting
gh help environment
```

## Authentication and account context

```bash
gh auth status
gh auth login
gh auth switch
gh auth refresh -s project
gh auth setup-git
gh auth token
```

Notes:

- `gh auth status` shows the active account, git protocol, and token scopes for each known host.
- Use `gh auth refresh -s <scope>` when a command fails because the current token lacks a needed scope.

## Repository targeting and discovery

```bash
gh repo view
gh repo view owner/repo
gh repo set-default --view
gh repo set-default owner/repo
GH_REPO=owner/repo gh issue list
gh browse
gh browse --repo owner/repo
```

Notes:

- Prefer `-R owner/repo` on individual commands when the target repository is ambiguous.
- Use `gh repo set-default` for repeated work in one checkout.

## Repository operations

```bash
gh repo list
gh repo list owner
gh repo clone owner/repo
gh repo fork owner/repo
gh repo create owner/new-repo --private --clone
gh repo sync owner/repo
gh repo edit owner/repo --description "Example description"
```

## Issue workflows

```bash
gh issue list
gh issue list -R owner/repo --json number,title,state,assignees
gh issue view 123
gh issue view 123 -R owner/repo --json number,title,body,labels,assignees
gh issue create --title "Bug: widget fails" --body "Steps to reproduce"
gh issue create -R owner/repo --title "Docs follow-up" --body-file /tmp/body.md --label docs
gh issue comment 123 --body "Investigating now"
gh issue edit 123 --add-label bug --remove-label triage
gh issue close 123 --comment "Fixed in #456"
```

## Pull request workflows

```bash
gh pr list
gh pr list -R owner/repo --json number,title,headRefName,reviewDecision
gh pr view 456
gh pr view 456 --json number,title,body,commits,reviews
gh pr checkout 456
gh pr diff 456
gh pr checks 456
gh pr create --title "Add retry guard" --body "Fixes #123"
gh pr create --fill --draft
gh pr review 456 --approve
gh pr review 456 --comment --body "Looks good overall"
gh pr review 456 --request-changes --body "Please add regression coverage"
gh pr merge 456 --squash --delete-branch
```

Notes:

- `gh pr create --dry-run` is helpful for checking the payload before creating a PR, but it may still push git changes.
- Use `--body-file -` to stream multiline bodies from stdin.

## Search and status

```bash
gh status
gh search repos "agent skills" --limit 10
gh search issues "repo:owner/repo is:open label:bug"
gh search prs "org:owner review-requested:@me state:open"
```

## Actions and releases

```bash
gh workflow list
gh workflow view ci.yml
gh run list
gh run view 123456789
gh run watch 123456789
gh release list
gh release view v1.2.3
gh release create v1.2.4 --generate-notes
```

## Structured output

```bash
gh pr list --json number,title,author
gh pr list --json number,title,author --jq '.[] | {number, title, author: .author.login}'
gh issue list --json number,title,url --template '{{range .}}{{printf "#%v %s\\n" .number .title}}{{end}}'
```

Notes:

- Omit field names once with `--json` to discover the available JSON field set for that command.
- `--jq` is built into `gh`; a separate `jq` binary is not required for those queries.

## REST and GraphQL escape hatches

```bash
gh api repos/{owner}/{repo}
gh api repos/{owner}/{repo}/pulls --jq '.[].title'
gh api -X GET search/issues -f q='repo:owner/repo is:open is:issue'
gh api repos/{owner}/{repo}/issues/123/comments -f body='Working on this'
gh api graphql -F owner='{owner}' -F name='{repo}' -f query='
  query($owner: String!, $name: String!) {
    repository(owner: $owner, name: $name) {
      defaultBranchRef { name }
    }
  }
'
gh api graphql --paginate -f query='
  query($endCursor: String) {
    viewer {
      repositories(first: 100, after: $endCursor) {
        nodes { nameWithOwner }
        pageInfo { hasNextPage endCursor }
      }
    }
  }
'
```

## Non-interactive and troubleshooting patterns

```bash
GH_PROMPT_DISABLED=1 gh pr create --title "Add retry guard" --body "Fixes #123"
GH_REPO=owner/repo gh issue list
GH_DEBUG=api gh api repos/{owner}/{repo}
```

## Help-first rule

Before using a command you have not used recently, inspect its live help:

```bash
gh <command> --help
gh <command> <subcommand> --help
```
