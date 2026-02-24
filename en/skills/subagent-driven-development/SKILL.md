---
name: subagent-driven-development
description: Subagent-driven development. Use when executing an implementation plan with independent tasks, or when facing 3+ independent issues that can be investigated separately. Dispatch a fresh subagent per task and perform review between tasks for fast iteration and quality gates. Trigger words: subagent, parallel execution, task dispatch, agent-driven.
---

# Subagent-Driven Development

Create and execute plans by dispatching a fresh subagent per task/problem, and perform code/output review after each task or batch.

**Core idea**: fresh subagent per task + reviews between tasks = high quality, fast iteration.

**Why it helps**:
- Same session (no manual context switching)
- Fresh subagent per task (reduces context pollution)
- Review after tasks (catch issues early)
- Faster iteration (less human intervention between steps)

---

## Supported execution modes

### Sequential execution

Use when tasks are coupled and must be done in order.

**Use when**:
- Tasks are tightly coupled
- Tasks have strict ordering

### Parallel execution

Use when tasks/issues are largely independent (different files, subsystems, bugs).

**Use when**:
- Tasks are mostly independent
- You can do a holistic review after all tasks complete

---

## Sequential execution workflow

### 1) Load the plan

Read the plan file and create all tasks in TodoWrite.

### 2) Execute tasks with subagents

For each task:

**Dispatch a fresh subagent**:

```markdown
Task tool (general purpose):
  description: "Implement task N: [task name]"
  prompt: |
    You are implementing task N from [plan file].

    Read the task carefully. Your job:
    1) Implement exactly what the task specifies
    2) Write tests (use TDD if required)
    3) Verify the implementation
    4) Commit your work
    5) Report back

    Working directory: [dir]

    Report: what you implemented, what you tested, test results, files changed, any issues
```

The subagent returns a work summary.

### 3) Review subagent work

**Dispatch a code review subagent**:

```markdown
Task tool (code-reviewer):
  WHAT_WAS_IMPLEMENTED: [from subagent report]
  PLAN_OR_REQUIREMENTS: task N from [plan file]
  BASE_SHA: [commit before task]
  HEAD_SHA: [current commit]
  DESCRIPTION: [task summary]
```

Review returns: strengths, issues (critical/important/minor), assessment.

### 4) Apply review feedback

**If issues found**:
- Fix critical issues immediately
- Fix important issues before the next task
- Record minor issues for later

**If a follow-up subagent is needed**:

```
"Fix issues from code review: [issue list]"
```

### 5) Mark done, move on

- Mark task as completed in TodoWrite
- Move to next task
- Repeat steps 2–5

### 6) Final review

After all tasks complete, dispatch a final review:
- Review the whole implementation
- Check all plan requirements are satisfied
- Validate overall architecture

---

## Parallel execution workflow

Load plan, review critically, execute tasks in batches, and report at checkpoints for review.

**Core idea**: batched execution with checkpoints for architect-level review.

### Step 1: Load and critique the plan

1. Read the plan file
2. Critically review it — identify risks / gaps
3. If there are concerns: ask the human partner before starting
4. If clear: create TodoWrite and proceed

### Step 2: Execute a batch

**Default: first 3 tasks**

For each task:
1. Mark as `in_progress`
2. Follow steps exactly
3. Run required verification
4. Mark as `completed`

### Step 3: Report

When the batch finishes:
- Show what was implemented
- Show verification outputs
- Say: “Ready for feedback.”

### Step 4: Continue

Based on feedback:
- Apply changes if needed
- Execute the next batch
- Repeat until done

---

## Parallel investigation workflow

A special case of parallel execution: multiple unrelated failures can be investigated independently.

### 1) Identify independent domains

Group failures by domain:
- File A tests: tool approval flow
- File B tests: batch completion behavior
- File C tests: abort functionality

Each domain is independent (fixing approval won’t affect abort tests).

### 2) Create focused agent tasks

Each agent gets:
- **Scope**: a single test file or subsystem
- **Goal**: make those tests pass
- **Constraints**: do not change unrelated code
- **Expected output**: summary of what you found/fixed

### 3) Dispatch in parallel

```python
# In Claude Code / agent environments
Task("Fix agent-tool-abort.test.ts failures")
Task("Fix batch-completion-behavior.test.ts failures")
Task("Fix tool-approval-race-conditions.test.ts failures")
```

### 4) Review and integrate

When agents return:
- Read each summary
- Verify fixes do not conflict
- Run full test suite
- Integrate changes

---

## Agent prompt structure

Good agent prompts are:

1. **Focused** — one clear domain
2. **Self-contained** — enough context to understand the problem
3. **Specific outputs** — what should the agent return?

**Good example**:

```markdown
Fix 3 failing tests in src/agents/agent-tool-abort.test.ts:

1. "should abort tool with partial output capture" - expect message contains 'interrupted at'
2. "should handle mixed completed and aborted tools" - fast tool is aborted rather than completed
3. "should properly track pendingToolCount" - expect 3 results but got 0

This is a timing/race issue. Your tasks:
1) Read the test file and understand what each test asserts
2) Identify the root cause - timing flakiness or real bug?
3) Fix approach:
   - Replace arbitrary timeouts with event-based waiting
   - If it's a product bug, fix abort implementation
   - If behavior changed, update test expectations

Do NOT just increase timeouts — find the real issue.

Return: summary of what you found and what you fixed.
```

---

## Common mistakes

| Wrong | Right |
|------|------|
| **Too broad**: “Fix all tests” | **Specific**: “Fix agent-tool-abort.test.ts” |
| **No context**: “Fix race conditions” | **With context**: include errors and test names |
| **No constraints**: agent refactors everything | **With constraints**: “don’t touch other modules” |
| **Vague output**: “Fix it” | **Specific output**: “return root cause + change summary” |

---

## When NOT to use

- **Related failures**: one fix may address multiple failures — investigate together first
- **Needs full context**: understanding requires the entire system
- **Exploratory debugging**: you don’t know what’s broken yet
- **Shared state**: agents will interfere (editing same files, using same resources)

---

## Verification

After agents return:

1. Read each summary (know what changed)
2. Check for conflicts (did they edit same code?)
3. Run full suite (verify fixes work together)
4. Spot-check (agents can make systematic mistakes)

---

## Red flags

**Never**:
- Skip reviews between tasks
- Continue with critical issues unresolved
- Dispatch multiple implementing subagents on the same files (conflicts)
- Implement without reading the plan tasks

**If a subagent task fails**:
- Dispatch a fix subagent with specific instructions
- Don’t manually patch in the same context (avoid pollution)

---

## When to stop and ask for help

Stop immediately when:
- You hit a blocker in the batch (missing deps, failing tests, unclear instructions)
- The plan has a critical gap that prevents starting
- You don’t understand an instruction
- Verification fails repeatedly

Seek clarification rather than guessing.
