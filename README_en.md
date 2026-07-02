# Agentic Coding Workflow

<p align="center">
  <img src="https://img.shields.io/badge/Agentic-Workflow-blue.svg" alt="Agentic Workflow">
  <img src="https://img.shields.io/badge/AI_Pair_Programming-Cursor_|_Claude-lightgrey.svg" alt="AI Pair Programming">
</p>

<p align="center">
  <b>English</b> | <a href="./README.md">简体中文</a>
</p>

> A sanitized Agentic Coding workflow: thin routing rules plus reusable skills for AI-assisted coding, debugging, testing, commits, and design discussion.

## Quick Start

```bash
git clone --recursive https://github.com/MagicKidd/Rokid-agentic-workflow.git ~/.cursor/skills/agentic-coding-workflow
```

### Cursor

```bash
mkdir -p .cursor/rules
ln -s ~/.cursor/skills/agentic-coding-workflow/en/rules/matt-skills-core.mdc .cursor/rules/
ln -s ~/.cursor/skills/agentic-coding-workflow/en/rules/ai-coding-protocol.mdc .cursor/rules/
ln -s ~/.cursor/skills/agentic-coding-workflow/en/rules/design-thinking-tools.mdc .cursor/rules/
ln -s ~/.cursor/skills/agentic-coding-workflow/en/rules/agent-continuity-protocol.mdc .cursor/rules/
```

### Claude Code / OpenCode

Copy `adapters/claude-code/CLAUDE.md` or `adapters/opencode/AGENTS.md` into your project root and replace `<path-to-agentic-coding-workflow>` with your local checkout path.

## Current Workflow

This repository now uses a Matt-style, small composable workflow:

- `matt-skills-core.mdc` only routes intent.
- Coding tasks load focused skills such as `diagnose`, `tdd`, `to-prd`, `to-issues`, `triage`, and `improve-codebase-architecture`.
- Non-coding design discussion is routed by `design-thinking-tools.mdc` to Superpowers thinking tools.
- `ai-coding-protocol.mdc` only keeps guardrails such as smallest effective change, read before write, and verify before completion.

## Structure

```text
agentic-coding-workflow/
├── zh/                     # Chinese rules and skills
├── en/                     # English rules and skills
├── superpowers/            # Community Superpowers submodule
├── adapters/               # Cursor / Claude Code / OpenCode adapters
├── templates/              # Reusable templates
└── docs/                   # Sync reports and showcase assets
```

## Sanitization Boundary

Only general engineering workflow content is included: coding workflow, tests, debugging, architecture, commits, docs, research, frontend, and prompt design. Personal profiles, private links, product-specific names, private repository lists, company-specific rules, and domain-specific skills are excluded.

## License and Credits

This project shares reusable AI coding workflow practices. The `superpowers` directory is imported as a Git submodule and remains under its original authors' copyright.
