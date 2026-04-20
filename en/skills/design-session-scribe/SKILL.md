---
name: design-session-scribe
description: >-
  Real-time scribe for design discussions. During multi-turn design sessions, create and continuously maintain a structured decision document; after every turn, incrementally update core conclusions, eliminate conflicts and stale content; at end of session, output a clean final record and run a missing-items check.
  Prevents attention collapse and memory-compression errors in long discussions.
  Trigger words: design discussion, design session, record discussion, discussion log.
---

# Design Session Scribe

## Core idea

The real danger in long discussions is not "I can't summarize at the end" — it's that **mid-flight, decisions get overwritten, conflicts get ignored, and context silently drifts**.

This skill's strategy: **freeze conclusions into the document at the end of every turn, never wait for a final summary**.
The document is the **Single Source of Truth**; the conversation is scratch paper.

## Activation

Activate when any of the following holds:
1. The user explicitly says "start a design discussion" or uses a trigger word.
2. The conversation naturally enters a design/proposal mode (multi-option tradeoffs, architecture decisions, requirement breakdown).
3. The user says "record this discussion" or "write this down".

## Workflow

### Phase 1: Create the document

Before the discussion formally starts, create the record file.

**Path**: `docs/design-sessions/<topic>-design-session-<YYYY-MM-DD>.md`

**Template**:

```markdown
# <Topic> — Design Session Record

> Created: <YYYY-MM-DD HH:MM>
> Status: 🟡 In progress
> Participants: User, AI assistant

---

## 1. Goal & constraints

### 1.1 Core goal
<!-- The root problem this design must solve -->

### 1.2 Hard constraints
<!-- Non-negotiable limits -->

### 1.3 Soft constraints
<!-- Tradeoffable preferences -->

---

## 2. Key decisions

| # | Item | Conclusion | Rationale | Turn |
|---|------|------------|-----------|------|
<!-- one row per confirmed decision -->

---

## 3. Design proposal

### 3.1 Current proposal
<!-- Latest proposal agreed by both sides -->

### 3.2 Rejected proposals
<!-- Previously considered, now rejected, with reason -->

---

## 4. Open items

- [ ] <!-- Unresolved questions -->

---

## 5. Implementation notes

<!-- Key delivery notes once the proposal is locked -->

---

## Change log
<!-- Auto-maintained -->
| Turn | Time | Summary |
|------|------|---------|
```

After creating, confirm: `"Design session record created at <path>. Every turn's key conclusions will be synced into the document in real time."`

### Phase 2: Incremental updates (after every turn)

When a turn produces any substantive conclusion, **update the document immediately**. Never batch.

#### Update rules

1. **New decision** → append to the decisions table, tag with turn number.
2. **Overturn an old decision** → move the old one into "Rejected proposals" noting which new decision replaced it; write the new decision into the table.
3. **Refinement** → edit the relevant section in place; do not start a new section.
4. **New open item** → append to "Open items".
5. **Resolved open item** → check it off and promote the conclusion into the right section.
6. **Wholesale proposal change** → update "Current proposal"; archive old one into "Rejected proposals".

#### Conflict-resolution priority

```
Latest explicit turn conclusion > earlier turn conclusions > implicit assumptions
```

When new content conflicts with existing content:
- Update the document with the new content as canonical.
- Log the conflict and its resolution in the change log.
- If ambiguous, confirm with the user before writing.

#### Change log entry

Each update appends one line:
```
| R{N} | HH:MM | {one-sentence summary of change} |
```

### Phase 3: Finish & audit

When the discussion ends (user explicitly ends it or conversation naturally wraps):

#### 3a. Close-out

1. Flip status from `🟡 In progress` to `🟢 Completed`.
2. Review "Open items" and flag any still unchecked.
3. Confirm "Current proposal" reflects the final consensus.

#### 3b. Gap check (mandatory)

Run through this checklist and output a report:

```
Gap check:
□ Core goal is clear and has not drifted
□ All hard constraints are reflected in the proposal
□ No discussed conclusion is missing from the document
□ Rejected proposals all carry a rejection reason
□ All open items are either resolved or explicitly deferred
□ Implementation notes cover the key risks
□ Parts of the proposal are self-consistent (no contradictions)
```

If gaps are found, patch them before delivery.

#### 3c. Deliver

Present final path and change stats:
```
Design session complete:
- Document: docs/design-sessions/xxx.md
- Total turns: N
- Key decisions: M
- Rejected proposals: K
```

## Conduct rules

- **Never hold it only in your head — write it to the document**: any substantive conclusion must land in the file; do not rely on conversation context.
- **Granularity: one turn, one update**: do not batch; low per-update cognitive load.
- **Overwrite, do not append**: when a decision changes, edit the row in place; do not leave stale versions in the main body (archive into rejected).
- **Silence does not get written**: undiscussed / unconfirmed assumptions do not land in the document.
- **Self-prompt**: if more than 3 turns pass without an update, proactively check whether a conclusion was missed.
