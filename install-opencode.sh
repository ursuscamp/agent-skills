#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_ROOT="$SCRIPT_DIR/agents"
SOURCE_AGENTS="$SOURCE_ROOT/agents"
SOURCE_SKILLS="$SOURCE_ROOT/skills"

TARGET_ROOT="${OPENCODE_CONFIG_DIR:-$HOME/.config/opencode}"
TARGET_AGENTS="$TARGET_ROOT/agents"
TARGET_SKILLS="$TARGET_ROOT/skills"
STATE_DIR="$TARGET_ROOT/.agent_stuff-sync"
AGENTS_STATE="$STATE_DIR/agents.txt"
SKILLS_STATE="$STATE_DIR/skills.txt"

MODE="watch"

usage() {
  cat <<'EOF'
Usage: ./install-opencode.sh [--watch|--once]

Copies this repo's OpenCode agents and skills into your global config directory.

Options:
  --watch  Sync once, then keep watching for changes (default)
  --once   Sync once and exit
  --help   Show this help text

Environment:
  OPENCODE_CONFIG_DIR  Override the default target of ~/.config/opencode
EOF
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --watch)
      MODE="watch"
      ;;
    --once)
      MODE="once"
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      printf 'Unknown argument: %s\n\n' "$1" >&2
      usage >&2
      exit 1
      ;;
  esac
  shift
done

require_source_layout() {
  if [ ! -d "$SOURCE_AGENTS" ]; then
    printf 'Missing source agents directory: %s\n' "$SOURCE_AGENTS" >&2
    exit 1
  fi

  if [ ! -d "$SOURCE_SKILLS" ]; then
    printf 'Missing source skills directory: %s\n' "$SOURCE_SKILLS" >&2
    exit 1
  fi
}

prepare_target_dirs() {
  mkdir -p "$TARGET_AGENTS" "$TARGET_SKILLS" "$STATE_DIR"
}

cleanup_removed_entries() {
  local previous_file="$1"
  local current_file="$2"
  local target_base="$3"
  local entry_type="$4"

  [ -f "$previous_file" ] || return 0

  while IFS= read -r entry; do
    [ -n "$entry" ] || continue

    if grep -Fqx "$entry" "$current_file"; then
      continue
    fi

    if [ "$entry_type" = "dir" ]; then
      rm -rf "$target_base/$entry"
    else
      rm -f "$target_base/$entry"
    fi
  done < "$previous_file"
}

sync_agents() {
  local current_file
  current_file="$(mktemp)"

  while IFS= read -r source_file; do
    local name
    name="$(basename "$source_file")"
    printf '%s\n' "$name" >> "$current_file"
    rsync -a "$source_file" "$TARGET_AGENTS/$name"
  done < <(python3 - <<'PY' "$SOURCE_AGENTS"
import pathlib
import sys

source_agents = pathlib.Path(sys.argv[1])
for path in sorted(source_agents.glob("*.md")):
    if path.is_file():
        print(path)
PY
)

  cleanup_removed_entries "$AGENTS_STATE" "$current_file" "$TARGET_AGENTS" "file"
  mv "$current_file" "$AGENTS_STATE"
}

sync_skills() {
  local current_file
  current_file="$(mktemp)"

  while IFS= read -r source_dir; do
    local name
    name="$(basename "$source_dir")"
    printf '%s\n' "$name" >> "$current_file"
    mkdir -p "$TARGET_SKILLS/$name"
    rsync -a --delete "$source_dir/" "$TARGET_SKILLS/$name/"
  done < <(python3 - <<'PY' "$SOURCE_SKILLS"
import pathlib
import sys

source_skills = pathlib.Path(sys.argv[1])
for path in sorted(source_skills.iterdir()):
    if path.is_dir() and (path / "SKILL.md").is_file():
        print(path)
PY
)

  cleanup_removed_entries "$SKILLS_STATE" "$current_file" "$TARGET_SKILLS" "dir"
  mv "$current_file" "$SKILLS_STATE"
}

sync_all() {
  sync_agents
  sync_skills
  printf '[%s] Synced to %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$TARGET_ROOT"
}

watch_with_fswatch() {
  fswatch -o "$SOURCE_AGENTS" "$SOURCE_SKILLS" | while IFS= read -r _; do
    sync_all
  done
}

watch_with_python() {
  python3 - <<'PY' "$SOURCE_AGENTS" "$SOURCE_SKILLS" | while IFS= read -r _; do
import hashlib
import os
import pathlib
import sys
import time

roots = [pathlib.Path(arg) for arg in sys.argv[1:]]

def snapshot():
    entries = []
    for root in roots:
        if not root.exists():
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = sorted(d for d in dirnames if not d.startswith('.'))
            for name in sorted(f for f in filenames if not f.startswith('.')):
                path = pathlib.Path(dirpath, name)
                stat = path.stat()
                entries.append((str(path), stat.st_mtime_ns, stat.st_size))
    return hashlib.sha256(repr(entries).encode()).hexdigest()

previous = snapshot()
while True:
    time.sleep(1)
    current = snapshot()
    if current != previous:
        previous = current
        print("changed", flush=True)
PY
    sync_all
  done
}

main() {
  require_source_layout
  prepare_target_dirs
  sync_all

  if [ "$MODE" = "once" ]; then
    exit 0
  fi

  printf 'Watching %s for changes... Press Ctrl+C to stop.\n' "$SOURCE_ROOT"

  if command -v fswatch >/dev/null 2>&1; then
    watch_with_fswatch
  else
    watch_with_python
  fi
}

main
