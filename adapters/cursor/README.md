# Cursor IDE Adapter

Cursor reads `.cursor/rules/*.mdc` natively. Link the workflow rules into each project that should use this workflow.

## Chinese Rules

```bash
mkdir -p .cursor/rules
ln -s <path-to-agentic-coding-workflow>/zh/rules/matt-skills-core.mdc .cursor/rules/
ln -s <path-to-agentic-coding-workflow>/zh/rules/ai-coding-protocol.mdc .cursor/rules/
ln -s <path-to-agentic-coding-workflow>/zh/rules/design-thinking-tools.mdc .cursor/rules/
ln -s <path-to-agentic-coding-workflow>/zh/rules/agent-continuity-protocol.mdc .cursor/rules/
```

## English Rules

```bash
mkdir -p .cursor/rules
ln -s <path-to-agentic-coding-workflow>/en/rules/matt-skills-core.mdc .cursor/rules/
ln -s <path-to-agentic-coding-workflow>/en/rules/ai-coding-protocol.mdc .cursor/rules/
ln -s <path-to-agentic-coding-workflow>/en/rules/design-thinking-tools.mdc .cursor/rules/
ln -s <path-to-agentic-coding-workflow>/en/rules/agent-continuity-protocol.mdc .cursor/rules/
```

## Skills

Point your agent or local conventions at `<path-to-agentic-coding-workflow>/zh/skills` or `<path-to-agentic-coding-workflow>/en/skills`. The rules route to skills by name, for example `diagnose`, `tdd`, `to-prd`, and `safe-commit`.
