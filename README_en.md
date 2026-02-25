# Agentic Coding Workflow

<p align="center">
  <img src="https://img.shields.io/badge/Agentic-Workflow-blue.svg" alt="Agentic Workflow">
  <img src="https://img.shields.io/badge/AI_Pair_Programming-Cursor_|_Claude-lightgrey.svg" alt="AI Pair Programming">
</p>

<p align="center">
  <b>English</b> | <a href="./README.md">简体中文</a>
</p>

> Exploring practical collaboration patterns to help AI coding assistants maintain context and execution discipline in daily development.

In everyday engineering practices, the team (Jing, et al.) noticed that when using AI coding assistants (like Cursor, Claude Code) for complex tasks, the AI often loses context over long conversations or rushes into coding without sufficient design. This leads to over-engineering or subtle bugs.

**Agentic Coding Workflow** is an AI collaboration protocol designed for developers. By utilizing predefined routing rules (Rules) and professional skill packs (Skills), it breaks down tasks into structured steps—from context gathering and architectural design, to coding and automated verification—making the AI collaboration process more predictable, transparent, and disciplined.

## 📖 Table of Contents
- [Core Concepts](#-core-concepts)
- [Quick Start](#-quick-start)
- [Directory Structure](#-directory-structure)
- [Basic Usage](#-basic-usage)
- [License & Acknowledgements](#-license--acknowledgements)

---

## 💡 Core Concepts

- **Mitigating Context Loss**: Through automated information retrieval (Phase 1), the AI scans related code, architectural documents, and past troubleshooting records right at the beginning of the conversation to establish a solid baseline.
- **Auto-Learning Project Conventions**: Bundled dynamic context scripts allow AI to distill naming, typing, logging, and error-handling patterns directly from your codebase, turning them into actionable rules to prevent generating inconsistent "slop" code.
- **Enforcing Engineering Discipline**: "Decision points" (Phase 2 & 3) are introduced before any code is written. Only after the approach is confirmed by the human will the AI be authorized to load professional skills like TDD or multi-step planning (Phase 4) for standardized development.
- **Verification First**: The AI is strictly required to provide evidence of passing tests or successful execution before claiming a defect is fixed or a task is completed.

👉 **[Click here for detailed workflow concepts & architecture (WORKFLOW_en.md)](./WORKFLOW_en.md)**

---

## ⚡ Quick Start

Regardless of which AI coding tool you use, this pure Markdown-based methodology is relatively straightforward to integrate into your workspace.

### 1. Get the Toolkit

Clone this repository to your local machine. To include the `superpowers` submodule (which provides core foundational dependencies), use the `--recursive` flag:

```bash
# Recommended to place in a global, reusable directory
mkdir -p ~/.cursor/skills
cd ~/.cursor/skills
git clone --recursive https://github.com/MagicKidd/Rokid-agentcode.git .
```

### 2. IDE Integration

Depending on the AI IDE you use daily, choose the corresponding setup method:

#### 🔹 For Cursor Users
Cursor natively supports reading `.mdc` rules from the `.cursor/rules` directory in your project.

1. Run the following in your project root:
```bash
mkdir -p .cursor/rules
# Use symlinks to easily keep your workflow updated across projects
ln -s ~/.cursor/skills/en/rules/ai-coding-protocol.mdc .cursor/rules/
ln -s ~/.cursor/skills/en/rules/new-task-trigger.mdc .cursor/rules/
ln -s ~/.cursor/skills/en/rules/new-task-kickoff.mdc .cursor/rules/
```
2. Open Cursor's Composer and simply type: "Start working on a new feature...". The trigger will automatically intercept the prompt and guide the step-by-step process.
*(See [adapters/cursor/README.md](adapters/cursor/README.md) for more details)*

#### 🔹 For Claude Code Users
Claude Code relies on a `CLAUDE.md` file in the project root to load system-level context.

1. Copy `adapters/claude-code/CLAUDE.md` to your project root.
2. Edit `CLAUDE.md` and replace `<path-to-agentic-coding-workflow>` with the absolute path where you cloned this repository.
3. Run `claude` and issue a task. Claude will automatically read the specified Skills and follow the protocol.

#### 🔹 For OpenCode and Others
Similarly, copy `adapters/opencode/AGENTS.md` to your project root and update the absolute paths.

---

## 📦 Directory Structure

```text
agentic-coding-workflow/
├── zh/                     # Chinese rules and skills
│   ├── rules/
│   └── skills/
├── en/                     # English rules and skills
│   ├── rules/              # Routing rules
│   └── skills/             # Core skills library
├── superpowers/            # [Recommended dependency] obra/superpowers excellent community practices
├── templates/              # Reusable templates (e.g., project-specific rules, lessons learned)
├── adapters/               # IDE integration guides (Cursor / Claude Code / OpenCode)
├── README_en.md            # This document
└── WORKFLOW_en.md          # Detailed workflow design
```

---

## 🛠️ Basic Usage

Once configured, when you need the AI to assist with development, you don't need to provide lengthy background information. You can start with a simple prompt:

> **"Start refactoring the user authentication module"** or **"Initiate new task: add export functionality"**

Constrained by the protocol, the AI will break the work into several phases:
1. **Auto Context Gathering (Phase 1)**: Retrieves related code, architecture docs, and past troubleshooting records in the background.
2. **Report & Decision (Phase 2 & 3)**: Summarizes the context it found and asks for your decision (e.g., whether to dive into design discussions regarding edge cases, or to start coding immediately).
3. **Step-by-Step Execution (Phase 4)**: Once you confirm the approach, the AI loads the appropriate development skills (such as TDD, multi-step planning) to begin coding systematically.

---

## 📜 License & Acknowledgements

This project is open-source. Contributions are welcome.

In building this workflow, we referenced and learned from excellent practices in the open-source community. Special thanks to [@obra](https://github.com/obra/superpowers-skills) for the `superpowers` collection, which contains highly valuable foundational engineering disciplines. The `superpowers` directory in this repository is included as a Git Submodule, and its copyright belongs to the original author.