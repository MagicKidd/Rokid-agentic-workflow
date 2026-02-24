---
name: prompt-engineering
description: Prompt engineering techniques and patterns. Use when writing agent commands, hooks, skills, subagent prompts, or any LLM interaction: optimizing prompts, improving output reliability, and designing production-grade prompt templates. Trigger words: prompt engineering, prompt, prompt optimization, LLM interaction.
---

# Prompt Engineering Patterns

Advanced prompt engineering techniques to maximize LLM performance, reliability, and controllability.

## Core Capabilities

### 1) Few-shot learning

Teach by showing examples instead of explaining rules. Include 2–5 input/output pairs demonstrating the desired behavior.

**Use when**: You need consistent formatting, a specific reasoning pattern, or robust handling of edge cases.

**Example**:

```markdown
Extract key fields from support tickets:

Input: "Login doesn't work, always getting 403"
Output: {"issue": "authentication", "error_code": "403", "priority": "high"}

Input: "Feature request: add dark mode in settings"
Output: {"issue": "feature_request", "error_code": null, "priority": "low"}

Now process: "Cannot upload files larger than 10MB, it times out"
```

### 2) Chain-of-thought prompting

Ask for step-by-step reasoning before the final answer.

- **Zero-shot**: add “Let’s think step by step”
- **Few-shot**: include example reasoning traces

**Example**:

```markdown
Analyze this bug report and identify the root cause.

Think step by step:
1. What is the expected behavior?
2. What is the actual behavior?
3. What recent change could have caused it?
4. Which components are involved?
5. What is the most likely root cause?

Bug: "After yesterday's cache update deploy, users cannot save drafts"
```

### 3) Prompt optimization workflow

Systematically improve prompts via testing and iteration.

```markdown
V1 (simple): "Summarize this article"
→ Result: inconsistent length, missing key points

V2 (constraints): "Summarize in 3 bullet points"
→ Result: better structure, still misses nuance

V3 (add reasoning): "Identify 3 key findings, then summarize each"
→ Result: consistent, accurate, captures key info
```

### 4) Template systems

Build reusable prompt structures with variables, conditional sections, and modular components.

```python
# Reusable code review template
template = """
Review this {language} code for {focus_area}.

Code:
{code_block}

Provide feedback on:
{checklist}
"""

prompt = template.format(
    language="Python",
    focus_area="security vulnerabilities",
    code_block=user_code,
    checklist="1. SQL injection\n2. XSS risks\n3. Auth issues"
)
```

### 5) System prompt design

Define global behavior and constraints that persist across the conversation.

```markdown
System: You are a senior backend engineer specializing in API design.

Rules:
- Always consider scalability and performance
- Prefer RESTful patterns by default
- Flag security concerns immediately
- Provide Python code examples
- Use early-return style

Response format:
1. Analysis
2. Recommendations
3. Code examples
4. Trade-offs
```

---

## Key Patterns

### Progressive disclosure

Start simple and add complexity only when needed:

1. **Level 1**: direct instruction → "Summarize this article"
2. **Level 2**: add constraints → "Summarize in 3 bullet points, focusing on key findings"
3. **Level 3**: add reasoning → "Read, identify key findings, then summarize in 3 bullets"
4. **Level 4**: add examples → include 2–3 input/output pairs

### Instruction hierarchy

```
[System context] → [Task instruction] → [Examples] → [Input data] → [Output format]
```

### Error recovery

Design prompts to fail gracefully:
- Include fallback instructions
- Ask for confidence scores
- Request alternative explanations when uncertain
- Specify how to represent missing information

---

## Context Window Management

**Principle**: The context window is a shared resource.

Your prompt competes with:
- System prompt
- Conversation history
- Other commands/skills/hooks/metadata
- The actual user request

**Default assumption**: the model is already smart.

Only add context the model truly needs. Challenge every line:
- “Does the model really need this?”
- “Can I assume the model already knows this?”
- “Is this worth the tokens?”

**Good (~50 tokens)**:

```markdown
## Extract PDF text
Using pdfplumber:
```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```
```

**Bad (~150 tokens)**:

```markdown
## Extract PDF text
PDF is a common file format that contains text, images, and other content...
```

---

## Freedom Level Tuning

Match specificity to task brittleness:

| Freedom | When to use | Example |
|--------|-------------|---------|
| **High** (text instructions) | Many approaches work | Code review guidance |
| **Medium** (pseudocode/templates) | Preferred pattern but flexible | Report generation |
| **Low** (exact scripts) | Brittle ops; consistency matters | Database migrations |

---

## Persuasion Principles (for agent prompts)

LLMs respond to similar persuasion levers as humans.

### 1) Authority

- Commanding language: “MUST”, “NEVER”, “ALWAYS”
- Non-negotiable framing: “No exceptions”

```markdown
✅ Wrote code before tests? Delete it. Start over. No exceptions.
❌ If possible, consider writing tests first.
```

### 2) Commitment

- Require explicit declaration: “I am using [skill]”
- Force choices: “Choose A, B, or C”
- Use tracking: Todo checklists

### 3) Social proof

- Universal patterns: “every time”, “always”
- Failure framing: “X without Y = failure”

### 4) Unity

- Collaborative language: “our codebase”, “we”
- Shared goals: quality, speed, safety

---

## Best practices checklist

1. **Be specific**: vague prompts produce inconsistent results
2. **Show, don’t tell**: examples beat explanations
3. **Test broadly**: diverse, representative inputs
4. **Iterate fast**: small changes can have big effects
5. **Monitor performance**: track production metrics
6. **Version control prompts**: treat prompts like code
7. **Document intent**: explain why the prompt is shaped this way

## Common pitfalls

- **Over-engineering**: building complex prompts before trying the simple version
- **Example contamination**: examples that don’t match target tasks
- **Context overflow**: too many examples exceed token limits
- **Ambiguous instructions**: multiple interpretations
- **Ignoring edge cases**: not testing on boundary inputs

---

## Integrating with RAG

```python
prompt = f\"\"\"Given the following context:
{retrieved_context}

{few_shot_examples}

Question: {user_question}

Answer in detail using only the context above. If context is insufficient, state what is missing.\"\"\"
```

## Integrating with verification

```python
prompt = f\"\"\"{main_task_prompt}

After generating a response, verify it meets:
1. Directly answers the question
2. Uses only provided context
3. Cites specific sources
4. Acknowledges uncertainty

If verification fails, revise the response.\"\"\"
```
