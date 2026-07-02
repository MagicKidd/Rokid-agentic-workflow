# Agentic Coding Workflow

<p align="center">
  <img src="https://img.shields.io/badge/Agentic-Workflow-blue.svg" alt="Agentic Workflow">
  <img src="https://img.shields.io/badge/AI_Pair_Programming-Cursor_|_Claude-lightgrey.svg" alt="AI Pair Programming">
</p>

<p align="center">
  <a href="./README_en.md">English</a> | <b>简体中文</b>
</p>

> 一套脱敏后的 Agentic Coding 工作流：用薄规则做路由，用可复用 skills 约束 AI 编程、调试、测试、提交和设计讨论。

## 快速接入

```bash
git clone --recursive https://github.com/MagicKidd/Rokid-agentic-workflow.git ~/.cursor/skills/agentic-coding-workflow
```

### Cursor

```bash
mkdir -p .cursor/rules
ln -s ~/.cursor/skills/agentic-coding-workflow/zh/rules/matt-skills-core.mdc .cursor/rules/
ln -s ~/.cursor/skills/agentic-coding-workflow/zh/rules/ai-coding-protocol.mdc .cursor/rules/
ln -s ~/.cursor/skills/agentic-coding-workflow/zh/rules/design-thinking-tools.mdc .cursor/rules/
ln -s ~/.cursor/skills/agentic-coding-workflow/zh/rules/agent-continuity-protocol.mdc .cursor/rules/
```

### Claude Code / OpenCode

复制 `adapters/claude-code/CLAUDE.md` 或 `adapters/opencode/AGENTS.md` 到你的项目根目录，并替换其中的 `<path-to-agentic-coding-workflow>`。

## 当前工作流

本仓库已更新为 Matt-style 小型可组合 workflow：

- `matt-skills-core.mdc` 只负责意图路由。
- 编程任务按 `diagnose`、`tdd`、`to-prd`、`to-issues`、`triage`、`improve-codebase-architecture` 等 skills 执行。
- 非编码设计讨论由 `design-thinking-tools.mdc` 路由到 Superpowers 思维工具。
- `ai-coding-protocol.mdc` 只保留最小有效改动、先读后写、验证后收尾等护栏。

## 目录结构

```text
agentic-coding-workflow/
├── zh/                     # 中文规则与 skills
├── en/                     # 英文规则与 skills
├── superpowers/            # 社区 Superpowers 子模块
├── adapters/               # Cursor / Claude Code / OpenCode 适配
├── templates/              # 可复用模板
└── docs/                   # 同步报告与展示资源
```

## 脱敏边界

同步内容只保留通用工程方法：工作流、测试、调试、架构、提交、文档、调研、前端和 prompt 设计。个人画像、内网链接、业务项目名、私有仓库清单、公司专项规则和产品特定 skills 不进入本仓库。

## 许可与致谢

本项目用于共享可复用的 AI coding workflow。`superpowers` 目录通过 Git submodule 引入，版权归原作者所有。
