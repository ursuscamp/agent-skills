# Playwright CLI Command Patterns

This reference reflects the current `@playwright/cli` docs and package contents reviewed on April 2, 2026. Re-check `playwright-cli --help` when exact flags matter because the CLI is still evolving quickly.

## Install and discover

```bash
npm install -g @playwright/cli@latest
playwright-cli --help
playwright-cli open --help
playwright-cli install --skills
```

If global install is undesirable, run commands with `npx playwright-cli ...`.

## Core page interaction

```bash
playwright-cli open [url]
playwright-cli goto <url>
playwright-cli click <ref-or-selector> [button]
playwright-cli dblclick <ref-or-selector> [button]
playwright-cli type <text>
playwright-cli fill <ref-or-selector> <text>
playwright-cli fill <ref-or-selector> <text> --submit
playwright-cli select <ref-or-selector> <value>
playwright-cli check <ref-or-selector>
playwright-cli uncheck <ref-or-selector>
playwright-cli hover <ref-or-selector>
playwright-cli drag <start-ref> <end-ref>
playwright-cli upload <file>
playwright-cli close
```

## Snapshots and captures

```bash
playwright-cli snapshot
playwright-cli snapshot <ref-or-selector>
playwright-cli snapshot --filename=state.yaml
playwright-cli snapshot --depth=4
playwright-cli screenshot
playwright-cli screenshot <ref-or-selector>
playwright-cli screenshot --filename=page.png
playwright-cli pdf
playwright-cli pdf --filename=page.pdf
```

Use snapshots more often than screenshots. Snapshots are lighter, expose element refs, and make follow-up commands easier.

## Navigation, keyboard, and mouse

```bash
playwright-cli go-back
playwright-cli go-forward
playwright-cli reload
playwright-cli press <key>
playwright-cli keydown <key>
playwright-cli keyup <key>
playwright-cli mousemove <x> <y>
playwright-cli mousedown [button]
playwright-cli mouseup [button]
playwright-cli mousewheel <dx> <dy>
```

## Tabs

```bash
playwright-cli tab-list
playwright-cli tab-new [url]
playwright-cli tab-select <index>
playwright-cli tab-close [index]
```

## Inspection and advanced control

```bash
playwright-cli eval <expression-or-function> [ref-or-selector]
playwright-cli run-code <code>
playwright-cli run-code --filename=script.js
playwright-cli console [min-level]
playwright-cli network
playwright-cli dialog-accept [prompt]
playwright-cli dialog-dismiss
playwright-cli resize <width> <height>
```

Use `eval` for small inspections of page or element state. Use `run-code` for full Playwright snippets.

## Network mocking

```bash
playwright-cli route <pattern> [options]
playwright-cli route-list
playwright-cli unroute [pattern]
```

Simple examples:

```bash
playwright-cli route "**/*.jpg" --status=404
playwright-cli route "**/api/users" --body='[{"id":1}]' --content-type=application/json
playwright-cli unroute
```
