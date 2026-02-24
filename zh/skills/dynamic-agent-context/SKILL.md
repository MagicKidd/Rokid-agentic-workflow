---
name: dynamic-agent-context
description: 在任意项目中安装并刷新动态学习上下文（.agent-context、AGENTS.md、learned-conventions.mdc）。用于编写代码、工程架构代码设计、测试、重构、代码审查、修复 bug。
---

# Dynamic Agent Context（动态学习上下文）

让 AI 从项目真实代码中提炼可执行的本地工程约定，并在代码相关任务中按需加载。

## 产物（在项目根目录生成）

- `.agent-context/conventions.md`：完整学习档案（统计 + 可执行指令）
- `.agent-context/project-context.md`：项目画像（结构、技术信号）
- `.agent-context/metadata.json`：机器可读指标
- `.cursor/rules/learned-conventions.mdc`：Cursor 按需加载的“精简约定”
- `AGENTS.md` / `CLAUDE.md`：跨编辑器入口（Claude Code / OpenCode / Codex）

## 安装（人执行一次）

在目标项目根目录执行：

```bash
mkdir -p scripts
# 如果你将本仓库克隆到 ~/.cursor/skills：
cp ~/.cursor/skills/zh/skills/dynamic-agent-context/scripts/generate_agent_context.py scripts/
cp ~/.cursor/skills/zh/skills/dynamic-agent-context/scripts/refresh_agent_context.py scripts/
cp ~/.cursor/skills/zh/skills/dynamic-agent-context/scripts/sync_agent_entrypoints.py scripts/

python scripts/refresh_agent_context.py --full
```

## 日常刷新

- 增量：`python scripts/refresh_agent_context.py --changed-only`
- 全量：`python scripts/refresh_agent_context.py --full`

## AI 如何使用

- Cursor：在代码相关任务中自动注入 `.cursor/rules/learned-conventions.mdc`
- 其他编辑器：读取 `AGENTS.md` / `CLAUDE.md`，再读取 `.agent-context/*`

