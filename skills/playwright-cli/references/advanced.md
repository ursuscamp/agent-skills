# Playwright CLI Advanced Usage

## Sessions

Use named sessions to isolate cookies, storage, tabs, and history:

```bash
playwright-cli -s=auth open https://app.example.com/login --persistent
playwright-cli -s=docs open https://playwright.dev
playwright-cli list
playwright-cli -s=auth close
playwright-cli close-all
playwright-cli kill-all
playwright-cli -s=auth delete-data
```

You can also set `PLAYWRIGHT_CLI_SESSION=<name>` to bind a shell or agent run to one session by default.

## Storage State

```bash
playwright-cli state-save auth.json
playwright-cli state-load auth.json
playwright-cli cookie-list --domain=example.com
playwright-cli cookie-get session_id
playwright-cli cookie-set theme dark
playwright-cli cookie-delete theme
playwright-cli localstorage-list
playwright-cli localstorage-get token
playwright-cli localstorage-set token abc123
playwright-cli localstorage-delete token
playwright-cli localstorage-clear
```

Prefer full `state-save` and `state-load` when moving auth state between runs. Use individual cookie or storage commands for precise inspection and small edits.

## Tracing and Video

```bash
playwright-cli tracing-start
playwright-cli tracing-stop
playwright-cli video-start demo.webm
playwright-cli video-chapter "Login flow" --description="Signing in" --duration=2000
playwright-cli video-stop
```

Use traces for debugging and replay. Use video for demonstrations or proof of work.

## Generating or debugging Playwright tests

- Interactive CLI actions can emit Playwright TypeScript snippets.
- Use those generated actions as a starting point, then move them into a real test file and add assertions yourself.
- When running `@playwright/test`, prefer `PLAYWRIGHT_HTML_OPEN=never npx playwright test ...` to avoid surprising report windows.
- If the project uses CLI debugging support such as `npx playwright test --debug=cli`, keep the test running in the background, then attach or inspect with `playwright-cli` commands as appropriate for that project setup.

## When to use `run-code`

Reach for `playwright-cli run-code` when you need capabilities not covered by the small CLI verbs:

- geolocation or permission changes
- custom waits
- frame or download handling
- complex conditional request mocking
- richer video overlays or screencast APIs

Keep snippets short, task-specific, and easy to explain back to the user.
