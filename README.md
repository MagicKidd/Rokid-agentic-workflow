# Agentic Coding Workflow

<p align="center">
  <img src="https://img.shields.io/badge/Agentic-Workflow-blue.svg" alt="Agentic Workflow">
  <img src="https://img.shields.io/badge/AI_Pair_Programming-Cursor_|_Claude-lightgrey.svg" alt="AI Pair Programming">
</p>

<p align="center">
  [English](./README_en.md) | <b>简体中文</b>
</p>

> 探索在日常开发中，让 AI 编程助手保持上下文连贯与执行纪律的协作协议。

在实际业务开发中，当使用 AI（如 Cursor, Claude Code）处理复杂任务时，AI 往往容易在长对话中丢失上下文，或在缺乏充分设计的情况下急于编码，导致代码过度工程或引入缺陷。

**Agentic Coding Workflow** 是一套面向开发者的 AI 协作协议。它通过预定义的调度规则（Rules）和专业技能包（Skills），将任务拆解为从上下文采集、方案设计到代码实现、自动化验证的结构化步骤，从而让 AI 的协作过程更加可控和规范。

## 📖 目录
- [核心思路](#-核心思路)
- [快速接入](#-快速接入)
- [目录结构](#-目录结构)
- [基础使用](#-基础使用)
- [许可与致谢](#-许可与致谢)

---

## 💡 核心思路

- **应对上下文丢失**：通过自动化信息采集（Phase 1），在对话之初检索关联代码、架构文档和历史避坑记录，确保基线信息完整。
- **引入工程纪律**：在编码前设立"决策点"（Phase 2 & 3）。只有在方案确认后，AI 才会被授权加载 TDD、多步拆解等专业技能（Phase 4）进行规范化开发。
- **先验证再闭环**：在宣称修复缺陷或完成开发前，强制要求提供运行测试用例的真实证据。

👉 **[点击查看详细的工作流核心思路与架构全景图 (WORKFLOW.md)](./WORKFLOW.md)**

---

## ⚡ 快速接入

无论你使用的是哪款主流的 AI 编程工具，这套基于纯 Markdown 的方法论都能相对轻松地集成到你的工作环境中。

### 1. 获取套件

将本仓库克隆到你的本地。为了包含 `superpowers` 核心基础依赖，请务必使用 `--recursive` 参数：

```bash
# 建议放置在全局的可重用目录
mkdir -p ~/.cursor/skills_shared
cd ~/.cursor/skills_shared
git clone --recursive https://github.com/Rokid/agentic-coding-workflow.git
```

### 2. IDE 适配配置

根据你日常使用的 AI IDE，选择对应的接入方式：

#### 🔹 Cursor 用户
Cursor 原生支持读取项目 `.cursor/rules` 目录下的 `.mdc` 规则文件。

1. 在你的业务项目根目录执行：
```bash
mkdir -p .cursor/rules
# 使用软链接，方便未来统一更新工作流
ln -s ~/.cursor/skills_shared/agentic-coding-workflow/rules/new-task-trigger.mdc .cursor/rules/
ln -s ~/.cursor/skills_shared/agentic-coding-workflow/rules/new-task-kickoff.mdc .cursor/rules/
```
2. 打开 Cursor 的 Composer，直接输入指令（如："开始做一个新功能..."），触发器将自动引导 AI 进入分步流程。
*(更多说明见 [adapters/cursor/README.md](adapters/cursor/README.md))*

#### 🔹 Claude Code 用户
Claude Code 依赖项目根目录的 `CLAUDE.md` 来加载系统级上下文。

1. 将 `adapters/claude-code/CLAUDE.md` 复制到你的业务项目根目录。
2. 编辑该 `CLAUDE.md`，将其中的 `<path-to-agentic-coding-workflow>` 替换为你实际克隆本仓库的绝对路径。
3. 运行 `claude` 并下达任务，Claude 会自动阅读指定的 Skills 并遵循协议。

#### 🔹 OpenCode 及其他
同理，将 `adapters/opencode/AGENTS.md` 复制到项目根目录并修改绝对路径即可。

---

## 📦 目录结构

```text
agentic-coding-workflow/
├── rules/                  # 流程调度规则（拦截任务指令并引导分步执行）
├── skills/                 # 核心技能库（需求探讨、架构分析、TDD等实践指南）
├── superpowers/            # [推荐依赖] obra/superpowers 优秀的社区基石实践
├── templates/              # 可复用模板（如项目规则约定、避坑记录文件）
├── adapters/               # 跨 IDE 适配指南（Cursor / Claude Code / OpenCode）
├── README.md               # 简体中文说明
└── WORKFLOW.md             # 详细工作流设计说明
```

---

## 🛠️ 基础使用

配置完成后，当你需要让 AI 协助开发时，不再需要交代冗长的背景。你可以使用简单的指令启动：

> **"开始重构用户认证模块"** 或 **"启动新任务：增加数据导出功能"**

AI 会受到规则的约束，将工作分为几个阶段进行：
1. **自动采集 (Phase 1)**：在后台检索与任务相关的代码、架构文档以及曾经的踩坑记录。
2. **汇报与决策 (Phase 2 & 3)**：向你总结它找到的上下文，并询问你的决定（例如是需要针对边界条件深入讨论设计，还是可以直接开始拆解计划）。
3. **分步执行 (Phase 4)**：在你确认方案后，AI 会加载相应的开发技能（如 TDD 测试驱动、多步骤计划拆解）开始规范地编写代码。

---

## 📜 许可与致谢

本项目开源，欢迎开发者们交流与贡献。

在构建这套工作流的过程中，我们参考和借鉴了开源社区中优秀的实践经验。特别感谢 [@obra](https://github.com/obra/superpowers-skills) 提供的 `superpowers` 集合，它包含了大量极具价值的底层工程纪律设计。本仓库内的 `superpowers` 目录作为 Git Submodule 引入，其版权归原作者所有。
