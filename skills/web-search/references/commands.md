# Exa MCP via mcporter: Command Reference

Re-check `npx -y mcporter --help` when exact flags matter.

## Inspect tools on the hosted server

```bash
npx -y mcporter list https://mcp.exa.ai/mcp --schema
```

## Web search

```bash
npx -y mcporter call \
  'https://mcp.exa.ai/mcp.web_search_exa(query: "latest changes in bun test runner", numResults: 3)'
```

## Web fetch

```bash
npx -y mcporter call \
  'https://mcp.exa.ai/mcp.web_fetch_exa(urls: ["https://bun.com/blog/bun-v1.3.13"], maxCharacters: 5000)'
```

## Structured output

```bash
npx -y mcporter call \
  'https://mcp.exa.ai/mcp.web_search_exa(query: "category:people staff machine learning engineer exa", numResults: 5)' \
  --output json
```

## Useful call flags

- `--output json` for machine-readable output
- `--timeout <ms>` to override call timeout
- `--save-images <dir>` when content blocks include images
- `--raw-strings` or `--no-coerce` when argument coercion causes issues
