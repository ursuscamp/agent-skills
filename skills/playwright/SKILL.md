---
name: playwright
description: Use when browser automation with Playwright is needed, especially through the Playwright coding-agent CLI, including opening pages, navigating, inspecting snapshots, targeting elements by ref or selector, capturing screenshots or PDFs, managing named browser sessions, inspecting storage or network state, recording traces or video, mocking requests, or generating Playwright test code from interactive browser work.
---

# Playwright

Use this skill to drive the browser through `playwright-cli` instead of guessing at browser behavior or writing ad hoc Playwright scripts first.

Start by checking the exact CLI surface in the current environment:

```bash
command -v playwright-cli
playwright-cli --help
playwright-cli open --help
```

If the CLI is missing, either install it globally with `npm install -g @playwright/cli@latest` or run it through `npx playwright-cli ...`.

## Quick Start

1. Open a browser session with `playwright-cli open [url]`.
2. Read the snapshot emitted after each command, or request one explicitly with `playwright-cli snapshot`.
3. Prefer element refs from snapshots such as `e15` for follow-up actions.
4. Use `playwright-cli eval ...` or `playwright-cli run-code ...` only when the built-in commands are not enough.
5. Close or clean up sessions when finished.

## Working Style

- Prefer `playwright-cli` over hand-written browser scripts for direct interactive browsing tasks.
- Prefer snapshot refs over brittle CSS selectors whenever the snapshot already exposes the element you need.
- Take a fresh snapshot after navigation, modal changes, or any action that may have changed the DOM.
- Prefer named sessions with `-s=<name>` when working on multiple sites, auth states, or concurrent flows.
- Use `--persistent` only when the task benefits from keeping browser state on disk across restarts.
- Capture screenshots, PDFs, traces, or video only when they help the user verify results or debug failures.
- Keep the CLI honest by checking `playwright-cli --help` for less common commands before relying on memory.

## Common Workflows

### Explore and interact with a page

```bash
playwright-cli open https://example.com
playwright-cli snapshot
playwright-cli click e15
playwright-cli fill e22 "hello world"
playwright-cli press Enter
```

### Use safer targeting

- Prefer refs like `e15` from snapshots.
- Use CSS selectors only when no stable ref is available.
- Use Playwright locator strings when they are clearer or more resilient than CSS.
- When the snapshot omits important attributes such as `id`, `class`, or `data-testid`, inspect them with `playwright-cli eval`.

Examples:

```bash
playwright-cli click e15
playwright-cli click "#main > button.submit"
playwright-cli click "getByRole('button', { name: 'Submit' })"
playwright-cli eval "el => el.getAttribute('data-testid')" e15
```

### Manage sessions deliberately

Use separate named sessions for different users, environments, or workstreams:

```bash
playwright-cli -s=admin open https://app.example.com --persistent
playwright-cli -s=guest open https://app.example.com
playwright-cli list
```

Use `playwright-cli close`, `playwright-cli close-all`, `playwright-cli kill-all`, and `playwright-cli delete-data` for cleanup.

### Debug, inspect, and capture evidence

- Use `playwright-cli screenshot` for a quick visual capture.
- Use `playwright-cli pdf` for printable page output.
- Use `playwright-cli tracing-start` and `playwright-cli tracing-stop` when you need replayable debugging artifacts.
- Use `playwright-cli console` and `playwright-cli network` to inspect runtime signals before changing app code.

### Escalate to custom code only when needed

Use `playwright-cli run-code` for advanced scenarios such as geolocation, permission changes, complex request mocking, downloads, or custom video overlays. Keep snippets focused and prefer built-in commands first.

### Convert exploration into tests

The CLI can emit Playwright TypeScript actions as you interact. Use the interactive flow to discover resilient locators, then copy the generated actions into a real `@playwright/test` test and add assertions manually.

## References

- Command patterns and command groups: [`references/commands.md`](references/commands.md)
- Session, storage, tracing, and advanced usage notes: [`references/advanced.md`](references/advanced.md)
