# AGENTS.md

- Treat `skills/<skill-name>/SKILL.md` as the canonical entrypoint for every skill.
- Consider a folder under `skills/` installable only if it contains `SKILL.md`.
- Keep skill-specific content inside `skills/<skill-name>/`.
- Keep repo skill folders minimal. Do not add `agents/openai.yaml` unless the user explicitly asks for it.
- Update `README.md` only when visible repo behavior or the documented skill list changes.
- Validate typical skill changes with `./install-skills --once`.
- Preserve `install-skills` sync behavior, including pruning removed skills from the target directory.
