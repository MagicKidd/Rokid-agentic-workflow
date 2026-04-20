---
name: easy-explain
description: Translate technical terms into plain, business-friendly language for non-engineers. Use when users ask "explain in plain language", "in human terms", "I'm not an engineer", or similar. Trigger words: plain language, layman explanation, translate jargon.
---

# Easy Explain

Translate function names, module names, and architecture terms into language a non-engineer can understand instantly.

## Audience

- Non-engineers
- Product / operations / business stakeholders
- Anyone asking for plain language

## Output template (5-part)

Every term is explained using this fixed 5-part structure:

1. **What it is** — one plain-language sentence
2. **Its role in the flow** — why the system needs it
3. **What it takes in** — input in everyday words
4. **What it produces** — output in everyday words
5. **What happens without it** — practical impact or risk

Then append:
- **One-line summary**: 1 sentence
- **Everyday analogy** (optional): only when it clearly aids understanding

## Hard rules

- ❌ Do not assume the reader knows code
- ❌ Do not use unexplained jargon
- ✅ Keep each term concise (5–8 lines)
- ⚠️ If the name is ambiguous, state your assumption explicitly

## Typical trigger phrases

- "Explain in plain language"
- "In human terms, please"
- "I'm not an engineer, I don't get it"
- "Translate this technical term into business language"

## Good example

Term: `intent_summary`

- **What it is**: A one-page concise conclusion of how the user's intent was processed.
- **Its role in the flow**: Gives downstream modules and the frontend a "ready-to-display" unified summary instead of scattered fields.
- **What it takes in**: the detected intent, confidence, supporting evidence, and other intermediate results.
- **What it produces**: a structured summary (e.g., "what the user wants, whether the system judged it valid, suggested next step").
- **What happens without it**: downstream has to assemble results on its own, leading to inconsistent wording.
- **One-line summary**: the step that converts analysis results into a unified report.
