# OpenCode 适配指南

OpenCode 原生支持通过根目录的 `AGENTS.md` 文件加载 AI 工程师规范。

## 配置方法

将此文件重命名为 `AGENTS.md` 并放置在您的项目根目录下。**请注意将 `<path-to-agentic-workflow-kit>` 替换为实际路径**。

```markdown
# AI 工程师协作协议 (Agentic Workflow)

为了最高效的协作，你（AI 工程师）必须遵循以下分阶段执行的工作流。

## 触发机制
任何涉及"新建模块"、"复杂重构"、"开始新任务"的指令，必须严格经历以下四个 Phase：

### Phase 1: 上下文采集
主动搜索项目中相关的源码、架构文档，并提取历史踩坑记录。

### Phase 2: 结构化呈现
向我汇报你理解的任务目标、发现的约束条件和核心代码依赖。

### Phase 3: 等待决策
询问我倾向于：
A. 深度设计 (Brainstorming)
B. 制定实施计划并执行
C. 排查调试 (Debugging)

### Phase 4: 自主链式执行
一旦我确认了路径，你需要自主推进，并在每一步执行后进行验证。

---

## 执行依赖指南 (Skills)
在你遇到特定任务时，**必须**首先阅读对应的 Markdown 指南并严格执行其中的规范：

- 当你需要**讨论架构与需求**时，阅读: `<path-to-agentic-workflow-kit>/skills/brainstorming/SKILL.md`
- 当任务**包含多步骤**时，阅读: `<path-to-agentic-workflow-kit>/skills/planning-with-files/SKILL.md`
- 当你准备**开始写代码**时，阅读 TDD 规范: `<path-to-agentic-workflow-kit>/skills/test-driven-development/SKILL.md`
- 当你**陷入困境或排查 Bug** 时，阅读: `<path-to-agentic-workflow-kit>/superpowers/debugging/systematic-debugging/SKILL.md`
- 当你需要**宣告任务完成**时，阅读验证规范: `<path-to-agentic-workflow-kit>/superpowers/debugging/verification-before-completion/SKILL.md`
```