---
name: design-impl-audit
description: The Design-vs-Implementation Audit Copilot. A universal skill for any project, any language, any design document. Before work starts, it reminds engineers what must be delivered; after code lands, it checks what was actually delivered, what drifted, and what silently went beyond the design. Feed it a design doc plus a Git commit range; it reconciles every design intent / stage / parameter / interaction against real code. Triggers: design audit, implementation audit, delivery review, code acceptance, check code against design doc.
---

# Design-Impl Audit — The Design-vs-Implementation Reconciliation Copilot

## What this skill is (self-introduction)

**In one sentence**: Engineers hold a design document in one hand (intent of truth) and a set of Git commits in the other (delivery of truth). This skill is the **copilot**: **it does not write code for you; it only gate-keeps for you**. Before work starts, it lists "what must land this round" (the **reminder**). After code lands, it reconciles "what actually landed, what drifted" (the **check**). Its output is a **checklist and a report**, never a patch.

**Pain points it solves**:
- Design documents evolve; a single iteration may touch 10+ points across stages and modules—no human remembers them all;
- Engineers easily miss "that one config line tucked in a corner of the doc" or "one interaction branch";
- Code review only sees a local diff and cannot answer "what percentage of the blueprint did we actually deliver?";
- Doc–code drift destroys the baseline of the next iteration and compounds technical debt.

**Position**: Not a decision-maker. Its job is to expose **every point on the design-to-code path that deserves reconciliation**, so humans can see the gap at a glance.

**Scope**: Any language, any size of codebase, as long as you have a design document (Markdown / HTML / text) and Git version control.

---

## Installation (zero code, copy-and-use)

This skill is just **a single SKILL.md file**. Drop it into the skill directory of whichever editor/agent you use—done.

### Prepare

- Create a subfolder under the target directory (recommended name: `design-impl-audit`)
- Copy this `SKILL.md` into it. Installation complete.

### Paths per editor/agent

| Tool | Global (all projects) | Project-local (current project only) |
|---|---|---|
| **Cursor** | `~/.cursor/skills/design-impl-audit/SKILL.md` | `<project>/.cursor/skills/design-impl-audit/SKILL.md` |
| **Claude Code** | `~/.claude/skills/design-impl-audit/SKILL.md` | `<project>/.claude/skills/design-impl-audit/SKILL.md` |
| **Codex CLI** | `~/.codex/skills/design-impl-audit/SKILL.md` | `<project>/.codex/skills/design-impl-audit/SKILL.md` |
| **Other Agent Skills-compatible tools** | Follow that tool's skill-dir convention | Same |

### Verify

After installation, trigger with any of these phrases:
- "Do a design audit for me"
- "Use the design-impl-audit skill on this commit range"
- "Check code against the xxx doc"

The agent will read this SKILL.md and follow the internal flow.

### Runtime requirements

- The agent must be able to read local files (to parse docs), execute `git` commands (to inspect commits), and fetch URLs (for remote docs). Mainstream agent tools (Cursor / Claude Code / Codex, etc.) have all of these by default—**no extra configuration needed**.
- If the design doc lives in a private GitLab/GitHub repo that requires auth, either pull it locally first, or let the agent use a logged-in `gh` / `glab` CLI.

---

## How to use (four typical scenarios)

### Scenario 1: "Give me a landing plan for this iteration"
→ Input: the design doc (freshly finalized or updated).
→ The skill runs **Step 2** of the flow, decomposing the doc into an **acceptance-item checklist** (stage / intent / expectations / doc-ref), **without touching Git**. Engineers use it to split tasks and commits.

### Scenario 2: "I'm done with this batch of commits—audit them"
→ Input: a Git commit range + the design doc.
→ The skill runs **Steps 1→5** end-to-end and produces a **reconciliation report**. Each acceptance item lands in one of four buckets: ✅ / ⚠️ / ❌ / ➕. Each drift item carries a one-line minimum-fix direction.

### Scenario 3: "Before I merge, double-check I didn't miss or drift anything"
→ Input: branch vs. target branch + design doc.
→ Same as Scenario 2, but with extra **safety-net search**: for every ❌ "not implemented" item, the skill first does a **second-round search** (widening `git log` or searching by symbol) to rule out "already done in another commit" false positives—then surfaces only the real risks.

### Scenario 4: "Which is stale, the doc or the code? Reconcile them"
→ Input: design doc + current branch state (or a time window).
→ The skill runs a **bidirectional scan**:
- Forward: every doc clause → is there corresponding code?
- Reverse: every key code addition (new function, new config, new API parameter) → is it in the doc?
→ Output: a **difference matrix** in two columns — "code needs doc update" vs. "doc needs code update". The engineer decides which side to fix.

---

## Runtime inputs (infer first, ask only when necessary)

When the skill is triggered, it **first infers from context / doc / Git whatever it can, and only asks the user for the truly ambiguous bits**. Never re-ask information the user has already stated.

### The three inputs

**Q1. Code range** (except Scenario 1):
- Acceptable forms: commit range `A..B` / a single commit hash / branch-vs-branch / time window + author / explicit file list
- Handling vague descriptions: use `git log --oneline --author=... -30` to list candidates and let the user pick

**Q2. Design document**:
- Local path (md / html / txt / docx, etc.)
- HTTP/HTTPS URL (fetched via WebFetch)
- For private-repo docs requiring auth: ask the user to pull locally first

**Q3. Optional focus**:
- Restrict to a specific module/directory (narrow the scan)
- Report output path (default: project-root `docs/audit-report/YYYY-MM-DD-<doc-name>-design-impl-audit.md`; if the directory does not exist, fall back to `<doc-dir>/audit-YYYY-MM-DD-<doc-name>.md`)

### Auto-arbitration principles (highest to lowest priority)

1. **User's explicit word wins**: anything the user stated in the current or latest message—use it as-is, do not re-ask.
2. **Doc-carried stage-based ruler**: if the doc has explicit stage markers (P1/P2, Stage-1/Stage-2, MVP/Enhanced, v1/v2, Phase A/B, etc.), automatically pick "the stage that corresponds to the current commit timeline" as the **positive ruler**, and set the other stages as **negative overreach checks**. Decide by commit time vs. the doc's delivery cadence.
3. **Auto-filter file list**: from `git log --stat`, automatically drop noise (test-data artifacts, binaries `*.class/*.dex/*.so/*.pyc`, build artifacts `build/ dist/ target/ node_modules/`, lockfiles, IDE configs, one-shot scripts). No need to ask.
4. **Default report path**: see Q3 above.
5. **Ask only when truly uncertain**: e.g., doc path cannot be inferred, or multiple candidate docs. Then merge all questions into **one** AskQuestion call—never across multiple rounds.

### Recap before Step 1

Before entering Step 1, **restate the auto-arbitration result in one paragraph** ("ruler = Stage-1 items; Stage-2 is negative overreach check; file list = 17 after noise filter; report → xxx"). The user sees it at a glance; if it's wrong they stop you immediately. This **replaces** the traditional mandatory confirmation gates—infer where you can, and the user will shout when you're wrong.

---

## Internal flow (5 steps, strict order)

### Step 1. Lock down the code range (Scenarios 2/3/4 only; Scenario 1 skips)
- Run `git log --stat <range>` + `git diff --stat <range>` to get the changed-file list + line counts.
- Auto-filter noise (see the list in the auto-arbitration section).
- **Include the filtered result in the auto-arbitration recap** given to the user. No separate gate; the user can stop you on the spot if something is off.

### Step 2. Parse the design doc → acceptance-item checklist + ruler arbitration
Cut the doc by H1/H2 headings. Each item records:

| Field | Meaning |
|---|---|
| `id` | Section number or self-numbering (§X.Y, D1-1, F-03 — follow whatever scheme the doc already uses) |
| `phase` | Owning stage (if the doc has stages; else empty) |
| `intent` | One-line paraphrase of the design intent |
| `expectations` | Concrete expectations (behavior / parameters / interfaces / interactions) as bullet points |
| `doc_ref` | Anchor or line number in the original doc |

**Ruler auto-arbitration**:
- If the doc has explicit stages: use Step 1's commit time × the doc's delivery cadence to auto-select "positive ruler = the stage this batch should have delivered". Other stages go into **negative overreach check** (presence of an unexpected capability is flagged ⚠️).
- If the doc has no stages: all items are positive rulers.
- The arbitration result goes into the user-facing recap; no separate confirmation gate.

Scenario 1 ends here—hand the checklist to the engineer.

### Step 3. Build the code evidence base
For each file's diff in Step 1, produce a **semantic summary** (never paste raw code), recording:
- File path + function/class name
- What this diff changed (new function / branch edited / parameter retuned / config added)
- New vs. old values for key parameters or thresholds

### Step 4. Reconcile item by item
For every acceptance item from Step 2, look it up in the Step 3 evidence base:

| Status | Criteria | Report handling |
|---|---|---|
| ✅ **Implemented** | Clear code correspondence + parameters/behavior match the doc | Cite code location |
| ⚠️ **Drifted** | Code exists but parameters/boundaries/interactions/error handling disagree with the doc | **State exactly what drifts** + one-line minimum-fix direction |
| ❌ **Missing** | Doc says so, no code trace | In Scenario 3, must run the second-round search first to rule out false positives |
| ➕ **Beyond-doc** | Code changed but doc doesn't cover it | Single-column call-out: please update the doc (main output of Scenario 4) |

### Step 5. Produce the report (write to Q3's path)

**Report design principles**:
- **Gap visible at a glance**: start with a "Key findings" section — one sentence on the 1~2 most critical issues + a status summary table.
- **Design vs. Implementation contrast is the core**: main tables are always three-column ("Design requirement | Actual implementation | Gap / Verdict"). No text-only descriptions.
- **Numbers align with numbers, behavior aligns with behavior**: for drift items, put the doc's concrete values/logic side-by-side with the code's concrete values/logic.
- **Cut the fluff**: no "This change covers..." openers; no long "stage summary" prose; tables first.
- **Code location precise to the line**: `<file>:<line>` (e.g., `MainActivity:528`), never the whole file.

**Template**:

```
# <Doc Name> Design-vs-Implementation Audit

**Code range**: <range>
**Design doc**: <path>
**Ruler**: <auto-arbitration result> | Generated: YYYY-MM-DD

---

## Key findings at a glance

> **<One-sentence summary of the worst 1~2 issues; keywords bolded>**
>
> <Optional: surface the single worst item on its own line>

| Status | Count | Items |
|---|---|---|
| ✅ Delivered as designed | a | <item ids> |
| ⚠️ Drifted | b | <item ids> |
| ❌ Not delivered | c | <item ids> |
| ➕ Beyond-doc patches | d | <item ids> |

---

## 2. Design vs. Implementation (core)

### ✅ Matching items (N)

| Design requirement (doc) | Actual implementation (code) | Verdict |
|---|---|---|
| **<id>**: <doc clause paraphrased> | <file:line + impl summary> | ✅ |

### ⚠️ Drifted items (N)

#### ⚠️ <id>: <title>

| | Design | Implementation | Gap |
|---|---|---|---|
| <dimension 1> | <value/behavior> | <value/behavior> (code location) | <one-line gap> |

**Impact**: <concrete consequence, tied to doc acceptance-item IDs>
**Fix**: <one-line minimum-fix direction>

### ❌ Not-delivered items (N)

#### ❌ <id>: <title>

| Design | Implementation |
|---|---|
| <doc clause> | <"No occurrence of X / Y anywhere" or "only X kept; Y/Z/W missing"> |

**Consequence**: <tied to doc acceptance-item IDs>

---

## 3. Beyond-doc patches (update doc or explicit acceptance required)

| Change | Source commit | Nature |
|---|---|---|

---

## 4. Next-stage overreach check (negative)

Generate this section only when the doc has stages.

| Item | Code evidence | Verdict |
|---|---|---|

---

## 5. References

**Git range**: <git log --oneline list>
**File list** (N files): <grouped by layer>
```

**Non-negotiables**:
- ❌ Prose-only without the side-by-side table → reader has to flip back to the original doc to find "what was designed"
- ❌ Vague words like "partially implemented" — always name exactly which dimension drifts
- ❌ "This audit covers...", "By cross-referencing..." self-introductions in the report opener

---

## Red lines

1. **Infer first, ask last**: do not re-ask information the user stated; auto-arbitrate when the doc has stages; when truly uncertain, batch all questions into one AskQuestion.
2. **Recap after inference**: the auto-arbitration result must be restated to the user in one paragraph (ruler, file list, report path) so the user can stop you on the spot. This replaces traditional confirmation gates.
3. **Facts only**: a drift note must state "the doc says X, the code is Y" concretely. Avoid "might be", "could be".
4. **Minimum-fix direction**: one line (e.g., "revert threshold 0.6 back to the doc's 0.7"). No design-level proposals.
5. **Stop immediately on mismatch**: if the commit theme does not share a single link with the design doc (topic / module / key entity words all miss), stop and ask the user to arbitrate—do not plow through.
6. **Don't mix tasks**: the report does not discuss future roadmap or "refactor suggestions". It answers only one question: "what did we actually deliver this round?"
7. **Report language follows the doc**: Chinese doc → Chinese report; English doc → English report. Keep terminology aligned.

---

## Anti-patterns (forbidden)

- ❌ Re-asking information the user has clearly stated (e.g., the user already gave the doc path; the skill still asks "which doc").
- ❌ Auto-guessing with `git log -20` when the user did not give a Git range.
- ❌ The doc has stage markers, but the skill still asks "which stage to audit"—should auto-arbitrate by commit time.
- ❌ Pasting the full `git diff` into the report context.
- ❌ Concluding "not implemented" without the second-round search (may exist in another commit).
- ❌ Writing the skill's own execution process into the report.
- ❌ Over-scoped recommendations like "suggest introducing design pattern X".
- ❌ Running Git under Scenario 1 (no Git range exists yet at that point).
