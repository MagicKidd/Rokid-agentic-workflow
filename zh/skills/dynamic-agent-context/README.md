# Dynamic Agent Context

让 AI 在任意项目中自动学习本地工程约定，并在代码相关任务中按需加载。

## 这套方案解决什么问题

- 不再写死单项目规则：从代码库自动提取约定
- 降低 AI 代码风格漂移：生成可执行的约定规则
- 兼容多编辑器：Cursor / Claude Code / OpenCode / Codex

## 目录结构

```text
dynamic-agent-context/
└── scripts/
    ├── generate_agent_context.py
    ├── refresh_agent_context.py
    └── sync_agent_entrypoints.py
```

## 安装（人执行一次）

### 1) 安装/更新 Skills 仓库

```bash
git clone https://github.com/<your-org>/<your-skills-repo>.git ~/.cursor/skills
# 已有仓库时
cd ~/.cursor/skills && git pull origin main --ff-only
```

### 2) 将脚本放入目标项目

在目标项目根目录创建 `scripts/`，复制三段脚本：

```bash
cp ~/.cursor/skills/dynamic-agent-context/scripts/generate_agent_context.py <project>/scripts/
cp ~/.cursor/skills/dynamic-agent-context/scripts/refresh_agent_context.py <project>/scripts/
cp ~/.cursor/skills/dynamic-agent-context/scripts/sync_agent_entrypoints.py <project>/scripts/
```

### 3) 首次初始化

```bash
cd <project>
python scripts/refresh_agent_context.py --full
```

初始化后会生成：

- `.agent-context/conventions.md`
- `.agent-context/project-context.md`
- `.agent-context/metadata.json`
- `AGENTS.md`
- `CLAUDE.md`
- `.cursor/rules/learned-conventions.mdc`（`alwaysApply: false`）

## 日常使用

- 全量刷新：`python scripts/refresh_agent_context.py --full`
- 增量刷新：`python scripts/refresh_agent_context.py --changed-only`

## AI 如何使用

### Cursor

1. 自动加载全局基线：`~/.cursor/rules/ai-coding-protocol.mdc`
2. 在代码任务中按需加载：`.cursor/rules/learned-conventions.mdc`
3. 详细统计来源：`.agent-context/conventions.md`

### Claude Code / OpenCode / Codex

- 读取项目根 `AGENTS.md`（或 `CLAUDE.md`）作为入口
- 再读取 `.agent-context/*` 获取项目学习结果

## 推荐触发词（给 AI）

- “刷新学习上下文”
- “更新本项目学习规则”
- “重新生成 learned-conventions”
- “按最新代码重建 agent-context”

## 验证清单

```bash
test -f .agent-context/conventions.md
test -f .agent-context/project-context.md
test -f .agent-context/metadata.json
test -f .cursor/rules/learned-conventions.mdc
shasum AGENTS.md CLAUDE.md
```

若 `AGENTS.md` 与 `CLAUDE.md` 的哈希相同，即同步成功。
