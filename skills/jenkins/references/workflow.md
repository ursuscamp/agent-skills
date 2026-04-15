# Jenkins Workflow Notes

Use this reference when you need the details behind the skill's helper script or when you need to improvise direct API calls.

## Authentication

The helper script reads a JSON config file first, then falls back to CLI flags and environment variables.

Default config path:

- `~/.config/jenkins-helper/config.json`

Override it with:

- `--config /path/to/config.json`

Expected JSON shape:

```json
{
  "url": "https://jenkins.example.com",
  "user": "your-user",
  "token": "your-api-token"
}
```

Override precedence is:

1. `--url`, `--user`, `--token`
2. Config file fields: `url`, `user`, `token`
3. Environment variables: `JENKINS_URL`, `JENKINS_USER`, `JENKINS_TOKEN`

It uses HTTP basic auth and will attempt to fetch a CSRF crumb from `/crumbIssuer/api/json` before POST requests. If the crumb endpoint is unavailable, it falls back to a plain POST because some Jenkins instances do not require crumbs for API-token-authenticated requests.

## Job Addressing

Use one of these forms:

- Job path: `folder/repo`
- Nested job path: `team/backend/repo`
- Full job URL: `https://jenkins.example.com/job/team/job/backend/job/repo/`

The helper converts slash-delimited paths into Jenkins `job/.../job/...` URLs automatically.

## Listing Jobs

Use `list-jobs` to discover:

- Root folders and top-level jobs
- Repositories inside an organization folder such as `Github-Purple`
- Branch jobs inside a multibranch repo such as `Github-Purple/pmpaware-webapp`

Examples:

```bash
python3 skills/jenkins/scripts/jenkins_helper.py list-jobs
python3 skills/jenkins/scripts/jenkins_helper.py list-jobs --job Github-Purple
python3 skills/jenkins/scripts/jenkins_helper.py list-jobs --job Github-Purple/pmpaware-webapp
python3 skills/jenkins/scripts/jenkins_helper.py list-jobs --depth 3 --recursive
```

Output is tab-separated:

- path
- Jenkins class
- URL

## Branch Matching Heuristics

`branch-builds` tries several signals, in this order:

1. Exact branch names found in `lastBuiltRevision.branch`
2. Branch-like build parameters such as `BRANCH_NAME`, `BRANCH`, `GIT_BRANCH`, `git_branch`, `branch`, or `CHANGE_BRANCH`
3. Git revision matches against the current local `HEAD`

Normalization strips common prefixes such as:

- `origin/`
- `refs/heads/`
- `refs/remotes/origin/`
- `*/`

That helps a local branch like `feature/foo` match Jenkins metadata like `origin/feature/foo` or `refs/heads/feature/foo`.

## Build Inspection

`build-summary` gathers:

- Core metadata: display name, URL, result, running state, timestamp, duration
- Parameters and causes
- SCM revision and branch hints
- Test report counts and failing cases from `testReport/api/json`
- Console tail from `consoleText`

If the job does not publish a JUnit-style report, the helper still returns the build result and console output.

## Inspecting Parameters

Use `show-params` to inspect Jenkins parameter definitions before triggering a job:

```bash
python3 skills/jenkins/scripts/jenkins_helper.py show-params --job Github-Purple/pmpaware-webapp/develop
```

The helper prints:

- Parameter name
- Jenkins parameter type
- Default value when Jenkins exposes one
- Choices for choice parameters
- Description text when present

## Console Analysis Tips

Start narrow:

- `--tail 100` for the failure epilogue
- `--grep 'FAIL|ERROR|Exception'` for a noise-reduced view
- Increase `--tail` only if the failure cause is still unclear

When summarizing a failure for the user, prefer:

1. The failing stage or command
2. The first actionable error line
3. The failing test names or counts
4. Any branch or parameter mismatch that explains why the wrong build ran

## Triggering Builds

Use:

- `/build` for jobs without parameters
- `/buildWithParameters` when at least one `--param` is present

Common parameter examples:

- `BRANCH_NAME=feature/foo`
- `GIT_BRANCH=origin/feature/foo`
- `TEST_SUITE=smoke`
- `ENVIRONMENT=staging`

If you do not know the parameter names, inspect a recent build first and reuse the keys returned in its parameter list.

When you want the helper to block until Jenkins finishes the new build, add `--wait`:

```bash
python3 skills/jenkins/scripts/jenkins_helper.py trigger-build --job folder/repo --param BRANCH_NAME=main --wait
```

With `--wait`, the helper:

1. Triggers the build
2. Polls the Jenkins queue until the executable build number exists
3. Prints the started build number and URL
4. Polls the running build until it completes
5. Exits non-zero if the final Jenkins result is not `SUCCESS`

## JenkinsAPI Notes

The user provided [JenkinsAPI docs](https://pycontribs.github.io/jenkinsapi/). Relevant capabilities from those docs include:

- Querying recent and successful builds
- Reading build parameters
- Fetching test results from a completed build
- Fetching console text

This skill's helper uses the Jenkins JSON and text endpoints directly with the Python standard library so it can run in lean environments without extra packages. If `jenkinsapi` is already installed and ad-hoc exploration is faster with it, use it, but do not make the skill depend on it.
