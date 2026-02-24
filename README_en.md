# Agentic Coding Workflow

English | [简体中文](./README.md)

> Exploring practical collaboration patterns to help AI coding assistants maintain context and execution discipline in daily development.

Agentic Coding Workflow is an AI collaboration protocol designed for developers. In everyday engineering practices at Rokid, the team (Jing, et al.) noticed that AI coding assistants (like Cursor, Claude Code) often lose context during complex tasks or rush into coding without sufficient design. To mitigate this, we organized this workflow.

By using predefined routing rules (Rules) and professional skill packs (Skills), it breaks down tasks into structured steps—from context gathering and architectural design, to coding and automated verification—making the AI collaboration process more predictable and disciplined.

For details, see: [👉 Workflow Concepts & Architecture (WORKFLOW_en.md)](./WORKFLOW_en.md)

---

## 📦 Directory Structure

```text
agentic-coding-workflow/
├── rules/                  # Routing rules (intercept task commands and guide execution)
├── skills/                 # Core skills library (requirements analysis, TDD, etc.)
├── superpowers/            # [Recommended dependency] obra/superpowers excellent community practices
├── templates/              # Reusable templates (e.g., project-specific rules, lessons learned)
├── adapters/               # IDE integration guides (Cursor / Claude Code / OpenCode)
├── README_en.md            # This document
└── WORKFLOW_en.md          # Detailed workflow design
```

---

## ⚡ Quick Start

Regardless of which AI coding tool you use, this pure Markdown-based methodology is relatively straightforward to integrate.

### 1. Get the Toolkit

Clone this repository to your local machine. To include the `superpowers` submodule, use the `--recursive` flag:

```bash
# Recommended to place in a global, reusable directory
mkdir -p ~/.cursor/skills_shared
cd ~/.cursor/skills_shared
git clone --recursive https://github.com/Rokid/agentic-coding-workflow.git
```

### 2. IDE Integration

Depending on the AI IDE you use daily, choose the corresponding setup method:

#### 🔹 For Cursor Users
Cursor natively supports reading `.mdc` rules from the `.cursor/rules` directory in your project.

1. Run the following in your project root:
```bash
mkdir -p .cursor/rules
# Use symlinks to easily keep your workflow updated across projects
ln -s ~/.cursor/skills_shared/agentic-coding-workflow/rules/new-task-trigger.mdc .cursor/rules/
ln -s ~/.cursor/skills_shared/agentic-coding-workflow/rules/new-task-kickoff.mdc .cursor/rules/
```
2. Open Cursor's Composer and simply type: "Start working on a new feature...". The trigger will automatically guide the step-by-step process.
*(See [adapters/cursor/README.md](adapters/cursor/README.md) for more details)*

#### 🔹 For Claude Code Users
Claude Code relies on a `CLAUDE.md` file in the project root to load system-level context.

1. Copy `adapters/claude-code/CLAUDE.md` to your project root.
2. Edit `CLAUDE.md` and replace `<path-to-agentic-coding-workflow>` with the absolute path where you cloned this repository.
3. Run `claude` and issue a task. Claude will automatically read the specified Skills and follow the protocol.

#### 🔹 For OpenCode and Others
Similarly, copy `adapters/opencode/AGENTS.md` to your project root and update the absolute paths.

---

## 🛠️ Basic Usage

Once configured, when you need the AI to assist with development, you can start with a simple prompt:

> **"Start refactoring the user authentication module"** or **"Initiate new task: add export functionality"**

The AI will follow the rules and break the process into phases:
1. **Auto Context Gathering (Phase 1)**: Retrieves related code, architecture docs, and past troubleshooting records in the background.
2. **Report & Decision (Phase 2 & 3)**: Summarizes the context it found and asks for your decision (e.g., whether to dive into design discussions or start coding immediately).
3. **Step-by-Step Execution (Phase 4)**: Once you confirm the approach, the AI loads the appropriate development skills (such as TDD, multi-step planning) to begin coding.

---

## 🌟 Core Practices

- **Verify Before Confirming**: Demand evidence of passing tests before claiming a defect is fixed.
- **Test-Driven Development (TDD)**: Advocate writing failing test cases before writing business logic.
- **Task Decomposition**: For complex tasks, encourage managing progress through an external file (`task_plan.md`) or dispatching sub-agents to handle independent tasks in parallel, preventing context overload in a single chat.

## 📜 License & Acknowledgements

This project is open-source. Contributions are welcome.

In building this workflow, we referenced and learned from excellent practices in the open-source community. Special thanks to [@obra](https://github.com/obra/superpowers-skills) for the `superpowers` collection, which contains highly valuable foundational engineering disciplines. The `superpowers` directory in this repository is included as a Git Submodule, and its copyright belongs to the original author.