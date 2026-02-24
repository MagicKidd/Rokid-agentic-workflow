# Agentic Workflow: 人类主导设计，AI 自主执行

## 一、理念：为什么需要 Agentic 工作协议？

在 AI 辅助编程（如 Cursor, Claude Code 等）中，开发者常遇到两大核心瓶颈：
1. **上下文遗忘与污染**：AI 容易在一个长对话中忘记最初的目标，或者因为代码库庞大而产生"幻觉"；
2. **缺乏流程纪律**：AI 经常在没有完全理解需求的情况下急于写代码，导致反复修改、过度工程甚至引入新的 Bug。

**Agentic Workflow Kit** 由 Rokid 研发工程师 **Jingliang** 设计并提炼。它不仅仅是几个提示词（Prompt），而是一套严密的 **"AI 工程师工作协议"**，它的核心理念是：

> **设计阶段 = 人类驱动（AI 准备上下文，人类决定方向）**
> **实施阶段 = AI 驱动（方案确认后，AI 自主调用 Skills 链条高效推进）**

通过这套工作流，我们将原本不可控的对话，变成了一条具有明确质量门控（Quality Gates）的工业化生产线。

---

## 二、工作流全景图

当你在 IDE 中输入类似 _"开始做一个新功能"_ 或 _"重构认证模块"_ 时，调度引擎会立即拦截并拉起以下四个 Phase（阶段）：

```mermaid
graph TD
    User([用户发起新任务]) --> P1
    
    subgraph Phase 1: 自动上下文采集 (并行)
        P1[感知与嗅探] --> |Task 子代理| P1A[历史对话搜索]
        P1 --> |Task 子代理| P1B[相关文档匹配]
        P1 --> |Task 子代理| P1C[已有规则/教训检查]
        P1 --> |Task 子代理| P1D[代码与近期变更分析]
    end
    
    P1A & P1B & P1C & P1D --> P2
    
    subgraph Phase 2 & 3: 摘要与人类决策
        P2[呈现结构化上下文摘要] --> P3{等待人类决策}
        P3 -->|A. 方案不明确| C1[深度设计讨论]
        P3 -->|B. 方案清晰| C2[实施计划制定]
        P3 -->|C. 简单明确| C3[直接编码]
        P3 -->|D. 排查缺陷| C4[系统化调试]
    end
    
    subgraph Phase 4: AI 自主执行链 (基于 Skills)
        C1 --> |brainstorming| Doc[产出设计文档]
        Doc --> C2
        
        C2 --> |writing-plans| Plan[拆解任务步骤]
        Plan --> |subagent-driven| Exec[派发子代理并行执行]
        
        Exec --> |requesting-code-review| Review[代码审查]
        Review --> |TDD & kaizen| Valid[完成前验证]
        
        C3 --> Valid
        
        C4 --> |systematic-debugging| Fix[根因调查与修复]
        Fix --> Valid
        
        Valid --> |finishing-branch| Done([完成并清理分支])
    end
    
    classDef phase fill:#f9f9f9,stroke:#333,stroke-width:2px;
    class P1,P2,P3,Phase4 phase;
```

### Phase 1: 自动上下文采集
AI 不会立刻回答，而是派出多个子代理（Sub-agents）去后台执行 `grep`、搜索文档、查阅历史教训（Lessons Learned），并在几秒内完成全盘扫描。

### Phase 2 & 3: 摘要呈现与人类决策
AI 将收集到的信息进行结构化总结，列出发现的约束、依赖，并向人类请示接下来的行动路径。

### Phase 4: AI 自主执行链
人类一旦做出选择，AI 便会根据路径自动加载对应的专业知识库（Skills），开始无需人类干预的"链式操作"。比如：拆解任务 -> 派发子代理写测试 -> 编码 -> 代码审查 -> 验证 -> 提交。

---

## 三、核心 Skills 说明

Skills 就像是 AI 的"能力插件"。我们将它们分为几个圈层，相互配合：

### 1. 流程调度引擎（核心）
- **`new-task-trigger.mdc`**：信号拦截器，常驻后台。
- **`new-task-kickoff.mdc`**：总司令，定义了上面提到的 Phase 1-4 协议。

### 2. 思维工具（决策增强）
在 Phase 3 人类决策阶段，如果方向不明确，AI 会动用这些能力：
- **`brainstorming`**：结构化头脑风暴，一次一问，强制提供多选选项，增量确认设计。
- **`expert-debate`**：让两个 AI 专家进行三轮辩论，解决技术分歧。
- **`expert-collaboration`**：让不同领域的 AI 专家各自贡献视角，渐进收敛。
- **`internalized-cognition`**：让 AI "成为"系统本身，从第一人称视角获取深层洞察。

### 3. 工程实践（质量保障）
在 Phase 4 执行阶段，AI 的行为受到这些规范的严格约束：
- **`software-architecture`**：强制遵循 Clean Architecture 和 DDD，杜绝随意堆砌代码。
- **`kaizen`**：持续改进，防错设计（Poka-Yoke），拒绝过度工程（YAGNI）。
- **`subagent-driven-development`**：用子代理执行独立任务，防止长对话污染。
- **`planning-with-files`**：通过生成 `task_plan.md` 建立"外置工作记忆"。
- **`test-driven-development`**：红-绿-重构循环，无测试不编码的铁律。

### 4. AI 元能力（自我进化）
- **`find-skills`**：让 AI 学会去查阅自己有什么能力，并有安全审核流程。
- **`skill-creator`**：标准化创建新 Skill 的流程。
- **`prompt-engineering`**：撰写高效提示词的方法论。

### 5. Superpowers (推荐基石依赖)
本项目将社区顶级的 [obra/superpowers](https://github.com/obra/superpowers-skills) 作为子模块引入。它提供了大量优秀的底层实践，如系统化调试 (`systematic-debugging`)、验证门控 (`verification-before-completion`) 等，被我们的调度引擎在关键节点调用。

---

## 四、定制指南

### 1. 如何添加你的项目专属规则
你可以为不同的项目或模块创建专属的规则文件（`.mdc`）。只需将它们放在 `.cursor/rules/` 目录下，并在头部添加描述。`new-task-kickoff` 在 Phase 1 会自动将它们扫描出来并应用。
（可参考 `templates/project-rules-example.mdc`）

### 2. 如何记录全局教训
在与 AI 协作时，如果 AI 犯了错，你可以纠正它并告诉它"把这个加入全局教训"。AI 会自动将该教训追加到 `_global_lessons.md`（见 `templates/`）中。这样，下次启动任何新任务时，AI 都会提前规避这个错误。

### 3. 如何扩展新 Skill
让 AI 执行："使用 `skill-creator` 帮我创建一个名为 `xxx` 的新技能"。AI 会按照标准流程询问你的需求，提炼出可复用的组件，并生成完整的 `SKILL.md` 文档。