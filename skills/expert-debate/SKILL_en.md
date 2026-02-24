---
name: expert-debate
description: Launch expert debate mode, letting two experts debate over disagreements for three rounds to unify a strategy. Use when there's a split in approaches, unclear paths, or blurred model boundaries. Trigger words: expert debate, debate, disagreement analysis.
---

# Expert Debate

## When to Use

- Two experts hold opposing views on the same issue
- Disagreement on technical approach paths
- Model boundaries or responsibilities are unclear
- Need to unify a strategy or clarify direction

## Debate Rules

1. **Experts DO NOT execute tasks**, they only provide judgments and reasoning
2. Respond to the other's viewpoint each round, driving towards convergence
3. **No code or design artifacts are output during debate**, only summarize consensus and disagreement
4. Execution phase begins only after the debate concludes

## Debate Process

### Launch Format

```
Launch **Expert Debate**
Experts: [Role 1], [Role 2]
Topic: [Issue to be debated]
```

### Three-Round Debate Structure

**Each round includes:**
1. **Judgment**: Stance on the issue
2. **Reasoning**: Evidence supporting the stance
3. **Rebuttal/Support**: Refuting or supporting the opponent's viewpoint

### Output Format

```markdown
## Round N

### [Role 1]
**Judgment**: ...
**Reasoning**: ...
**Response to [Role 2]**: ...

### [Role 2]
**Judgment**: ...
**Reasoning**: ...
**Response to [Role 1]**: ...
```

## Ending the Debate

After the third round, output:

```markdown
## Debate Summary

### Consensus Reached
- Consensus point 1
- Consensus point 2

### Remaining Disagreements
- Disagreement point 1 (needs human decision)

### Recommended Strategy
[Unified strategy or recommended approach]
```

## Example

**User**: Use an expert debate to analyze whether this module should use microservices or a monolithic architecture.

**Response**:

```
Launch **Expert Debate**
Experts: System Architect, Full-stack Developer
Topic: Microservices vs Monolithic Architecture

## Round 1

### System Architect
**Judgment**: Recommend microservices architecture
**Reasoning**: 
- Independent deployment of modules, reduced coupling
- Teams can develop in parallel
- Easy to scale in the future
**Response to Full-stack Developer**: Waiting for opponent's statement

### Full-stack Developer
**Judgment**: Recommend monolithic architecture
**Reasoning**:
- Current team is small, microservices add DevOps overhead
- Early business is uncertain, monolith allows rapid iteration
- Avoid premature optimization
**Response to System Architect**: The benefits of microservices only show up after the team scales.

... (Continues for 2-3 rounds) ...

## Debate Summary
### Consensus Reached
- Adopt modular monolith initially, reserving interfaces for future splitting

### Recommended Strategy
Monolith first, microservices later. Set triggers for splitting (e.g. team > 10 people or module QPS > 1000).
```
