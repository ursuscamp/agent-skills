# Neovim Doc Workflow

Use this reference when the main skill needs a quick reminder about how the cache works or what to search.

## Cache Contract

- Default cache directory: `${NEOVIM_DOCS_DIR:-${TMPDIR:-/tmp}/neovim-docs-cache}`
- Export trigger: no cached `*.txt` help files are present, or the caller passes `--refresh`
- Export source: `nvim --headless` plus the current runtimepath reported by that Neovim instance
- Export fallback: retry with `nvim --clean --headless -i NONE` if the normal startup fails because of config or plugin side effects
- Exported support files:
  - `manifest.tsv`: cached filename to original source path
  - `runtimepath.txt`: runtimepath used during export
  - `nvim-version.txt`: Neovim version reported by headless export

## Search Patterns

- Exact function: `rg -n "nvim_buf_set_lines" "$DOCS_DIR"`
- Lua namespace: `rg -n "vim\\.api|vim\\.lsp|vim\\.diagnostic" "$DOCS_DIR"`
- Help tags: `rg -n "\\*diagnostic-defaults\\*" "$DOCS_DIR"`
- Editor behavior: `rg -n "runtimepath|packpath|shada|swapfile" "$DOCS_DIR"`
- Plugin loading: `rg -n "packages|pack-add|start|opt" "$DOCS_DIR"`

## Common Files

- `api.txt`: core API definitions
- `lua.txt`: Lua integration and idioms
- `options.txt`: editor options
- `autocmd.txt`: events and augroups
- `map.txt`: mappings
- `usr_*.txt`: higher-level user manual material
- `lsp.txt`, `diagnostic.txt`, `treesitter.txt`: feature-specific docs when available in the local runtime

## Notes

- Search the cache before browsing elsewhere when the question is about canonical Neovim behavior.
- Refresh the cache after upgrading Neovim or changing installed plugins if the exported docs may be stale.
