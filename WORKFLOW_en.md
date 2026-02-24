# Agentic Workflow: Structured AI Collaboration

## I. Why do we need a workflow protocol?

When using powerful AI coding assistants (like Cursor, Claude Code), developers often encounter these pain points:
1. **Context Loss**: In a long conversation, the AI can easily drift from the original goal or start generating irrelevant code modifications due to the sheer size of the codebase.
2. **Lack of Discipline**: If given a broad task description, the AI might immediately output massive blocks of code without properly clarifying requirements or respecting existing architecture, leading to over-engineering or subtle bugs.

This protocol aims to guide the AI's behavior in a standardized way. The core idea is:

> **Humans drive the design by providing inputs and making decisions; AI gathers information, provides options, and executes rigorously upon confirmation.**

By introducing distinct Phases and Checkpoints, we turn open-ended chats into a more predictable and structured workflow.

---

## II. Workflow Overview

When you issue a command like _"Start implementing the shopping cart logic"_, the trigger rules guide the conversation through the following phases:

```mermaid
graph TD
    User([User initiates new task]) --> P1
    
    subgraph Phase 1: Context Gathering
        P1[Auto Information Retrieval] --> P1A[Lessons Learned & Docs]
        P1 --> P1B[Code Dependencies & Recent Changes]
    end
    
    P1A & P1B --> P2
    
    subgraph Phase 2 & 3: Summary & Human Decision
        P2[Present Structured Summary] --> P3{Wait for Direction}
        P3 -->|A. Discuss Requirements| C1[In-depth Discussion]
        P3 -->|B. Clear Plan| C2[Create Implementation Plan]
        P3 -->|C. Straightforward| C3[Direct Coding]
        P3 -->|D. Troubleshooting| C4[Systematic Debugging]
    end
    
    subgraph Phase 4: AI Execution (Load Skills as needed)
        C1 --> |Apply Brainstorming Guide| Doc[Finalize Design]
        Doc --> C2
        
        C2 --> |Apply Planning Guide| Plan[Output Step List]
        Plan --> |Support Sub-agents| Exec[Execute Steps]
        
        Exec --> |Request Code Review| Review[Stage Review]
        Review --> |Advocate TDD| Valid[Test & Verify]
        
        C3 --> Valid
        
        C4 --> |Apply Debugging Guide| Fix[Locate & Fix]
        Fix --> Valid
        
        Valid --> Done([Task Completed])
    end
    
    classDef phase fill:#f9f9f9,stroke:#333,stroke-width:2px;
    class P1,P2,P3,Phase4 phase;
```

### Phase 1: Context Gathering
Instead of outputting code immediately, the AI performs a background scan (via file searches or scripts) covering project documentation, related code modules, and even a `lessons.md` file that accumulates past troubleshooting experiences to avoid repeating mistakes.

### Phase 2 & 3: Summary & Human Decision
The AI compiles the gathered information into a summary, outlining its understanding of the current state and constraints. It then asks the human developer how to proceed (e.g., whether to dive into design discussions or to start executing based on an existing plan).

### Phase 4: AI Execution
Once confirmed by the human, the AI automatically loads the appropriate professional knowledge base (Skills) based on the chosen path. For example, if entering troubleshooting mode, it loads the `systematic-debugging` skill, forcing itself to find the root cause before suggesting a fix; if building a new module, it follows the TDD guidelines to write test files first.

---

## III. Introduction to Core Skills

Skills are text references that instruct the AI on how to behave in specific scenarios. They are categorized by function:

### 1. Thinking & Discussion
Guides the AI to ask questions or debate options to help narrow down ideas when requirements are vague.
- **`brainstorming`**: Instructs the AI to ask only one question at a time and provide multiple-choice options instead of long, monolithic responses.
- **`expert-debate`** / **`expert-collaboration`**: Allows the AI to simulate experts with different perspectives to expose risks in a proposed solution.

### 2. Engineering Discipline
Standardizes the AI's code generation process during execution.
- **`kaizen`**: Emphasizes simple iterations and continuous improvement, avoiding over-engineering for hypothetical requirements (YAGNI).
- **`software-architecture`**: Advocates for clear separation of concerns and prioritizing mature existing libraries over writing custom infrastructure code.
- **`test-driven-development`**: Reminds the AI to write test cases to verify expectations before modifying business logic.
- **`planning-with-files`**: When tasks involve many steps, it instructs the AI to maintain an external progress file to prevent memory loss.

### 3. Foundation Practices (Superpowers)
Incorporates the excellent community practice collection (`obra/superpowers`), providing fundamental process guarantees, such as:
- **`verification-before-completion`**: Requires the AI to actively run scripts to check the results before concluding a task.
- **`subagent-driven-development`**: Uses sub-agents to split independent tasks, isolating conversational context.

---

## IV. How to Customize the Workflow

1. **Project-level Rules**: You can place specific technical specification files in your project's `.cursor/rules/` directory. During the Phase 1 scan, the AI will automatically sense these and take your custom constraints into account.
2. **Accumulating Lessons**: If you notice the AI repeatedly making a certain type of mistake during collaboration, you can point it out and have it written into the project's `lessons.md`. This will be automatically referenced as prior knowledge in future tasks.
3. **Writing New Skills**: If you have an internal tool manual or a company-wide UI library development guide, you can add it as plain text to the `skills/` directory and instruct the AI to read it in your daily Prompts.