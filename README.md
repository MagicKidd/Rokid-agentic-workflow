# Agentic Workflow Kit 🚀

> 将不可控的 AI 对话，变成具有严密质量门控的工业化流水线。

Agentic Workflow Kit 是一套专为资深开发者设计的 **"AI 工程师工作协议"**。它由一系列规则（Rules）和能力插件（Skills）组成，通过拦截任务信号、自动采集上下文、引导人类决策，最后拉起 AI 的自主执行链（TDD, 代码审查, 自动化验证），极大地提升了使用 AI 辅助编程的效率和代码质量。

详见：[👉 工作流核心理念与全景图 (WORKFLOW.md)](./WORKFLOW.md)

---

## 📦 目录结构

```text
agentic-workflow-kit/
├── rules/                  # 流程调度引擎（核心调度规则）
├── skills/                 # 原创核心技能库（思维增强、工程实践、AI 元能力等）
├── superpowers/            # [推荐依赖] obra/superpowers 社区顶级实践集
├── templates/              # 可复用模板（教训记忆、项目规则示例）
├── adapters/               # 跨 IDE 适配指南（Cursor / Claude Code / OpenCode）
├── README.md               # 本文档
└── WORKFLOW.md             # 详细工作流设计说明
```

---

## ⚡ 快速开始

无论你使用的是哪款顶级 AI 编程工具，这套工作流（纯 Markdown 方法论）都能无缝接入。

### 1. 获取套件

首先将本仓库克隆到你的本地电脑。为了包含 `superpowers` 子模块，请加上 `--recursive` 参数：

```bash
# 假设你希望放在统一的共享目录下
mkdir -p ~/.cursor/skills_shared
cd ~/.cursor/skills_shared
git clone --recursive https://github.com/<your-org>/agentic-workflow-kit.git
```

### 2. IDE 适配配置

根据你日常使用的 AI IDE，选择对应的接入方式：

#### 🔹 Cursor 用户
Cursor 原生支持读取项目 `.cursor/rules` 目录下的 `.mdc` 规则。

1. 在你的项目根目录执行：
```bash
mkdir -p .cursor/rules
# 推荐使用软链接，这样你更新 workflow-kit 时，所有项目都能受益
ln -s ~/.cursor/skills_shared/agentic-workflow-kit/rules/new-task-trigger.mdc .cursor/rules/
ln -s ~/.cursor/skills_shared/agentic-workflow-kit/rules/new-task-kickoff.mdc .cursor/rules/
```
2. 打开 Cursor 的 Composer，直接输入："开始做一个新功能..."，工作流即刻触发。
*(更多说明见 [adapters/cursor/README.md](adapters/cursor/README.md))*

#### 🔹 Claude Code 用户
Claude Code 依赖项目根目录的 `CLAUDE.md` 来加载系统级上下文。

1. 将 `adapters/claude-code/CLAUDE.md` 复制到你的项目根目录。
2. **重要**：编辑该 `CLAUDE.md`，将其中的 `<path-to-agentic-workflow-kit>` 替换为你实际克隆本仓库的绝对路径（例如 `/Users/name/.cursor/skills_shared/agentic-workflow-kit`）。
3. 运行 `claude` 并下达任务，Claude 会自动阅读指定的 Skills 并遵循流程。

#### 🔹 OpenCode 及其他
同理，将 `adapters/opencode/AGENTS.md` 复制到项目根目录并修改绝对路径即可。

---

## 🛠️ 如何使用？

接入完成后，你不再需要像以前那样向 AI 交代冗长的背景。只需简单一句：

> **"开始重构用户认证模块"** 或 **"启动新任务：增加导出 Excel 功能"**

AI 将立即进入 **Phase 1 (上下文自动采集)**，你会看到它在后台搜索代码、翻阅文档、查找历史踩坑记录。接着它会向你汇报（**Phase 2**），并请你做出关键架构决策（**Phase 3**）。一旦你确认了路线，它就会自动加载 TDD、Debug 等专业 Skills，开始自主编码和验证（**Phase 4**）。

---

## 🌟 核心理念集锦

- **无验证，不完成**：AI 在宣称修复了 Bug 之前，必须有跑通测试的实质性证据。
- **无测试，不编码**：强制 TDD，看到红色的失败测试，才允许写第一行绿色的生产代码。
- **隔离污染**：使用子代理（Sub-agents）并行处理独立任务，避免单一长对话导致 AI 智商下降。
- **持续教训记忆**：AI 犯错被纠正后，会自动将其记录到全局或局部的 `lessons.md`，下次绝不重犯。

## 📜 许可证 (License)

本项目开源。其中 `superpowers` 目录版权归原作者 [@obra](https://github.com/obra/superpowers-skills) 所有。