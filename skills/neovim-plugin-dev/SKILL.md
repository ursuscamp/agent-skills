---
name: neovim-plugin-dev
description: Expert help for Neovim usage, debugging, and plugin development. Use when building, reviewing, fixing, or explaining Neovim configuration, Lua or Vimscript plugins, runtimepath behavior, user commands, keymaps, autocmds, LSP integrations, remote plugins, help topics, or Neovim API usage. Consult cached Neovim help docs before answering doc-sensitive questions.
---

# Neovim Plugin Development

Use this skill to ground Neovim answers in the local `:help` docs instead of memory alone.

## Quick Start

1. Ensure the doc cache exists before answering questions that depend on exact Neovim behavior, command syntax, option semantics, runtime layout, or public APIs.
2. Search the cached docs first with `rg`.
3. Read the matching help files with `sed` or `rg -n -C`.
4. Inspect the target project after the docs confirm the API or behavior you plan to use.

## Doc Cache Workflow

Use [`scripts/cache-neovim-docs.sh`](scripts/cache-neovim-docs.sh) to manage the help cache.

- Cache root: `${NEOVIM_DOCS_DIR:-${TMPDIR:-/tmp}/neovim-docs-cache}`
- Default behavior: if the cache is missing or has no exported help files, run Neovim in headless mode and export the current runtime docs into the cache directory
- Fallback behavior: if the normal headless startup fails because of local config side effects, retry with a clean headless Neovim session
- Refresh behavior: pass `--refresh` when the local Neovim install, runtimepath, or plugin set may have changed
- Print behavior: pass `--print-dir` to get the active cache directory

Typical flow:

```bash
DOCS_DIR="$("$(pwd)/skills/neovim-plugin-dev/scripts/cache-neovim-docs.sh" --print-dir)"
rg -n "nvim_create_user_command|vim.api.nvim_create_user_command" "$DOCS_DIR"
sed -n '1,220p' "$DOCS_DIR"/0010-api.txt
```

If the repository root is not the current directory, use the absolute path to the script instead.

## Search Strategy

Start with focused searches, then widen only if needed.

- APIs and Lua entry points: search for `vim.api`, `vim.fn`, `vim.loop`, `lua-guide`, or exact function names
- Editor behavior: search for option names, Ex commands, events, keymap topics, or `:help` tags such as `autocmd`, `map.txt`, `options`, `api.txt`, `lua.txt`, `diagnostic.txt`, `lsp.txt`
- Plugin loading and packaging: search for `runtimepath`, `packages`, `pack-add`, `rplugin`, `health`, `provider`
- Treesitter or LSP work: search for `treesitter`, `vim.lsp`, `diagnostic`, `client`, `buf_attach_client`

Useful commands:

```bash
DOCS_DIR="$("$(pwd)/skills/neovim-plugin-dev/scripts/cache-neovim-docs.sh" --print-dir)"
rg -n "runtimepath|packpath|packages" "$DOCS_DIR"
rg -n "autocmd|nvim_create_autocmd" "$DOCS_DIR"
rg -n "vim\.lsp|diagnostic" "$DOCS_DIR"
rg -n "^.\{-}\\*nvim_create_user_command\\*" "$DOCS_DIR"
```

## Working Style

- Prefer documented public APIs over internal behavior.
- Check the docs before claiming an option, function, event, or command exists.
- When a help topic is ambiguous, read both the API reference and the surrounding conceptual guide.
- When editing plugins, combine doc findings with direct inspection of the plugin code, tests, and runtime files.
- When the task depends on installed plugins, remember that the exported docs reflect the local Neovim runtime available to headless `nvim`.

## References

- Doc lookup notes: [`references/doc-workflow.md`](references/doc-workflow.md)
