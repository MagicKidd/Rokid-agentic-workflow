# Claude Code 适配指南

Claude Code 原生支持通过根目录的 `CLAUDE.md` 文件加载项目上下文。

## 配置方法

将此文件重命名为 `CLAUDE.md` 并放置在您的项目根目录下。**请注意将 `<path-to-agentic-workflow-kit>` 替换为实际路径**。

```markdown
# 项目上下文与执行协议

## Agentic Workflow 协议
执行任何复杂任务前，**必须**严格遵循预定义的工作流阶段（Phase 1-4）。

### 触发条件
当被要求"新任务"、"新功能"、"开始做"时，立即执行以下流程：

### Phase 1: 自动上下文采集
执行环境嗅探，并行搜索相关代码、文档和历史经验教训。

### Phase 2: 上下文摘要呈现
向我展示结构化的任务理解、已有决策和待确认项。

### Phase 3: 需求确认
等待我确认方向。

### Phase 4: 执行链
根据我选择的路径，自主调用相应 Skills 推进。

---

## 核心 Skills 指引
在执行上述 Phase 或任何任务时，你必须查阅以下 Skills 来指导你的行为（使用 `cat` 读取内容）：

- **设计讨论**: `cat <path-to-agentic-workflow-kit>/skills/brainstorming/SKILL.md`
- **复杂规划**: `cat <path-to-agentic-workflow-kit>/skills/planning-with-files/SKILL.md`
- **子代理执行**: `cat <path-to-agentic-workflow-kit>/skills/subagent-driven-development/SKILL.md`
- **TDD 规范**: `cat <path-to-agentic-workflow-kit>/skills/test-driven-development/SKILL.md`
- **持续改进**: `cat <path-to-agentic-workflow-kit>/skills/kaizen/SKILL.md`

## 推荐依赖 (Superpowers)
你还可以参考以下超级技能以提升问题解决能力：
- 调试指南: `cat <path-to-agentic-workflow-kit>/superpowers/debugging/systematic-debugging/SKILL.md`
- 完成前验证: `cat <path-to-agentic-workflow-kit>/superpowers/debugging/verification-before-completion/SKILL.md`
```