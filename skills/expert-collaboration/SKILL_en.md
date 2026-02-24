---
name: expert-collaboration
description: Launch expert collaboration mode, dividing complex tasks among multiple roles. Use when a task requires coordination of experts from multiple domains, each contributing specialized knowledge. Trigger words: expert collaboration, collaborate, multi-role cooperation.
---

# Expert Collaboration

## When to Use

- Task requires cooperation of experts across multiple domains
- No major disagreements exist; differences are only in responsibility and perspective
- Need progressive convergence to produce an executable result
- Dividing and conquering a complex task

## Collaboration Rules

1. Each expert contributes work or suggestions from their respective domain
2. Experts respond to each other, converging progressively
3. **Collaboration mode must be manually specified**, it won't automatically switch from debate
4. Limit the scope of impact, prioritizing small, verifiable steps

## Collaboration Process

### Launch Format

```
Launch **Expert Collaboration**
Roles: [Role 1], [Role 2], ...
Task: [Task to be completed]
```

### Round Structure

**In each round, every expert does:**
1. **Reasoning**: Analyze the current state and next steps
2. **Acting**: Execute or suggest specific operations
3. **Observing**: Evaluate results and prepare for the next round

### Output Format

```markdown
## Round N

### [Role 1]
**Reasoning**: Analysis of current state...
**Acting**: I will handle...
**Observing**: Completion status...

### [Role 2]
**Reasoning**: Based on [Role 1]'s output...
**Acting**: I will add...
**Observing**: Overall progress...
```

## Ending the Collaboration

At least 3 rounds, until all experts reach an agreement:

```markdown
## Collaboration Results

### Contributions
- [Role 1]: Completed...
- [Role 2]: Completed...

### Final Output
[Executable result/plan/code]

### Verification Checklist
- [ ] Checkpoint 1
- [ ] Checkpoint 2
```

## Example

**User**: Use expert collaboration to help me design a user authentication module.

**Response**:

```
Launch **Expert Collaboration**
Roles: System Architect, Full-stack Developer, Test/QA Expert
Task: Design user authentication module

## Round 1

### System Architect
**Reasoning**: Auth module needs to consider security, scalability, and integration.
**Acting**: 
- Select JWT + Refresh Token strategy
- Define API spec: /auth/login, /auth/refresh, /auth/logout
**Observing**: Architecture complete, needs development of implementation details.

### Full-stack Developer
**Reasoning**: Based on the architect's plan, I need to implement the code.
**Acting**: 
- Implement JWT issuing and validation middleware
- Design Token storage strategy (Redis)
**Observing**: Core functionality complete, needs test coverage.

### Test/QA Expert
**Reasoning**: Auth is security-critical and requires comprehensive testing.
**Acting**:
- Design test cases: normal login, token expiry, concurrent refresh
- Security tests: SQL injection, brute-force protection
**Observing**: Test plan complete.

... (Continues for 2-3 rounds to refine) ...

## Collaboration Results
### Final Output
Complete auth module design doc + core code + test cases
```

## Differences from Expert Debate

| Dimension | Expert Collaboration | Expert Debate |
|-----------|----------------------|---------------|
| Premise | No major disagreement | Disagreement exists |
| Goal | Divide work to finish task | Unify strategy |
| Output | Executable result | Decision consensus |
| Process | Individual contribution, progressive convergence | Mutual questioning, pushing to converge |
