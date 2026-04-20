---
name: dynamic-agent-context
description: Install and refresh dynamic learned context in any repo (.agent-context, AGENTS.md, learned-conventions.mdc). Use for coding, architecture code design, tests, refactors, code review, and bug fixes.
---

# Dynamic Agent Context — Install & Use

Automatically extract executable, project-local conventions from real code and load them on-demand for code-related tasks.

## When to use

- Enabling AI coding conventions on a new project
- Turning "verbal team conventions" into "auto-learned rules" on a legacy project
- Code style is drifting and AI output needs to be unified

## Standard operation

### 1) Deploy scripts into your project

```bash
mkdir -p scripts
# If you cloned this skills repo to ~/.cursor/skills:
cp ~/.cursor/skills/dynamic-agent-context/scripts/generate_agent_context.py scripts/
cp ~/.cursor/skills/dynamic-agent-context/scripts/refresh_agent_context.py scripts/
cp ~/.cursor/skills/dynamic-agent-context/scripts/sync_agent_entrypoints.py scripts/
```

### 2) First generation

```bash
python scripts/refresh_agent_context.py --full
```

### 3) Verify output

```bash
test -f .agent-context/conventions.md
test -f .agent-context/project-context.md
test -f .agent-context/metadata.json
test -f AGENTS.md
test -f CLAUDE.md
test -f .cursor/rules/learned-conventions.mdc
```

## AI loading paths

- Cursor: `.cursor/rules/learned-conventions.mdc` (`alwaysApply: false`, auto-loaded for code-related tasks)
- Claude Code / OpenCode / Codex: enter via `AGENTS.md` / `CLAUDE.md` → `.agent-context/*`

## Refresh strategy

- Full: `python scripts/refresh_agent_context.py --full`
- Incremental: `python scripts/refresh_agent_context.py --changed-only`

## Notes

- `.agent-context/*` are machine-generated; manual edits get overwritten on refresh (except the `Maintainer Notes` section)
- `learned-conventions.mdc` is auto-generated; do not hand-edit
