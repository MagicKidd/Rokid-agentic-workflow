---
name: community-solution-research
description: Methodology-grade community and technology research tool. Use when you need to find existing solutions, architecture references, or best practices from the web, OSS communities, or technical forums. Trigger words: community research, best practices research, competitor research, "how are others doing it".
---

# Community Solution Research

## Core principle

**"Research with a specific pain point in hand, never search vaguely."**

Before looking outside, you must first translate internal pain points and engineering constraints into technical anchors. The ultimate purpose of external research is to solve **our** problem — not to write an academic survey.

## Execution flow

### Step 1: Extract internal constraints

If the user did not state them explicitly, pull the following from project docs, chat history, or the codebase first (this step is **non-skippable**):

- **Core pain point**: where exactly does our current system fail? (e.g., intent routing latency too high)
- **Engineering constraints**: what objective limits do we have? (e.g., local-only, no heavyweight frameworks, offline-capable)
- **Existing stack**: what are we already running? (e.g., we already have a vector DB deployed)

### Step 2: Build the search strategy

Never use plain natural-language vague queries. Always use multi-dimensional combinations:

- **Architecture & standards**: `[keyword] architecture` / `system design` / `best practices`
- **Production & pitfalls**: `[keyword] in production` / `challenges` / `vs`
- **Real discussions**: `[keyword] reddit` / `stack overflow`
- **OSS ecosystem**: `[keyword] github` / `awesome [keyword]`

Run these high-dimension queries in parallel, not serially.

### Step 3: Filter & cross-validate

Brutally filter every candidate through the Step 1 constraints:

- Does it solve our core pain point?
- Does it violate our engineering constraints? (too heavy / too expensive / needs lots of labeled data / maintenance nightmare?)
- Can it plug into our existing stack, or does it demand a rewrite?

### Step 4: Structured output

Deliver the report in this exact template:

```markdown
## Community Research Report: [Topic]

### 1. Our internal anchors
- **Core pain point**: ...
- **Engineering constraints**: ...
- **Existing stack**: ...

### 2. Community solution landscape
- **Solution A** (e.g., Semantic Router): [one-line principle]
- **Solution B**: [one-line principle]

### 3. Brutal fit comparison

| Candidate | Solves pain point | Violates constraint | Integration cost | Recommendation |
|---|---|---|---|---|
| A | Fully solves latency | None | Very low (reuses existing infra) | ⭐⭐⭐⭐⭐ |
| B | High accuracy | Requires a new heavy dep | High | ⭐⭐ |

### 4. Landing advice & pitfall warnings
- **Conclusion**: Given our current state, strongly recommend [Solution X]
- **Community-reported pitfalls**: per feedback, adopters typically hit [concrete issue]; we should plan for ...
```

## Notes

- Ruthlessly eliminate theoretically advanced but constraint-violating "dragon-slaying" solutions.
- If results are all SEO marketing fluff, immediately append `github` / `issue` / a concrete technical term and re-search.
