---
name: dynamic-agent-context
description: Install and refresh dynamic learned context in any repo (.agent-context, AGENTS.md, learned-conventions.mdc). Use for coding, architecture code design, tests, refactors, code review, and bug fixes.
---

# Dynamic Agent Context

Extract executable, project-local engineering conventions from real code and load them on-demand for code-related tasks.

## Outputs (generated at repo root)

- `.agent-context/conventions.md`: full conventions profile (stats + actionable guidance)
- `.agent-context/project-context.md`: project profile (layout + signals)
- `.agent-context/metadata.json`: machine-readable metrics
- `.cursor/rules/learned-conventions.mdc`: concise Cursor rule loaded on-demand
- `AGENTS.md` / `CLAUDE.md`: cross-editor entrypoints

## Install (one-time)

Run from the target repo root:

```bash
mkdir -p scripts
# If you cloned this repository to ~/.cursor/skills:
cp ~/.cursor/skills/en/skills/dynamic-agent-context/scripts/generate_agent_context.py scripts/
cp ~/.cursor/skills/en/skills/dynamic-agent-context/scripts/refresh_agent_context.py scripts/
cp ~/.cursor/skills/en/skills/dynamic-agent-context/scripts/sync_agent_entrypoints.py scripts/
python scripts/refresh_agent_context.py --full
```

## Refresh

- Incremental: `python scripts/refresh_agent_context.py --changed-only`
- Full: `python scripts/refresh_agent_context.py --full`

## How AI uses it

- Cursor: auto-injects `.cursor/rules/learned-conventions.mdc` for code-related tasks
- Other editors: read `AGENTS.md` / `CLAUDE.md`, then `.agent-context/*`

