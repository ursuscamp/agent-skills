---
name: jenkins
description: Use when working with Jenkins jobs and builds from the terminal, especially to find builds for the current git branch, inspect build or test failures, troubleshoot Jenkins console logs, or trigger new builds with or without parameters.
---

# Jenkins

Use this skill to ground Jenkins work in the live job and build data instead of guessing from partial logs or stale links.

Start with read-only inspection. Confirm the current repository branch, identify the relevant Jenkins job or multibranch job, and only trigger a build after the target job and parameters are clear.

## Quick Start

1. Check the local git context:

```bash
git rev-parse --show-toplevel
git rev-parse --abbrev-ref HEAD
git rev-parse HEAD
```

2. Create the shared skill config file:

```bash
mkdir -p ~/.config/agent-skills
cat > ~/.config/agent-skills/config.json <<'JSON'
{
  "jenkins": {
    "url": "https://jenkins.example.com",
    "user": "your-user",
    "token": "your-api-token"
  }
}
JSON
```

Use `--config /path/to/config.json` if the config is not at the default location.

3. Use the helper script for the common workflows in this skill:

```bash
python3 skills/jenkins/scripts/jenkins_helper.py --help
python3 skills/jenkins/scripts/jenkins_helper.py list-jobs
python3 skills/jenkins/scripts/jenkins_helper.py list-jobs --job Github-Purple
python3 skills/jenkins/scripts/jenkins_helper.py show-params --job folder/repo
python3 skills/jenkins/scripts/jenkins_helper.py branch-builds --job folder/repo
python3 skills/jenkins/scripts/jenkins_helper.py build-summary --job folder/repo --build 123
python3 skills/jenkins/scripts/jenkins_helper.py console --job folder/repo --build 123 --tail 120
python3 skills/jenkins/scripts/jenkins_helper.py trigger-build --job folder/repo --param BRANCH_NAME="$(git rev-parse --abbrev-ref HEAD)"
```

Use `--job` with a Jenkins job path like `folder/repo` or a full job URL. For a multibranch pipeline, prefer the branch-specific job path if one exists.

## Workflow

### Discover folders, repos, and branch jobs

- Use `list-jobs` with no `--job` to list the Jenkins root.
- Pass a folder or multibranch repo path to drill in.
- Add `--recursive` with a higher `--depth` when you want nested output in one call.

Examples:

```bash
python3 skills/jenkins/scripts/jenkins_helper.py list-jobs
python3 skills/jenkins/scripts/jenkins_helper.py list-jobs --job Github-Purple
python3 skills/jenkins/scripts/jenkins_helper.py list-jobs --job Github-Purple/pmpaware-webapp
python3 skills/jenkins/scripts/jenkins_helper.py list-jobs --depth 3 --recursive
```

### Find builds for the current branch

- Start with `branch-builds` and let the helper infer the current git branch by default.
- Prefer a branch-specific multibranch job when available because the mapping is usually exact.
- For classic parameterized jobs, pass the shared job and let the helper match by branch-like parameter names or build revision metadata.
- If the job is ambiguous, inspect a recent build with `build-summary` before claiming it belongs to the branch.
- If you pass a multibranch repo root and a branch name, the helper can resolve the branch child job and will print the resolved path.

Examples:

```bash
python3 skills/jenkins/scripts/jenkins_helper.py branch-builds --job folder/repo
python3 skills/jenkins/scripts/jenkins_helper.py branch-builds --job folder/repo --branch release/2026.04 --limit 20
python3 skills/jenkins/scripts/jenkins_helper.py branch-builds --job https://jenkins.example.com/job/folder/job/repo/
```

### Check failures and test results

- Use `build-summary` first. It combines build metadata, parameters, test result counts, failed tests, and a console tail.
- If the job has no published test report, rely on the console section and build result.
- Keep the summary tight, then drill into the raw console only when needed.

Examples:

```bash
python3 skills/jenkins/scripts/jenkins_helper.py build-summary --job folder/repo --build 123
python3 skills/jenkins/scripts/jenkins_helper.py build-summary --job folder/repo --build 123 --console-lines 200 --failed-test-limit 20
```

### Troubleshoot console logs

- Use `console` when you need more than the summary tail.
- Start with `--tail` before dumping the full log.
- Add `--grep` to isolate stack traces, test names, or common failure markers.

Examples:

```bash
python3 skills/jenkins/scripts/jenkins_helper.py console --job folder/repo --build 123 --tail 200
python3 skills/jenkins/scripts/jenkins_helper.py console --job folder/repo --build 123 --grep 'FAIL|ERROR|Exception'
```

### Trigger new builds

- Use `show-params` first when you do not know the accepted Jenkins parameter names or defaults.
- Confirm the exact target job before posting anything.
- Use `trigger-build` without parameters for plain builds.
- Use repeated `--param KEY=VALUE` flags for parameterized jobs.
- Add `--wait` when you want the helper to follow the queue item, print the started build number, and wait for completion.
- Mirror the parameter names used by recent successful builds when the expected names are unclear.

Examples:

```bash
python3 skills/jenkins/scripts/jenkins_helper.py show-params --job folder/repo
python3 skills/jenkins/scripts/jenkins_helper.py trigger-build --job folder/repo
python3 skills/jenkins/scripts/jenkins_helper.py trigger-build --job folder/repo --param BRANCH_NAME=main --param TEST_SUITE=smoke
python3 skills/jenkins/scripts/jenkins_helper.py trigger-build --job folder/repo --param BRANCH_NAME=main --wait
```

## Working Style

- Prefer read-only discovery first: branch lookup, build summary, then console details, then triggering.
- Quote exact branch names, build numbers, and parameter names in the response so the user can verify them quickly.
- When the user says "current branch", resolve it with local git commands rather than assuming.
- When the user mentions "latest" or "today", anchor the answer to the exact build number and timestamp returned by Jenkins.
- If the job uses folders or multibranch layout, keep the full job path in the response to avoid ambiguity.
- If Jenkins auth or crumbs fail, report the HTTP status and the missing config fields instead of guessing.

## References

- Branch matching heuristics, auth expectations, and API patterns: [`references/workflow.md`](references/workflow.md)
- Reusable helper for branch lookup, failure summaries, console logs, and parameterized triggers: [`scripts/jenkins_helper.py`](scripts/jenkins_helper.py)
