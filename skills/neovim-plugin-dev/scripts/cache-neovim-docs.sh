#!/usr/bin/env bash
set -euo pipefail

CACHE_DIR="${NEOVIM_DOCS_DIR:-${TMPDIR:-/tmp}/codex-neovim-docs}"
REFRESH=0
PRINT_DIR=0

usage() {
  cat <<'EOF'
Usage: cache-neovim-docs.sh [--refresh] [--print-dir]

Export Neovim help docs into a local cache directory if the cache is missing.

Options:
  --refresh    Rebuild the cache even if docs already exist
  --print-dir  Print the cache directory after ensuring it exists
  --help       Show this help text
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --refresh)
      REFRESH=1
      shift
      ;;
    --print-dir)
      PRINT_DIR=1
      shift
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

mkdir -p "$CACHE_DIR"

needs_export=0
if [[ "$REFRESH" -eq 1 ]]; then
  needs_export=1
elif ! find "$CACHE_DIR" -maxdepth 1 -type f -name '*.txt' -print -quit | grep -q .; then
  needs_export=1
fi

if [[ "$needs_export" -eq 1 ]]; then
  if ! command -v nvim >/dev/null 2>&1; then
    echo "nvim is required to export help docs" >&2
    exit 1
  fi

  find "$CACHE_DIR" -maxdepth 1 -type f \
    \( -name '*.txt' -o -name 'manifest.tsv' -o -name 'runtimepath.txt' -o -name 'nvim-version.txt' \) \
    -exec rm -f {} +

  export NVIM_DOCS_CACHE_DIR="$CACHE_DIR"

  export_lua='lua
local cache_dir = assert(vim.env.NVIM_DOCS_CACHE_DIR, "NVIM_DOCS_CACHE_DIR is required")
vim.fn.mkdir(cache_dir, "p")

local docs = vim.api.nvim_get_runtime_file("doc/*.txt", true)
table.sort(docs)

local manifest = {}
for index, source in ipairs(docs) do
  local basename = vim.fn.fnamemodify(source, ":t")
  local target = string.format("%s/%04d-%s", cache_dir, index, basename)
  vim.fn.writefile(vim.fn.readfile(source), target)
  table.insert(manifest, string.format("%s\t%s", vim.fn.fnamemodify(target, ":t"), source))
end

vim.fn.writefile(manifest, cache_dir .. "/manifest.tsv")
vim.fn.writefile(vim.split(vim.o.runtimepath, ","), cache_dir .. "/runtimepath.txt")
vim.fn.writefile(vim.split(vim.fn.execute("version"), "\n"), cache_dir .. "/nvim-version.txt")
'

  export_log="$(mktemp)"
  if ! nvim --headless -i NONE +"$export_lua" +qa >"$export_log" 2>&1; then
    if ! nvim --clean --headless -i NONE +"$export_lua" +qa >"$export_log" 2>&1; then
      cat "$export_log" >&2
      rm -f "$export_log"
      exit 1
    fi
  fi
  rm -f "$export_log"
fi

if [[ "$PRINT_DIR" -eq 1 ]]; then
  printf '%s\n' "$CACHE_DIR"
fi
