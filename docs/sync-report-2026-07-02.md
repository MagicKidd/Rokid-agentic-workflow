# Open Workflow Sync Report - 2026-07-02

## Source

- Private source: local latest skills library under `<user_home>/.cursor/skills`
- Shared target: `https://github.com/MagicKidd/Rokid-agentic-workflow.git`

## Synced Scope

Synced the generic engineering workflow layer:

- Rules: `matt-skills-core`, `ai-coding-protocol`, `design-thinking-tools`, `agent-continuity-protocol`
- Core coding skills: `diagnose`, `tdd`, `to-prd`, `to-issues`, `triage`, `improve-codebase-architecture`, `zoom-out`
- Tooling and delivery skills: `safe-commit`, `setup-pre-commit`, `git-guardrails-claude-code`, `setup-matt-pocock-skills`, `dynamic-agent-context`, `skill-creator`
- Reusable collaboration/design skills: `community-solution-research`, `design-impl-audit`, `design-session-scribe`, `expert-collaboration`, `expert-debate`, `grill-with-docs`, `prompt-engineering`, `frontend-design`, `ui-ux-pro-max`

## Explicitly Excluded

Not synced because they are personal, company-specific, product-specific, third-party bulk packages, or private operational knowledge:

- Personal profile/persona/repository list rules and skills
- Product-specific skills such as glasses, dense recognition, vector database, admin permission, private domain experts, or dataflow-doc sync
- Internal report/memo delivery skills that contain business examples or local prompts
- Large document-processing third-party packages already better sourced from their upstream providers

## Sanitization

Applied text-level replacement for:

- Personal absolute paths -> `<user_home>` / `<project_root>`
- Private repository pointers -> generic placeholders
- Internal hostnames -> `<private_git_host>`
- Product-specific wording in synced files where encountered

## Structural Changes

- Replaced old Phase-style rules with Matt-style thin routing rules.
- Removed old first-party core skill directories from `zh/skills` and `en/skills`: `kaizen`, `software-architecture`, `test-driven-development`, `planning-with-files`, `subagent-driven-development`.
- Updated README, workflow docs, and IDE adapters to point at the new rule set.
