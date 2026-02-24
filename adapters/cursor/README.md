# Cursor IDE 适配指南

Cursor 原生支持读取 `.cursor/rules/*.mdc`。

## 配置方法

1. 在你的项目根目录创建 `.cursor/rules` 文件夹（如果没有的话）。
2. 将 `agentic-workflow-kit/rules/` 目录下的所有 `.mdc` 文件**复制或软链接**到你的项目中：

```bash
mkdir -p .cursor/rules
cp path/to/agentic-workflow-kit/rules/*.mdc .cursor/rules/
```

或者使用软链接（便于统一更新）：

```bash
mkdir -p .cursor/rules
ln -s path/to/agentic-workflow-kit/rules/new-task-trigger.mdc .cursor/rules/
ln -s path/to/agentic-workflow-kit/rules/new-task-kickoff.mdc .cursor/rules/
```

## 开始使用

打开 Cursor 的 Composer (Cmd/Ctrl + I) 并发送信号：
> "开始做一个新功能..." 
> "启动重构任务..."

Cursor 会自动触发 `new-task-trigger.mdc` 并拉起完整工作流。