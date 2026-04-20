---
name: mergeable-feature-dev
description: For new-module development or cross-module refactors, enforce separation of scaffolding from deliverables so that "locally standalone runnable" and "low-cost mergeable into the trunk" hold simultaneously. Trigger words: mergeable, low-cost handoff, standalone run, scaffolding, deliverable layer, refactor merge.
---

# Mergeable Feature Dev

Resolves the tension between:

- local dev needs to run standalone (fast iteration)
- main repo merge needs minimal diff (low risk)

Core method: **integration-boundary scan first + two-layer directory isolation + single-purpose PRs**.

---

## When to use

Use if any of:

1. Building a new module / subsystem
2. Cross-module refactor
3. User explicitly demands "mergeable directly, cheap to hand off"
4. You realize the change touches online + training / scripts / demo simultaneously

Not for:

- Single-file patches
- Small bug fixes
- Pure documentation tasks

---

## Flow

### Step 1: Integration-boundary scan (before coding)

Scan and list four things:

1. **Existing abstractions that must be reused**
2. **Capabilities forbidden to rewrite**
3. **Deliverable interface (externally exposed) definition**
4. **Boundary items needing human confirmation**

Recommended scan paths (replace with your project's layout):

- `src/<project>/component/`
- `src/<project>/config/`
- `src/<project>/vo/`
- sibling directories of the target module

Search templates (project-wide + intra-module duplicate detection):

```bash
# project-wide: existing shared capabilities
rg "yaml.safe_load|get_embedding|Logger\(__name__\)|Result\.(success|failed)" src

# intra-module: duplicated defs across files in the new module
rg "^def |^class " src/<project>/<new_module>/ --no-heading | sort -t: -k2 | uniq -d -f1
```

### Step 2: Two-layer directory init

```text
feature_module/
  ├── __init__.py
  ├── core_logic.py
  ├── config.py
  └── _standalone/
      ├── __init__.py
      ├── mock_xxx.py
      ├── demo_server.py
      └── test_local.py
```

Hard constraints:

- Deliverable layer must NOT `import _standalone`
- Deliverable layer must NOT contain inline fallbacks (`try: import X except: mock`)
- `_standalone/` must be in `.gitignore`
- Scaffolding code does NOT enter the first merge PR

### Step 3: Isolate local capabilities via DI

Python template:

```python
from typing import Any, Callable, Optional


class FeatureService:
    def __init__(
        self,
        storage: Optional[Any] = None,
        embed_fn: Optional[Callable[..., Any]] = None,
    ):
        self.storage = storage or existing_project_storage
        self.embed_fn = embed_fn or existing_project_embed_fn
```

Scaffolding injects mocks inside `_standalone` only:

```python
service = FeatureService(
    storage=LocalMockStorage(),
    embed_fn=local_mock_embed,
)
```

### Step 4: Extract a shared core to kill duplicated branches

When two methods differ only in "data source":

**Anti-example** (`validate` and `validate_on_collection` are ~60 lines each and nearly identical):

```python
# BAD: 60 lines duplicated, only matcher call differs
async def validate(self, golden_path): ...
async def validate_on_collection(self, collection, golden_path): ...
```

**Correct template**:

```python
async def _run_validation(
    self, match_fn: Callable[[str], Awaitable[MatchResult]], golden_path: Path
) -> ValidationResult:
    """Shared core: iterate cases, aggregate, return result."""
    payload = self._load_cases(Path(golden_path))
    # ... shared iteration + aggregation ...
    return ValidationResult(...)

async def validate(self, golden_path=config.GOLDEN_TEST_PATH):
    return await self._run_validation(self.matcher.match, golden_path)

async def validate_on_collection(self, collection, golden_path=config.GOLDEN_TEST_PATH):
    match_fn = lambda text: self.matcher.match_with_collection(text=text, collection=collection)
    return await self._run_validation(match_fn, golden_path)
```

### Step 5: PR-split decision tree

```text
Does the change touch online + offline + scripts + docs at the same time?
  yes -> split PRs
         PR1: online hot path (directly mergeable)
         PR2: training / calibration pipeline
         PR3: scripts & reports
         PR4: docs & ops SOP
  no  -> single PR, but keep a single concern
```

---

## Pre-commit checklist (all must pass)

- [ ] Deliverable layer has no `_standalone` dependency
- [ ] Deliverable layer has no inline fallbacks (`try: import X except: mock`)
- [ ] No duplicated implementation (YAML / embedding / logger / Result)
- [ ] No intra-module cross-file duplication in the new module
- [ ] `FORCE_*` flags default to `False`
- [ ] Commit has a single concern
- [ ] Diff is reviewable (suggest net < 500 lines)

---

## Common pitfalls

1. Writing mocks / scripts into the deliverable layer just to run locally.
2. Shipping online logic and training scripts together, producing review noise.
3. Rewriting utilities the project already has (YAML loader, response wrapper, etc.).
4. Defaulting experimental flags to on (`FORCE_* = True`).
5. Writing `try: import pymilvus except: class FakeXxx` in deliverable files — that bakes scaffolding into deliverables.
6. Two files in the new module each defining the same helper (e.g., `_normalize_vector`) — intra-module duplication.
7. Two methods differing only in "data source" arg get copy-pasted wholesale instead of extracting a shared core.

---

## Output requirement

When invoking this skill, produce first:

1. Integration-boundary list (four items)
2. PR-split proposal (by concern)
3. Deliverable-files vs. scaffolding-files list

Then start coding.
