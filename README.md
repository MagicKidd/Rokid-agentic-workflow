# Rokid Agentic Coding

<p align="center">
  <img src="https://img.shields.io/badge/Agentic-Workflow-blue.svg" alt="Agentic Workflow">
  <img src="https://img.shields.io/badge/AI_Pair_Programming-Cursor_|_Claude-lightgrey.svg" alt="AI Pair Programming">
</p>

<p align="center">
  <a href="./README_en.md">English</a> | <b>简体中文</b>
</p>

> 用流程协议接管行为，重塑 AI 编程的工程纪律。这是一份面向高级研发的架构说明文件。单体大模型解决不了复杂的软件工程问题。我们通过开源 Rokid-agentcode，把 AI 从一个“盲目打字的打字机”，驯化成了一个“有规矩、按阶段推进的系统工程师”。

<div align="center">
  <img src="./docs/showcase.png" alt="Agentic Workflow Architecture Showcase" width="100%">
</div>

---

## 📖 快速索引
- [快速接入](#-快速接入)
- [目录结构](#-目录结构)
- [基础使用](#-基础使用)
- [许可与致谢](#-许可与致谢)

---

## ⚡ 快速接入

无论你使用的是哪款主流的 AI 编程工具，这套基于纯 Markdown 的方法论都能相对轻松地集成到你的工作环境中。

### 1. 获取套件

将本仓库克隆到你的本地。为了包含 `superpowers` 核心基础依赖，请务必使用 `--recursive` 参数：

```bash
# 建议放置在全局的可重用目录
mkdir -p ~/.cursor/skills
cd ~/.cursor/skills
git clone --recursive https://github.com/MagicKidd/Rokid-agentcode.git .
```

### 2. IDE 适配配置

根据你日常使用的 AI IDE，选择对应的接入方式：

#### 🔹 Cursor 用户
Cursor 原生支持读取项目 `.cursor/rules` 目录下的 `.mdc` 规则文件。

1. 在你的业务项目根目录执行：
```bash
mkdir -p .cursor/rules
# 使用软链接，方便未来统一更新工作流
ln -s ~/.cursor/skills/zh/rules/ai-coding-protocol.mdc .cursor/rules/
ln -s ~/.cursor/skills/zh/rules/new-task-trigger.mdc .cursor/rules/
ln -s ~/.cursor/skills/zh/rules/new-task-kickoff.mdc .cursor/rules/
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
Rokid-agentcode/
├── zh/                     # 中文版规则和技能
│   ├── rules/              # 流程调度规则
│   └── skills/             # 核心技能库
├── en/                     # 英文版规则和技能
│   ├── rules/
│   └── skills/
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
