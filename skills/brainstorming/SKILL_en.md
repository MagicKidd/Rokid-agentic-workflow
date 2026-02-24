---
name: brainstorming
description: Brainstorming design process. Must be used before any creative work - creating features, building components, adding functionality, or modifying behavior. Transforms ideas into complete designs and specifications through collaborative dialogue. Trigger words: brainstorm, design discussion, requirement analysis, explore solutions.
---

# Brainstorming: Transforming Ideas into Designs

## Overview

Help transform ideas into complete designs and specifications through natural, collaborative dialogue.

First, understand the current project context, then refine the idea by asking one question at a time. Once you understand what needs to be built, present the design in small sections (200-300 words), checking for correctness after each section.

---

## Process

### Understanding the Idea

1. **Understand project state first** (files, docs, recent commits)
2. **Ask ONE question at a time** to refine the idea
3. **Use multiple-choice when possible**, open-ended is also fine
4. **Only one question per message** - if the topic requires more exploration, break it into multiple questions
5. **Focus on understanding**: purpose, constraints, success criteria

### Exploring Approaches

1. **Propose 2-3 different approaches** and their trade-offs
2. **Present options conversationally**, with your recommendation and reasoning
3. **State the recommended option first** and explain why

### Presenting the Design

1. Once confident you understand what to build, **present the design**
2. **Break it down into 200-300 word sections**
3. **Ask after each section** if it looks correct
4. **Cover**: architecture, components, data flow, error handling, testing
5. **Be ready to clarify** if anything is unclear

---

## After Design

### Documentation

- Write the validated design to `docs/plans/YYYY-MM-DD-<name>-design.md`
- Commit the design document to git

### Implementation (if proceeding)

- Ask: "Ready to setup the implementation?"
- Create an isolated workspace (if using worktrees)
- Create a detailed implementation plan

---

## Key Principles

| Principle | Description |
|-----------|-------------|
| **One question at a time** | Don't overwhelm the user with multiple questions |
| **Multiple-choice preferred** | Easier to answer than open-ended (when possible) |
| **Ruthless YAGNI** | Remove unnecessary features from all designs |
| **Explore alternatives** | Always propose 2-3 approaches before settling |
| **Incremental validation** | Present design in sections, validate each section |
| **Stay flexible** | Go back for clarification when anything is unclear |

---

## Question Type Examples

### Multiple Choice (Preferred)

```markdown
What is the primary goal of this feature?
A) Improve user experience
B) Enhance performance
C) Add new functionality
D) Fix existing issues
```

### Open-Ended Question

```markdown
Can you describe a typical scenario of a user interacting with this feature?
```

### Confirmation Question

```markdown
So if I understand correctly, the main requirements are:
1. Support multiple languages
2. Response time < 200ms
3. Compatible with existing APIs

What is the priority order for these?
```

---

## Design Presentation Templates

### Section 1: Overview

```markdown
## Design Overview

### Goal
[1-2 sentences describing the problem to solve]

### Approach
[Chosen approach and brief reasoning]

Does this look correct?
```

### Section 2: Architecture

```markdown
## Architecture

### Components
- Component A: [Responsibility]
- Component B: [Responsibility]

### Data Flow
[Brief description of how data flows]

Is this architectural direction right?
```

### Section 3: Interface Design

```markdown
## Interface Design

### API
\`\`\`python
def process_request(input: RequestType) -> ResponseType:
    """
    Process request...
    """
\`\`\`

### Inputs / Outputs
- Input: [Description]
- Output: [Description]

Does the interface design meet the requirements?
```

### Section 4: Error Handling & Testing

```markdown
## Error Handling

### Potential Error Scenarios
1. [Scenario 1]: [Handling strategy]
2. [Scenario 2]: [Handling strategy]

## Testing Strategy

### Key Test Cases
1. [Test Case 1]
2. [Test Case 2]

Do these cover the main scenarios?
```

---

## Approach Comparison Template

```markdown
## Approach Comparison

### Approach A: [Name]
**Pros**:
- [Pro 1]
- [Pro 2]

**Cons**:
- [Con 1]

**Best suited for**: [Description]

### Approach B: [Name]
**Pros**:
- [Pro 1]

**Cons**:
- [Con 1]
- [Con 2]

**Best suited for**: [Description]

### Recommendation
I recommend **Approach A** because [Reasoning].

Which direction do you lean towards?
```

---

## Red Flags

- **Skipping the question phase** and jumping straight into design
- **Asking too many questions at once**
- **Recommending one approach** without providing alternatives
- **Presenting a massive design block** without checking for understanding
- **Ignoring user feedback** and continuing with original plan

---

## Example Conversation

**User**: I want to add a personalized recommendation feature to the museum guide.

**Assistant**:
Sure, let me understand the requirements first.

First, what is the primary scenario for this recommendation feature?
A) Pre-visit - Help users plan their route
B) During visit - Recommend the next exhibit based on current location
C) Post-visit - Recommend related content for deep learning
D) All of the above

**User**: B, recommendations during the visit.

**Assistant**:
Got it, focusing on real-time recommendations during the visit.

What is the primary basis for the recommendations?
A) User's historical preferences
B) Correlation with current exhibit
C) Popularity / other user behavior
D) A combination of the above

**User**: D, a comprehensive combination.

**Assistant**:
Okay, combining multiple signals. Let me confirm my understanding:

Goal: During the user's visit, recommend the next exhibit based on historical preferences, current exhibit correlation, and popularity.

Is this understanding correct? If so, I will propose 2-3 implementation approaches for you to choose from.

---

## Remember

- **Ask questions first**, don't assume requirements
- **One question at a time**, keep the conversation flowing
- **Provide options**, make it easy for the user to answer
- **Present in chunks**, ensure aligned understanding
- **Stay flexible**, adjust direction anytime
