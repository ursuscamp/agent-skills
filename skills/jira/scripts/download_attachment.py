#!/usr/bin/env python3

"""
Download a Jira attachment by using `jira issue view --raw` to discover metadata.

This script is intentionally auth-agnostic for the final download request because the
attachment content URL may require headers or cookies that are specific to the Jira setup.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import pathlib
import re
import subprocess
import sys
import urllib.error
import urllib.request
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download a Jira attachment by issue key and attachment name or id.",
    )
    parser.add_argument("issue_key", help="Jira issue key, for example ENG-123")
    parser.add_argument(
        "--attachment-name",
        help="Attachment filename to download. Exact match is preferred; case-insensitive fallback is supported.",
    )
    parser.add_argument(
        "--attachment-id",
        help="Attachment id to download.",
    )
    parser.add_argument(
        "--output",
        help="Exact output file path. Defaults to OUTPUT_DIR/<attachment filename>.",
    )
    parser.add_argument(
        "--output-dir",
        default=".",
        help="Directory for downloaded files when --output is not set.",
    )
    parser.add_argument(
        "--project",
        help="Optional Jira project key passed through to `jira -p`.",
    )
    parser.add_argument(
        "--header",
        action="append",
        default=[],
        help="Additional HTTP header for the attachment download, repeatable. Example: Authorization: Bearer ...",
    )
    parser.add_argument(
        "--basic-user",
        help="Username or email for HTTP basic auth.",
    )
    parser.add_argument(
        "--basic-token",
        help="Password or API token for HTTP basic auth.",
    )
    parser.add_argument(
        "--cookie",
        action="append",
        default=[],
        help="Cookie header value, repeatable. Example: atlassian.xsrf.token=...",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=120,
        help="Download timeout in seconds.",
    )
    parser.add_argument(
        "--metadata-file",
        help="Use an existing raw issue JSON file instead of calling `jira issue view --raw`.",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List discovered attachments and exit without downloading.",
    )
    parser.add_argument(
        "--config-file",
        help="Optional path to the jira CLI config file. Defaults to JIRA_CONFIG_FILE or ~/.config/.jira/.config.yml.",
    )
    return parser.parse_args()


def run_jira_issue_view(issue_key: str, project: str | None) -> dict[str, Any]:
    command = ["jira"]
    if project:
        command.extend(["-p", project])
    command.extend(["issue", "view", issue_key, "--raw"])

    try:
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as exc:
        raise SystemExit("Could not find `jira` on PATH.") from exc
    except subprocess.CalledProcessError as exc:
        stderr = exc.stderr.strip()
        stdout = exc.stdout.strip()
        message = stderr or stdout or str(exc)
        raise SystemExit(f"`{' '.join(command)}` failed: {message}") from exc

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise SystemExit("`jira issue view --raw` did not return valid JSON.") from exc


def load_metadata(args: argparse.Namespace) -> dict[str, Any]:
    if args.metadata_file:
        with open(args.metadata_file, "r", encoding="utf-8") as handle:
            return json.load(handle)
    return run_jira_issue_view(args.issue_key, args.project)


def looks_like_attachment(entry: Any) -> bool:
    return (
        isinstance(entry, dict)
        and isinstance(entry.get("filename"), str)
        and isinstance(entry.get("id"), (str, int))
        and isinstance(entry.get("content"), str)
    )


def find_attachment_lists(value: Any) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            attachment_field = node.get("attachment")
            if isinstance(attachment_field, list):
                for item in attachment_field:
                    if looks_like_attachment(item):
                        found.append(item)
            for child in node.values():
                walk(child)
        elif isinstance(node, list):
            for child in node:
                walk(child)

    walk(value)

    deduped: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for item in found:
        key = (str(item.get("id")), item.get("filename", ""))
        if key in seen:
            continue
        seen.add(key)
        deduped.append(item)
    return deduped


def choose_attachment(
    attachments: list[dict[str, Any]],
    attachment_id: str | None,
    attachment_name: str | None,
) -> dict[str, Any]:
    if not attachments:
        raise SystemExit("No attachments were found in the raw Jira issue response.")

    if attachment_id:
        for item in attachments:
            if str(item.get("id")) == attachment_id:
                return item
        raise SystemExit(f"No attachment matched id {attachment_id!r}.")

    if attachment_name:
        exact_matches = [
            item for item in attachments if item.get("filename") == attachment_name
        ]
        if len(exact_matches) == 1:
            return exact_matches[0]
        if len(exact_matches) > 1:
            raise SystemExit(
                f"Multiple attachments matched filename {attachment_name!r}; use --attachment-id."
            )

        folded_name = attachment_name.casefold()
        folded_matches = [
            item
            for item in attachments
            if str(item.get("filename", "")).casefold() == folded_name
        ]
        if len(folded_matches) == 1:
            return folded_matches[0]
        if len(folded_matches) > 1:
            raise SystemExit(
                f"Multiple attachments matched filename {attachment_name!r}; use --attachment-id."
            )
        raise SystemExit(f"No attachment matched filename {attachment_name!r}.")

    if len(attachments) == 1:
        return attachments[0]

    names = ", ".join(f"{item['filename']} ({item['id']})" for item in attachments)
    raise SystemExit(
        "Issue has multiple attachments; choose one with --attachment-name or --attachment-id. "
        f"Available: {names}"
    )


def sanitize_filename(name: str) -> str:
    sanitized = re.sub(r"[\\/]+", "_", name).strip()
    return sanitized or "attachment.bin"


def default_config_path(args: argparse.Namespace) -> pathlib.Path:
    if args.config_file:
        return pathlib.Path(args.config_file).expanduser()
    env_path = pathlib.Path(
        os.environ.get(
            "JIRA_CONFIG_FILE",
            "~/.config/.jira/.config.yml",
        )
    ).expanduser()
    return env_path


def read_simple_config(path: pathlib.Path) -> dict[str, str]:
    if not path.exists():
        return {}

    values: dict[str, str] = {}
    with open(path, "r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.rstrip("\n")
            if not line or line.startswith((" ", "\t")):
                continue
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            values[key.strip()] = value.strip()
    return values


def maybe_add_auto_auth(
    headers: list[tuple[str, str]], args: argparse.Namespace
) -> list[tuple[str, str]]:
    if headers:
        return headers

    environ = os.environ
    bearer = environ.get("JIRA_BEARER_TOKEN")
    if bearer:
        return [("Authorization", f"Bearer {bearer}")]

    config = read_simple_config(default_config_path(args))
    auth_type = config.get("auth_type", "").strip().lower()
    login = config.get("login", "").strip()
    token = environ.get("JIRA_API_TOKEN")
    if auth_type == "basic" and login and token:
        encoded = base64.b64encode(f"{login}:{token}".encode("utf-8")).decode("ascii")
        return [("Authorization", f"Basic {encoded}")]

    return headers


def build_headers(args: argparse.Namespace) -> list[tuple[str, str]]:
    headers: list[tuple[str, str]] = []

    for value in args.header:
        if ":" not in value:
            raise SystemExit(f"Invalid --header value {value!r}; expected NAME: VALUE.")
        name, raw_value = value.split(":", 1)
        headers.append((name.strip(), raw_value.strip()))

    if args.basic_user or args.basic_token:
        if not (args.basic_user and args.basic_token):
            raise SystemExit("Pass both --basic-user and --basic-token for basic auth.")
        token = base64.b64encode(
            f"{args.basic_user}:{args.basic_token}".encode("utf-8")
        ).decode("ascii")
        headers.append(("Authorization", f"Basic {token}"))

    if args.cookie:
        headers.append(("Cookie", "; ".join(args.cookie)))

    return maybe_add_auto_auth(headers, args)


def resolve_output_path(args: argparse.Namespace, attachment: dict[str, Any]) -> pathlib.Path:
    if args.output:
        path = pathlib.Path(args.output)
        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    output_dir = pathlib.Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = sanitize_filename(str(attachment.get("filename", "attachment.bin")))
    return output_dir / filename


def download(url: str, headers: list[tuple[str, str]], destination: pathlib.Path, timeout: int) -> None:
    request = urllib.request.Request(url)
    for name, value in headers:
        request.add_header(name, value)

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response, open(
            destination, "wb"
        ) as handle:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                handle.write(chunk)
    except urllib.error.HTTPError as exc:
        destination.unlink(missing_ok=True)
        raise SystemExit(
            f"Attachment download failed with HTTP {exc.code}. "
            "Pass auth headers, basic auth, or cookies if your Jira attachment URLs require them."
        ) from exc
    except urllib.error.URLError as exc:
        destination.unlink(missing_ok=True)
        raise SystemExit(f"Attachment download failed: {exc.reason}") from exc


def print_attachments(attachments: list[dict[str, Any]]) -> None:
    for item in attachments:
        attachment_id = item.get("id", "")
        filename = item.get("filename", "")
        size = item.get("size", "")
        content = item.get("content", "")
        print(f"{attachment_id}\t{filename}\t{size}\t{content}")


def main() -> int:
    args = parse_args()
    metadata = load_metadata(args)
    attachments = find_attachment_lists(metadata)

    if args.list:
        if not attachments:
            print("No attachments found.", file=sys.stderr)
            return 1
        print_attachments(attachments)
        return 0

    attachment = choose_attachment(
        attachments,
        attachment_id=args.attachment_id,
        attachment_name=args.attachment_name,
    )
    destination = resolve_output_path(args, attachment)
    headers = build_headers(args)
    url = str(attachment.get("content"))

    if not url:
        raise SystemExit("Selected attachment does not include a content URL.")

    download(url, headers, destination, args.timeout)
    print(destination.resolve())
    return 0


if __name__ == "__main__":
    sys.exit(main())
