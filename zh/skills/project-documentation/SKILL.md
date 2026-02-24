---
name: project-documentation
description: 为项目创建完整的开发指南文档。当开始新项目、接手现有项目、或需要为项目创建 README/CLAUDE.md/开发文档时使用。触发词：项目文档、开发指南、CLAUDE.md、项目规范、架构文档。
---

# 项目文档生成

为任何项目创建结构化的开发指南文档，包含项目概述、开发命令、架构说明、测试指南等。

## 文档结构模板

### 1. 项目概述

```markdown
## Project Overview

[项目名称] 是 [一句话描述项目做什么]。

主要功能：
- 功能 1
- 功能 2
- 功能 3
```

### 2. 开发命令

```markdown
## Development Commands

### 环境设置
\`\`\`bash
# 安装依赖
[包管理器命令]

# 环境变量配置
cp .env.example .env
\`\`\`

### 运行项目
\`\`\`bash
# 开发模式
[开发运行命令]

# 生产模式
[生产运行命令]
\`\`\`

### 测试
\`\`\`bash
# 运行所有测试
[测试命令]

# 运行单个测试
[单测命令]
\`\`\`

### 代码质量
\`\`\`bash
# Lint 检查
[lint 命令]

# 格式化
[format 命令]

# 类型检查
[type check 命令]
\`\`\`
```

### 3. 架构概览

```markdown
## Architecture Overview

### 核心组件

1. **组件A** (`path/to/component_a/`)
   - 职责描述
   - 关键类/函数

2. **组件B** (`path/to/component_b/`)
   - 职责描述
   - 关键类/函数

### 数据流

\`\`\`
输入 → 组件A → 组件B → 组件C → 输出
\`\`\`

### 设计模式

- **模式1**: 用于 [场景]
- **模式2**: 用于 [场景]
```

### 4. 目录结构

```markdown
## Directory Structure

\`\`\`
project/
├── src/              # 源代码
│   ├── module_a/     # 模块A
│   └── module_b/     # 模块B
├── tests/            # 测试代码
│   ├── unit/         # 单元测试
│   └── integration/  # 集成测试
├── docs/             # 文档
├── scripts/          # 脚本工具
└── config/           # 配置文件
\`\`\`
```

### 5. 测试指南

```markdown
## Testing Guidelines

### 测试分类

| 类型 | 目录 | 说明 |
|------|------|------|
| 单元测试 | `tests/unit/` | 独立组件测试 |
| 功能测试 | `tests/functional/` | 组件交互测试 |
| 集成测试 | `tests/integration/` | 外部服务测试 |

### 测试规范

- 单元测试：Mock 外部依赖
- 集成测试：使用真实服务
- 命名规范：`test_[功能]_[场景]_[预期结果]`
```

### 6. 注意事项

```markdown
## Important Considerations

### 添加新功能时

1. 检查现有组件中的类似模式
2. 确保同步和异步版本都实现（如适用）
3. 添加类型注解
4. 编写对应测试

### 常见问题

1. **问题1**: [描述] → 解决方案
2. **问题2**: [描述] → 解决方案

### 性能考虑

- 考虑点1
- 考虑点2
```

---

## 生成流程

当需要为项目创建文档时：

### 步骤 1: 分析项目

```bash
# 查看项目结构
ls -la
tree -L 2 -I 'node_modules|__pycache__|.git|venv'

# 查看包管理文件
cat package.json  # Node.js
cat pyproject.toml  # Python
cat Cargo.toml  # Rust

# 查看现有文档
cat README.md
```

### 步骤 2: 识别关键信息

- 项目类型（Web 应用、CLI 工具、库等）
- 使用的语言和框架
- 包管理器
- 测试框架
- 主要入口点
- 核心模块

### 步骤 3: 生成文档

根据收集的信息，按照上述模板结构生成文档。

### 步骤 4: 放置文档

| 场景 | 文件名 | 位置 |
|------|--------|------|
| Claude Code 项目 | `CLAUDE.md` | 项目根目录 |
| Cursor 项目规则 | `project-guide.mdc` | `.cursor/rules/` |
| 通用 README | `README.md` | 项目根目录 |
| 开发者文档 | `CONTRIBUTING.md` | 项目根目录 |

---

## 示例输出

为一个 Python FastAPI 项目生成的文档：

```markdown
# Project Guide

## Project Overview

用户管理服务，提供用户注册、认证、权限管理等 REST API。

## Development Commands

### 环境设置
\`\`\`bash
# 安装依赖
pip install -r requirements.txt

# 启动数据库
docker-compose up -d postgres redis
\`\`\`

### 运行项目
\`\`\`bash
# 开发模式
uvicorn app.main:app --reload --port 8000

# 生产模式
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
\`\`\`

### 测试
\`\`\`bash
pytest tests/ -v --cov=app
\`\`\`

## Architecture Overview

### 核心组件

1. **API 层** (`app/api/`)
   - REST 端点定义
   - 请求验证

2. **服务层** (`app/services/`)
   - 业务逻辑
   - 外部服务调用

3. **数据层** (`app/models/`)
   - SQLAlchemy 模型
   - Pydantic schemas

### 数据流

\`\`\`
Request → Router → Service → Repository → Database
                                      ↓
Response ← Router ← Service ← Repository
\`\`\`
```

---

## 记住

- **简洁优先**：只写开发者需要知道的
- **可执行**：命令必须能直接复制运行
- **保持更新**：代码变化时同步更新文档
- **面向新人**：假设读者第一次接触项目
