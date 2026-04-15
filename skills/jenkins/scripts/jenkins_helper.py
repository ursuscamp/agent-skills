#!/usr/bin/env python3
"""Small Jenkins helper for branch-aware build lookup and troubleshooting."""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urlencode, urlparse
from urllib.request import Request, urlopen


BRANCH_PARAMETER_KEYS = (
    "BRANCH_NAME",
    "BRANCH",
    "GIT_BRANCH",
    "git_branch",
    "branch",
    "CHANGE_BRANCH",
)


def fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def default_config_path() -> Path:
    config_home = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")).expanduser()
    return config_home / "jenkins-helper" / "config.json"


def load_config(path_value: Optional[str]) -> Dict[str, str]:
    config_path = Path(path_value).expanduser() if path_value else default_config_path()
    if not config_path.exists():
        return {}
    try:
        payload = json.loads(config_path.read_text())
    except OSError as exc:
        fail(f"failed to read config file {config_path}: {exc}")
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in config file {config_path}: {exc}")
    if not isinstance(payload, dict):
        fail(f"config file {config_path} must contain a JSON object")
    normalized = {}
    for key in ("url", "user", "token"):
        value = payload.get(key)
        if value is None:
            continue
        if not isinstance(value, str):
            fail(f"config file {config_path} field '{key}' must be a string")
        normalized[key] = value
    return normalized


def normalize_branch(value: str) -> str:
    branch = value.strip()
    for prefix in ("refs/remotes/origin/", "refs/heads/", "origin/", "*/"):
        if branch.startswith(prefix):
            branch = branch[len(prefix) :]
    return branch


def format_timestamp(ms: Optional[int]) -> str:
    if not ms:
        return "unknown"
    dt = datetime.fromtimestamp(ms / 1000, tz=timezone.utc).astimezone()
    return dt.isoformat(timespec="seconds")


def format_duration(ms: Optional[int]) -> str:
    if not ms:
        return "0s"
    total = int(ms / 1000)
    minutes, seconds = divmod(total, 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours}h {minutes}m {seconds}s"
    if minutes:
        return f"{minutes}m {seconds}s"
    return f"{seconds}s"


def format_elapsed_seconds(seconds: float) -> str:
    total = int(seconds)
    minutes, seconds = divmod(total, 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours}h {minutes}m {seconds}s"
    if minutes:
        return f"{minutes}m {seconds}s"
    return f"{seconds}s"


def split_job_path(job: str) -> List[str]:
    return [part for part in job.strip("/").split("/") if part]


def job_path_segments(job: str) -> List[str]:
    if job.startswith("http://") or job.startswith("https://"):
        path = urlparse(job).path.strip("/")
        parts = path.split("/")
        segments = []
        for index, part in enumerate(parts):
            if part == "job" and index + 1 < len(parts):
                segments.append(parts[index + 1])
        return segments
    return split_job_path(job)


def job_path_tail(job: str) -> Optional[str]:
    segments = job_path_segments(job)
    if not segments:
        return None
    return normalize_branch(unquote(segments[-1]))


def job_base_url(base_url: str, job: str) -> str:
    if job.startswith("http://") or job.startswith("https://"):
        return job.rstrip("/")
    parts = "/job/".join(split_job_path(job))
    return f"{base_url.rstrip('/')}/job/{parts}"


def absolute_url(base_url: str, value: str) -> str:
    if value.startswith("http://") or value.startswith("https://"):
        return value
    return f"{base_url.rstrip('/')}/{value.lstrip('/')}"


def git_output(args: Sequence[str]) -> Optional[str]:
    try:
        result = subprocess.run(
            ["git", *args],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return result.stdout.strip()


def current_branch() -> Optional[str]:
    value = git_output(["rev-parse", "--abbrev-ref", "HEAD"])
    if not value or value == "HEAD":
        return None
    return value


def current_commit() -> Optional[str]:
    return git_output(["rev-parse", "HEAD"])


@dataclass
class Client:
    base_url: str
    user: str
    token: str
    crumb: Optional[Tuple[str, str]] = None

    def auth_header(self) -> str:
        raw = f"{self.user}:{self.token}".encode("utf-8")
        return "Basic " + base64.b64encode(raw).decode("ascii")

    def request(
        self,
        url: str,
        *,
        method: str = "GET",
        params: Optional[Dict[str, str]] = None,
        data: Optional[bytes] = None,
        include_crumb: bool = False,
        accept: str = "application/json",
    ):
        if params:
            url = f"{url}?{urlencode(params)}"
        headers = {
            "Authorization": self.auth_header(),
            "Accept": accept,
        }
        if include_crumb:
            crumb = self.get_crumb()
            if crumb:
                headers[crumb[0]] = crumb[1]
        request = Request(url, data=data, method=method, headers=headers)
        try:
            return urlopen(request)
        except HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            fail(f"HTTP {exc.code} for {url}: {detail or exc.reason}")
        except URLError as exc:
            fail(f"failed to reach {url}: {exc.reason}")
        return None

    def optional_request(
        self,
        url: str,
        *,
        method: str = "GET",
        params: Optional[Dict[str, str]] = None,
        data: Optional[bytes] = None,
        accept: str = "application/json",
    ):
        if params:
            url = f"{url}?{urlencode(params)}"
        headers = {
            "Authorization": self.auth_header(),
            "Accept": accept,
        }
        request = Request(url, data=data, method=method, headers=headers)
        try:
            return urlopen(request)
        except (HTTPError, URLError):
            return None

    def get_json(self, url: str, *, params: Optional[Dict[str, str]] = None) -> Dict:
        response = self.request(url, params=params)
        return json.load(response)

    def get_text(self, url: str) -> str:
        response = self.request(url, accept="text/plain")
        return response.read().decode("utf-8", errors="replace")

    def post(self, url: str, *, data: Optional[bytes] = None):
        return self.request(url, method="POST", data=data, include_crumb=True, accept="*/*")

    def get_crumb(self) -> Optional[Tuple[str, str]]:
        if self.crumb is not None:
            return self.crumb
        crumb_url = f"{self.base_url.rstrip('/')}/crumbIssuer/api/json"
        response = self.optional_request(crumb_url)
        if response is None:
            self.crumb = None
            return None
        payload = json.load(response)
        field = payload.get("crumbRequestField")
        value = payload.get("crumb")
        self.crumb = (field, value) if field and value else None
        return self.crumb


def make_client(args: argparse.Namespace) -> Client:
    config = load_config(args.config)
    base_url = args.url or config.get("url") or os.environ.get("JENKINS_URL")
    user = args.user or config.get("user") or os.environ.get("JENKINS_USER")
    token = args.token or config.get("token") or os.environ.get("JENKINS_TOKEN")
    if not base_url:
        fail(
            "set 'url' in the Jenkins helper config file, set JENKINS_URL, or pass --url"
        )
    if not user:
        fail(
            "set 'user' in the Jenkins helper config file, set JENKINS_USER, or pass --user"
        )
    if not token:
        fail(
            "set 'token' in the Jenkins helper config file, set JENKINS_TOKEN, or pass --token"
        )
    return Client(base_url=base_url.rstrip("/"), user=user, token=token)


def extract_parameters(actions: Iterable[Dict]) -> Dict[str, str]:
    for action in actions or []:
        if not isinstance(action, dict):
            continue
        if action.get("_class") == "hudson.model.ParametersAction":
            return {
                item.get("name"): str(item.get("value"))
                for item in action.get("parameters", [])
                if item.get("name")
            }
    return {}


def extract_revision_info(actions: Iterable[Dict]) -> Tuple[Optional[str], List[str]]:
    revision = None
    branches: List[str] = []
    for action in actions or []:
        if not isinstance(action, dict):
            continue
        last_revision = action.get("lastBuiltRevision") or {}
        if isinstance(last_revision, dict):
            revision = revision or last_revision.get("SHA1")
            branch_value = last_revision.get("branch")
            if isinstance(branch_value, str):
                branches.append(normalize_branch(branch_value))
            elif isinstance(branch_value, list):
                for entry in branch_value:
                    if isinstance(entry, dict) and entry.get("name"):
                        branches.append(normalize_branch(str(entry["name"])))
                    elif isinstance(entry, str):
                        branches.append(normalize_branch(entry))
    return revision, sorted(set(branches))


def build_matches_branch(
    build: Dict,
    branch: str,
    commit: Optional[str],
) -> Tuple[bool, List[str]]:
    actions = build.get("actions", [])
    reasons: List[str] = []
    revision, revision_branches = extract_revision_info(actions)
    normalized_target = normalize_branch(branch)
    if normalized_target in revision_branches:
        reasons.append(f"revision branch={normalized_target}")
    params = extract_parameters(actions)
    for key in BRANCH_PARAMETER_KEYS:
        value = params.get(key)
        if value and normalize_branch(value) == normalized_target:
            reasons.append(f"parameter {key}={value}")
    if commit and revision and (revision.startswith(commit) or commit.startswith(revision)):
        reasons.append(f"revision sha={revision}")
    if commit:
        for item in build.get("changeSet", {}).get("items", []):
            commit_id = item.get("commitId")
            if commit_id and commit.startswith(commit_id):
                reasons.append(f"changeset commit={commit_id}")
    return bool(reasons), reasons


def fetch_builds(client: Client, job: str, limit: int) -> List[Dict]:
    url = f"{job_base_url(client.base_url, job)}/api/json"
    tree = (
        "builds[number,url,result,building,timestamp,duration,fullDisplayName,"
        "actions[_class,parameters[name,value],lastBuiltRevision[SHA1,branch]],"
        "changeSet[items[commitId]]]"
    )
    payload = client.get_json(url, params={"tree": tree})
    return payload.get("builds", [])[:limit]


def fetch_jobs(client: Client, job: Optional[str], depth: int) -> List[Dict]:
    if job:
        url = f"{job_base_url(client.base_url, job)}/api/json"
    else:
        url = f"{client.base_url}/api/json"
    tree = "jobs[name,url,_class"
    for _ in range(max(depth, 1) - 1):
        tree += ",jobs[name,url,_class"
    tree += "]" * max(depth, 1)
    payload = client.get_json(url, params={"tree": tree})
    return payload.get("jobs", [])


def print_jobs(jobs: List[Dict], prefix: str = "", recursive: bool = False) -> None:
    for job in jobs:
        name = job.get("name", "")
        path = f"{prefix}/{name}" if prefix else name
        print(f"{path}\t{job.get('_class', '')}\t{job.get('url', '')}")
        if recursive and job.get("jobs"):
            print_jobs(job["jobs"], prefix=path, recursive=True)


def branch_job_name_matches(job_name: str, branch: str) -> bool:
    return normalize_branch(unquote(job_name)) == normalize_branch(branch)


def resolve_branch_job(client: Client, job: str, branch: str) -> Optional[str]:
    if job_path_tail(job) == normalize_branch(branch):
        return job
    jobs = fetch_jobs(client, job, depth=1)
    for child in jobs:
        name = child.get("name")
        if isinstance(name, str) and branch_job_name_matches(name, branch):
            return f"{job.strip('/')}/{name}"
    return None


def fetch_build_detail(client: Client, job: str, build_number: str) -> Dict:
    url = f"{job_base_url(client.base_url, job)}/{build_number}/api/json"
    tree = (
        "fullDisplayName,url,result,building,timestamp,duration,estimatedDuration,"
        "actions[_class,parameters[name,value],causes[shortDescription],"
        "lastBuiltRevision[SHA1,branch],totalCount,failCount,skipCount],"
        "changeSet[items[msg,commitId,author[fullName],affectedPaths]]"
    )
    return client.get_json(url, params={"tree": tree})


def fetch_job_info(client: Client, job: str) -> Dict:
    url = f"{job_base_url(client.base_url, job)}/api/json"
    tree = (
        "fullName,url,_class,"
        "property[_class,parameterDefinitions[name,_class,description,"
        "defaultParameterValue[value],choices]]"
    )
    return client.get_json(url, params={"tree": tree})


def fetch_queue_item(client: Client, queue_url: str) -> Dict:
    url = absolute_url(client.base_url, queue_url.rstrip("/") + "/api/json")
    tree = "id,blocked,buildable,stuck,cancelled,why,inQueueSince,task[name,url],executable[number,url]"
    return client.get_json(url, params={"tree": tree})


def fetch_build_status(client: Client, build_url: str) -> Dict:
    url = absolute_url(client.base_url, build_url.rstrip("/") + "/api/json")
    tree = "fullDisplayName,url,number,building,result,duration,timestamp"
    return client.get_json(url, params={"tree": tree})


def fetch_test_report(client: Client, job: str, build_number: str) -> Optional[Dict]:
    url = f"{job_base_url(client.base_url, job)}/{build_number}/testReport/api/json"
    response = client.optional_request(url)
    if response is None:
        return None
    return json.load(response)


def fetch_console(client: Client, job: str, build_number: str) -> str:
    url = f"{job_base_url(client.base_url, job)}/{build_number}/consoleText"
    return client.get_text(url)


def command_branch_builds(args: argparse.Namespace) -> None:
    client = make_client(args)
    branch = args.branch or current_branch()
    if not branch:
        fail("could not infer the current git branch; pass --branch")
    commit = current_commit()
    effective_job = resolve_branch_job(client, args.job, branch) or args.job
    if effective_job != args.job:
        print(f"Resolved branch job: {effective_job}")
    builds = fetch_builds(client, effective_job, args.limit)
    matches = []
    for build in builds:
        matched, reasons = build_matches_branch(build, branch, commit)
        if not matched and effective_job != args.job:
            matched = True
            reasons = [f"branch job path={effective_job}"]
        elif not matched and job_path_tail(effective_job) == normalize_branch(branch):
            matched = True
            reasons = [f"branch job path={effective_job}"]
        if matched:
            matches.append((build, reasons))
    if not matches:
        print(f"No matching builds found for branch '{branch}' in the last {args.limit} builds.")
        return
    print(f"Builds for branch '{branch}':")
    for build, reasons in matches:
        print(
            f"- #{build.get('number')} {build.get('result') or 'RUNNING'} "
            f"{format_timestamp(build.get('timestamp'))} "
            f"{build.get('url')}"
        )
        print(f"  reasons: {', '.join(reasons)}")


def command_list_jobs(args: argparse.Namespace) -> None:
    client = make_client(args)
    jobs = fetch_jobs(client, args.job, args.depth)
    print_jobs(jobs, prefix=(args.job or "").strip("/"), recursive=args.recursive)


def command_show_params(args: argparse.Namespace) -> None:
    client = make_client(args)
    job_info = fetch_job_info(client, args.job)
    print(job_info.get("fullName") or args.job)
    definitions = []
    for prop in job_info.get("property", []):
        if not isinstance(prop, dict):
            continue
        if prop.get("_class") == "hudson.model.ParametersDefinitionProperty":
            definitions.extend(prop.get("parameterDefinitions", []))
    if not definitions:
        print("No parameters defined.")
        return
    for definition in definitions:
        name = definition.get("name", "")
        param_type = definition.get("_class", "").split(".")[-1]
        print(f"- {name} ({param_type})")
        default_value = definition.get("defaultParameterValue", {}).get("value")
        if default_value is not None:
            print(f"  default: {default_value}")
        choices = definition.get("choices")
        if choices:
            if isinstance(choices, list):
                print(f"  choices: {', '.join(str(choice) for choice in choices)}")
            else:
                print(f"  choices: {choices}")
        description = definition.get("description")
        if description:
            print(f"  description: {description}")


def command_build_summary(args: argparse.Namespace) -> None:
    client = make_client(args)
    build = fetch_build_detail(client, args.job, args.build)
    params = extract_parameters(build.get("actions", []))
    revision, branches = extract_revision_info(build.get("actions", []))
    causes = []
    for action in build.get("actions", []):
        if isinstance(action, dict):
            for cause in action.get("causes", []):
                if cause.get("shortDescription"):
                    causes.append(cause["shortDescription"])
    print(build.get("fullDisplayName", f"Build {args.build}"))
    print(f"url: {build.get('url')}")
    print(f"result: {build.get('result') or 'RUNNING'}")
    print(f"building: {build.get('building')}")
    print(f"started: {format_timestamp(build.get('timestamp'))}")
    print(f"duration: {format_duration(build.get('duration'))}")
    if revision:
        print(f"revision: {revision}")
    if branches:
        print(f"branches: {', '.join(branches)}")
    if causes:
        print(f"causes: {'; '.join(causes)}")
    if params:
        print("parameters:")
        for key in sorted(params):
            print(f"  {key}={params[key]}")

    report = fetch_test_report(client, args.job, args.build)
    if report:
        print(
            "tests: "
            f"total={report.get('totalCount', 0)} "
            f"failed={report.get('failCount', 0)} "
            f"skipped={report.get('skipCount', 0)}"
        )
        failures = []
        for suite in report.get("suites", []):
            for case in suite.get("cases", []):
                status = (case.get("status") or "").upper()
                if status in {"FAILED", "REGRESSION"}:
                    failures.append(case)
        for case in failures[: args.failed_test_limit]:
            name = ".".join(
                part for part in (case.get("className"), case.get("name")) if part
            )
            age = case.get("age")
            print(f"  failed: {name} status={case.get('status')} age={age}")
    else:
        print("tests: unavailable")

    console_text = fetch_console(client, args.job, args.build)
    lines = console_text.splitlines()
    tail = lines[-args.console_lines :] if args.console_lines > 0 else lines
    print(f"console tail ({len(tail)} lines):")
    for line in tail:
        print(line)


def command_console(args: argparse.Namespace) -> None:
    client = make_client(args)
    console_text = fetch_console(client, args.job, args.build)
    lines = console_text.splitlines()
    if args.grep:
        pattern = re.compile(args.grep)
        lines = [line for line in lines if pattern.search(line)]
    if args.tail:
        lines = lines[-args.tail :]
    for line in lines:
        print(line)


def command_trigger_build(args: argparse.Namespace) -> None:
    client = make_client(args)
    params = {}
    for item in args.param:
        if "=" not in item:
            fail(f"invalid --param value '{item}'; expected KEY=VALUE")
        key, value = item.split("=", 1)
        params[key] = value
    job_url = job_base_url(client.base_url, args.job)
    endpoint = "buildWithParameters" if params else "build"
    payload = urlencode(params).encode("utf-8") if params else None
    response = client.post(f"{job_url}/{endpoint}", data=payload)
    location = response.headers.get("Location")
    print(f"Triggered {job_url}/{endpoint}")
    if location:
        print(f"queue: {location}")
    if not args.wait:
        if params:
            for key in sorted(params):
                print(f"  {key}={params[key]}")
        return
    if not location:
        fail("Jenkins did not return a queue location; cannot wait for the build")

    deadline = time.monotonic() + args.timeout
    build_url = None
    build_number = None
    queue_started = time.monotonic()
    last_queue_update = queue_started
    while time.monotonic() < deadline:
        queue_item = fetch_queue_item(client, location)
        if queue_item.get("cancelled"):
            fail(f"queue item was cancelled: {queue_item.get('why') or 'no reason provided'}")
        executable = queue_item.get("executable") or {}
        build_url = executable.get("url")
        build_number = executable.get("number")
        if build_url and build_number is not None:
            print(f"started build: #{build_number} {build_url}")
            break
        now = time.monotonic()
        if now - last_queue_update >= args.progress_interval:
            why = queue_item.get("why") or "waiting in queue"
            print(
                "still queued: "
                f"{format_elapsed_seconds(now - queue_started)} elapsed, {why}"
            )
            last_queue_update = now
        time.sleep(args.poll_interval)
    else:
        fail(f"timed out after {args.timeout}s waiting for Jenkins to start the build")

    build_started = time.monotonic()
    last_build_update = build_started
    while time.monotonic() < deadline:
        build = fetch_build_status(client, build_url)
        if not build.get("building"):
            result = build.get("result") or "UNKNOWN"
            print(
                f"completed build: #{build.get('number')} {result} "
                f"{format_timestamp(build.get('timestamp'))} {build.get('url')}"
            )
            if result != "SUCCESS":
                raise SystemExit(1)
            return
        now = time.monotonic()
        if now - last_build_update >= args.progress_interval:
            print(
                "still building: "
                f"#{build.get('number')} {format_elapsed_seconds(now - build_started)} elapsed"
            )
            last_build_update = now
        time.sleep(args.poll_interval)
    fail(f"timed out after {args.timeout}s waiting for Jenkins to finish the build")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        help=(
            "Path to Jenkins helper JSON config file, "
            f"default: {default_config_path()}"
        ),
    )
    parser.add_argument("--url", help="Base Jenkins URL, default: $JENKINS_URL")
    parser.add_argument("--user", help="Jenkins username, default: $JENKINS_USER")
    parser.add_argument("--token", help="Jenkins API token, default: $JENKINS_TOKEN")
    subparsers = parser.add_subparsers(dest="command", required=True)

    branch = subparsers.add_parser("branch-builds", help="Find builds for a branch")
    branch.add_argument("--job", required=True, help="Job path like folder/repo or full job URL")
    branch.add_argument("--branch", help="Branch name, default: current git branch")
    branch.add_argument("--limit", type=int, default=25, help="Number of recent builds to inspect")
    branch.set_defaults(func=command_branch_builds)

    jobs = subparsers.add_parser("list-jobs", help="List jobs under Jenkins root or a parent job")
    jobs.add_argument(
        "--job",
        help="Parent job path like Github-Purple/pmpaware-webapp; omit to list the Jenkins root",
    )
    jobs.add_argument(
        "--depth",
        type=int,
        default=1,
        help="How many job nesting levels to request from Jenkins",
    )
    jobs.add_argument(
        "--recursive",
        action="store_true",
        help="Recursively print nested jobs returned by Jenkins",
    )
    jobs.set_defaults(func=command_list_jobs)

    show_params = subparsers.add_parser("show-params", help="Show Jenkins parameter definitions for a job")
    show_params.add_argument("--job", required=True, help="Job path like folder/repo or full job URL")
    show_params.set_defaults(func=command_show_params)

    summary = subparsers.add_parser("build-summary", help="Show build, test, and console summary")
    summary.add_argument("--job", required=True, help="Job path like folder/repo or full job URL")
    summary.add_argument("--build", required=True, help="Build number")
    summary.add_argument("--console-lines", type=int, default=80, help="Console tail size")
    summary.add_argument("--failed-test-limit", type=int, default=10, help="Max failing tests to print")
    summary.set_defaults(func=command_build_summary)

    console = subparsers.add_parser("console", help="Print or filter console output")
    console.add_argument("--job", required=True, help="Job path like folder/repo or full job URL")
    console.add_argument("--build", required=True, help="Build number")
    console.add_argument("--tail", type=int, default=0, help="Print only the last N lines")
    console.add_argument("--grep", help="Regex filter applied to console lines")
    console.set_defaults(func=command_console)

    trigger = subparsers.add_parser("trigger-build", help="Trigger a Jenkins build")
    trigger.add_argument("--job", required=True, help="Job path like folder/repo or full job URL")
    trigger.add_argument(
        "--param",
        action="append",
        default=[],
        help="Build parameter in KEY=VALUE form; may be repeated",
    )
    trigger.add_argument(
        "--wait",
        action="store_true",
        help="Wait for Jenkins to start and finish the triggered build",
    )
    trigger.add_argument(
        "--poll-interval",
        type=int,
        default=5,
        help="Polling interval in seconds used with --wait",
    )
    trigger.add_argument(
        "--timeout",
        type=int,
        default=1800,
        help="Maximum seconds to wait for the build when --wait is used",
    )
    trigger.add_argument(
        "--progress-interval",
        type=int,
        default=30,
        help="Seconds between heartbeat updates while waiting",
    )
    trigger.set_defaults(func=command_trigger_build)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
