# Agentic Coding Workflow

[English](./README_en.md) | 简体中文

> 探索在日常开发中让 AI 编程助手保持上下文连贯和执行纪律的协作模式。

Agentic Coding Workflow 是一套面向开发者的 AI 协作协议。在 Rokid 的实际业务开发中，团队（Jing 等）发现 AI（如 Cursor, Claude Code）在处理复杂任务时，往往容易丢失上下文或在没有充分设计的情况下急于编码。为此，我们整理了这套工作流。

它通过预定义的调度规则（Rules）和专业技能包（Skills），将任务拆解为从上下文采集、方案设计到代码实现、自动化验证的结构化步骤，从而让 AI 的协作过程更加可控和规范。

详见：[👉 工作流核心思路与全景图 (WORKFLOW.md)](./WORKFLOW.md)

---

## 📦 目录结构

```text
agentic-coding-workflow/
├── rules/                  # 流程调度规则（拦截任务指令并引导分步执行）
├── skills/                 # 核心技能库（包含需求分析、架构指导、测试驱动等实践）
├── superpowers/            # [推荐依赖] obra/superpowers 优秀的社区实践合集
├── templates/              # 可复用模板（如项目规则约定、避坑记录）
├── adapters/               # 跨 IDE 适配指南（Cursor / Claude Code / OpenCode）
├── README.md               # 本文档
└── WORKFLOW.md             # 详细工作流设计说明
```

---

## ⚡ 快速开始

无论你使用的是哪款 AI 编程工具，这套基于纯 Markdown 的方法论都能相对容易地接入。

### 1. 获取套件

将本仓库克隆到你的本地。为了包含 `superpowers` 子模块，建议使用 `--recursive` 参数：

```bash
# 建议放置在全局的可重用目录
mkdir -p ~/.cursor/skills_shared
cd ~/.cursor/skills_shared
git clone --recursive https://github.com/Rokid/agentic-coding-workflow.git
```

### 2. IDE 适配配置

根据你日常使用的 AI IDE，选择对应的接入方式：

#### 🔹 Cursor 用户
Cursor 原生支持读取项目 `.cursor/rules` 目录下的 `.mdc` 规则。

1. 在你的项目根目录执行：
```bash
mkdir -p .cursor/rules
# 使用软链接，方便统一更新工作流
ln -s ~/.cursor/skills_shared/agentic-coding-workflow/rules/new-task-trigger.mdc .cursor/rules/
ln -s ~/.cursor/skills_shared/agentic-coding-workflow/rules/new-task-kickoff.mdc .cursor/rules/
```
2. 打开 Cursor 的 Composer，直接输入："开始做一个新功能..."，触发器将自动引导执行步骤。
*(更多说明见 [adapters/cursor/README.md](adapters/cursor/README.md))*

#### 🔹 Claude Code 用户
Claude Code 依赖项目根目录的 `CLAUDE.md` 来加载系统级上下文。

1. 将 `adapters/claude-code/CLAUDE.md` 复制到你的项目根目录。
2. 编辑该 `CLAUDE.md`，将其中的 `<path-to-agentic-coding-workflow>` 替换为你实际克隆本仓库的绝对路径。
3. 运行 `claude` 并下达任务，Claude 会自动阅读指定的 Skills 并遵循流程。

#### 🔹 OpenCode 及其他
同理，将 `adapters/opencode/AGENTS.md` 复制到项目根目录并修改绝对路径即可。

---

## 🛠️ 基本使用

配置完成后，当你需要让 AI 协助开发时，可以使用简单的指令启动：

> **"开始重构用户认证模块"** 或 **"启动新任务：增加导出功能"**

AI 会根据规则分为几个阶段：
1. **自动采集 (Phase 1)**：在后台检索关联代码、架构文档和历史踩坑记录。
2. **汇报与决策 (Phase 2 & 3)**：向你总结它找到的上下文，并询问你的决定（例如是需要深入讨论设计，还是直接开始编码）。
3. **分步执行 (Phase 4)**：在你确认方案后，AI 会加载相应的开发技能（如 TDD 测试驱动、多步骤计划拆解）开始编码。

---

## 🌟 核心实践参考

- **先验证再确认**：在宣称修复缺陷之前，需有执行测试用例的证据。
- **测试驱动 (TDD)**：倡导在编写业务代码前先编写失败的测试用例。
- **任务拆解**：针对复杂任务，鼓励通过外部文件 (`task_plan.md`) 管理进度，或者派发子代理并行处理不相关的任务，防止单次对话上下文过载。

## 📜 许可与致谢

本项目开源，欢迎交流与贡献。

在构建这套工作流的过程中，我们参考和借鉴了开源社区中优秀的实践经验。特别感谢 [@obra](https://github.com/obra/superpowers-skills) 提供的 `superpowers` 集合，它包含了大量极具价值的底层工程纪律设计。本仓库内的 `superpowers` 目录作为 Git Submodule 引入，版权归原作者所有。