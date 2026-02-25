# Rokid-agentcode (原 Agentic Coding Workflow)

<p align="center">
  <img src="https://img.shields.io/badge/Agentic-Workflow-blue.svg" alt="Agentic Workflow">
  <img src="https://img.shields.io/badge/AI_Pair_Programming-Cursor_|_Claude-lightgrey.svg" alt="AI Pair Programming">
</p>

<p align="center">
  <a href="./README_en.md">English</a> | <b>简体中文</b>
</p>

> 用流程协议接管行为，重塑 AI 编程的工程纪律。这是一份面向高级研发的架构说明文件。单体大模型解决不了复杂的软件工程问题。我们通过开源 Rokid-agentcode，把 AI 从一个“盲目打字的打字机”，驯化成了一个“有规矩、按阶段推进的系统工程师”。

---

## 🚀 01. 最先进的 AI Coding 架构演进

技术演进正在经历三个截然不同的阶段：

*   **GEN 1: Copilot 时代 (高级打字机)**：基于上下文的单点补全。IDE 插件截取光标前后的短文本，发送给模型。它只能解决“怎么写这个函数”的语法问题，完全缺乏项目全局视图，无法解决架构问题。
*   **GEN 2: Chat & RAG 时代 (带搜索引擎的外包)**：基于检索的问答与单步修改。通过向量搜索将相关文件拼接到 Prompt。但它缺乏纪律，收到指令就立刻动工，容易破坏分层架构。而且多轮对话后会导致严重的“失忆”与上下文污染。
*   **GEN 3: Agentic Workflow (有纪律的系统工程师)**：引入状态机、多智能体与工具链。模型不再是直接的代码生成器，而是被嵌入到一个有严格规则控制的工作流中。人类只做高层架构决策，AI 负责底层的脏活累活并强制闭环验证。

> **核心论点：单体大模型解决不了复杂的软件工程问题，我们需要的不是更聪明的大模型，而是“控制大模型行为的架构协议”。**

---

## 🧩 02. 解构三剑客：Agent / Rules / Skills

在我们的架构中，必须用软件工程的语言重新定义它们，消除抽象感：

*   **Rules (规则) - 静态宪法**：被动触发的、声明式（Declarative）的约束条件（如 `.mdc` 文件）。
    *   **作用**：定义系统的边界与红线。**类比**：项目中的 Linter 和团队架构规范手册。
*   **Main Agent - Orchestrator (主代理)**：作为网关和项目经理，负责接受 Rules 监督，拆解任务，分配执行。
*   **Skills (技能) - 动态 SOP**：主动加载的、命令式（Imperative）的执行手册（如 TDD）。
    *   **作用**：赋予 AI 特定领域的专业方法论。**类比**：某项业务的标准化操作指南。
*   **Subagents (并发执行集群 / 微服务)**：由主代理派生出，具有独立上下文。实现**分而治之，隔离污染**，防止长文本导致的记忆混乱。

---

## 🗺️ 03. 规则库与技能树矩阵 (The Catalog)

我们构建的并非一段 Prompt，而是一个精密如游戏技能树的“法则矩阵”，覆盖了软件生命周期的每个角落。

### 全生态依赖结构图 (Ecosystem Architecture)
1. **第 1 层（意图雷达与环境）**：`new-task-trigger`（意图雷达嗅探器）与 `[项目]-playbook`（项目环境与依赖挂载）。
2. **第 2 层（守门人）**：`new-task-kickoff.mdc`（核心总控与状态机引擎）。
3. **第 3 层（宪法）**：`ai-coding-protocol` 与 `core-engineering-principles`（全局工程纪律底线）。
4. **第 4 层（武器库）**：挂载了 5 大分类、囊括 15 个技能的 Skills Array（工作流域、架构域、专家域、防错域、生态域）。
5. **第 5 层（基座）**：底层能力支撑脚本（Python / Shell / CLI）。

### 核心规则系 (Rules) - 静态宪法
*   **`new-task-kickoff.mdc` (核心总控)**：任务启动的绝对入口。强制挂起 AI，执行 4 阶段的流转与上下文收集。
*   **`ai-coding-protocol.mdc` (纪律基线)**：无论处于何种状态都必须遵守的底线：最小化变更、先读后写、差异自审。
*   **`new-task-trigger.mdc` (意图嗅探)**：智能监听用户对话，识别“新需求/新设计”等意图，自动加载并触发 kickoff 流程。
*   **`core-engineering-principles.mdc` (架构底座)**：定义系统设计的核心原则（如高内聚低耦合），为 AI 架构选型提供底层价值观。

### 动态能力域 (15 大开源 Skills 矩阵)
*   **核心开发与工作流**：`test-driven-development`, `subagent-driven-development`, `planning-with-files`, `brainstorming`
*   **架构、前端与提示工程**：`software-architecture`, `frontend-design`, `prompt-engineering`
*   **专家认知与协作系统**：`expert-collaboration`, `expert-debate`, `internalized-cognition`
*   **工程防错与生态扩展**：`kaizen`, `project-documentation`, `skill-creator`, `find-skills`, `dynamic-agent-context`

---

## 🔍 04. 源码级深剖：核心规则逐行拆解

### Engine Alpha: The Gatekeeper（“守门人”引擎）
> 对应源码：`new-task-kickoff.mdc`

大模型有一种天生的“生成冲动”，看到需求就忍不住敲代码。守门人的唯一职责，就是在代码生成的入口处布下关卡，强行将其从“生成态”打断为“挂起态”。
*   **强制上下文嗅探 (Phase 1)**：静默执行六重扫描，包含嗅探配置、查历史对话、看设计文档、搜核心源码、跑 git 变更，以及**读取双层记忆教训 (`lessons.md`)**，让团队所有 AI 自动避坑。
*   **The Blocking Point（强制挂起与人类决策 Phase 2 & 3）**：通过注入高优先级元指令改变大模型的 Logit 分布（如：“必须强制输出：我们要先讨论设计，还是直接出拆解计划？等待用户敲定...”）。**高维度的架构决策，永远必须人类来做。**
*   **智能路由分发与执行链 (Phase 4)**：人类下达“通行证”后，守门人放行并动态路由唤起不同技能（如 TDD 或 排错），并根据任务难度调度模型成本（T1/T2/T4）。

### Engine Beta: The Constitution（“钢铁纪律”引擎）
> 对应源码：`ai-coding-protocol.mdc`

作为全局 `alwaysApply: true` 的最高宪法，防范主 Agent 在漫长链路中出现幻觉、过度工程或代码污染。
*   **自动初始化流程 (Read-Before-Write 5步挂载)**：
    *   **Step 1 Check**: 优先嗅探基线字典。
    *   **Step 2 Sample**: 强制暗中读取同目录真实文件。
    *   **Step 3 Extract**: 现场提炼错误处理、日志习惯与类型密度。
    *   **Step 4 Align**: 覆盖 AI 自带的大众风格。
    *   **Step 5 Verify**: 动笔后修正突兀语法。
*   **最小有效变更 (Smallest Effective Diff)**：偏好能解决请求的最小改动，绝不重构无关代码。
*   **严禁盲造轮子 (Check Before Creating)**：创建新类或工具前，强制全库检索现成的 Helper 复用。
*   **交卷前自查 (Diff Self-Review)**：交付前必须暗中运行命令检查 `git diff`，清理多余冗余。

---

## ⚙️ 05. 四阶段状态机运转 (FSM)

这套工作流的本质是一个有限状态机，将大模型的执行切分为 4 个严格的生命周期：

1.  **Phase 1: 谋定而后动 (强制采集态)**
    *   **触发**：由 `new-task-trigger` 和 `playbook` 截获并挂载。
    *   **行为**：大模型被剥夺代码生成权，在后台静默完成全景上下文的拼装（读代码、文档、`lessons.md`）。
    *   **💡 核心价值**：消除幻觉，确保基于“真实全库视图”而非“金鱼记忆”开局。
2.  **Phase 2 & 3: 架构决策点 (挂起态 / HITL)**
    *   **触发**：由 `new-task-kickoff` 控制。
    *   **行为**：输出调研报告，向人类抛出架构路径选择，原地挂起 (Suspend)。
    *   **💡 核心价值**：Human-in-the-loop。把 AI 从“盲目写代码的外包”变成“提供方案的参谋”，避免南辕北辙的重构。
3.  **Phase 4: 动态路由与自治执行 (执行态)**
    *   **触发**：由 `ai-coding-protocol` 与 `Skills Array` 接管。
    *   **行为**：收到人类指令后生成代码，动态挂载专业技能 SOP，强制闭环跑通测试并自审。
    *   **💡 核心价值**：确定性交付。告别残缺代码，确保每行代码极度贴合原仓库且 100% 跑通。

---
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