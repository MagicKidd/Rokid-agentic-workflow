---
name: test-driven-development
description: Test-driven development (TDD). Before implementing any feature or bugfix, write the test first. Trigger words: TDD, test-driven, write tests first, Red-Green-Refactor.
---

# Test-Driven Development (TDD)

## Overview

Write the test first. Watch it fail. Write the minimum code to make it pass.

**Core principle**: If you never saw the test fail, you don’t know whether it tested the right thing.

**Breaking the letter breaks the spirit.**

## When to use

**Always**:
- New features
- Bug fixes
- Refactors
- Behavior changes

**Exceptions (must ask your human partner)**:
- One-off prototypes
- Generated code
- Pure configuration changes

Thinking “just this once I’ll skip TDD”? Stop. That’s rationalization.

---

## Iron law

```
No production code without a previously failing test.
```

Wrote code before tests? Delete it. Start over.

**No exceptions**:
- Don’t keep it “for reference”
- Don’t “adjust it” while writing tests
- Don’t look at it
- Delete means delete

Start fresh from tests. Period.

---

## Red-Green-Refactor loop

```
RED (write failing test) → verify correct failure → GREEN (minimum code) → verify pass → REFACTOR (clean up) → next
```

### RED — write a failing test

Write the smallest test that demonstrates what should happen.

**Good example**:

```typescript
test('retries failed operation 3 times', async () => {
    let attempts = 0;
    const operation = () => {
        attempts++;
        if (attempts < 3) throw new Error('fail');
        return 'success';
    };

    const result = await retryOperation(operation);

    expect(result).toBe('success');
    expect(attempts).toBe(3);
});
```

Clear name, tests real behavior, one thing.

**Bad example**:

```typescript
test('retry works', async () => {
    const mock = jest.fn()
        .mockRejectedValueOnce(new Error())
        .mockResolvedValueOnce('success');
    await retryOperation(mock);
    expect(mock).toHaveBeenCalledTimes(2);
});
```

Vague name; tests mock behavior instead of the system behavior.

**Requirements**:
- One behavior per test
- Clear name
- Real code (mock only when unavoidable)

### Verify RED — watch it fail

**Mandatory. Never skip.**

```bash
npm test path/to/test.test.ts
# or
pytest path/to/test.py
```

Confirm:
- Test fails (not crashes)
- Failure message matches expectation
- It fails because the feature is missing (not because of typos)

**Test passes?** You are testing existing behavior. Fix the test.

**Test errors?** Fix the error and rerun until it fails for the correct reason.

### GREEN — minimum code

Write the simplest code that makes the test pass.

**Good example**:

```typescript
async function retryOperation<T>(fn: () => Promise<T>): Promise<T> {
    for (let i = 0; i < 3; i++) {
        try {
            return await fn();
        } catch (e) {
            if (i === 2) throw e;
        }
    }
    throw new Error('unreachable');
}
```

Just enough to pass.

**Bad example**:

```typescript
async function retryOperation<T>(
    fn: () => Promise<T>,
    options?: {
        maxRetries?: number;
        backoff?: 'linear' | 'exponential';
        onRetry?: (attempt: number) => void;
    }
): Promise<T> {
    // YAGNI
}
```

Over-engineering.

Do not add extra features, refactor unrelated code, or “improve” beyond what the test demands.

### Verify GREEN — watch it pass

**Mandatory.**

```bash
npm test path/to/test.test.ts
```

Confirm:
- Test passes
- Other tests still pass
- Output is clean (no errors/warnings)

**Test fails?** Fix code, not the test.

**Other tests fail?** Fix them now (you introduced a regression).

### REFACTOR — clean up

Only after GREEN:
- Remove duplication
- Improve naming
- Extract helper functions

Keep tests green. Do not add new behavior.

---

## What good tests look like

| Quality | Good | Bad |
|--------|------|-----|
| **Minimal** | One thing. If the name contains “and”, split it. | `test('validates email and domain and whitespace')` |
| **Clear** | Name describes behavior | `test('test1')` |
| **Shows intent** | Demonstrates expected API | Hides what the code should do |

---

## Why the order matters

**“I’ll add tests later to confirm it works.”**

Tests written later often pass immediately. Immediate pass proves nothing:
- You may test the wrong thing
- You may test implementation instead of behavior
- You may miss edge cases you forgot
- You never saw it catch a bug

Test-first forces you to observe failure, proving the test actually checks something.

**“I already manually tested all edge cases.”**

Manual tests are temporary:
- No record
- Not repeatable after changes
- Easy to forget under pressure

Automated tests are systematic and repeatable.

**“Deleting X hours of work is wasteful.”**

Sunk-cost fallacy. The time is already spent. Your choice now:
- Delete and rewrite with TDD (more time, high confidence)
- Keep it and add tests later (less time, low confidence, likely bugs)

The real waste is shipping code you can’t trust.

---

## Common excuses

| Excuse | Reality |
|-------|---------|
| “Too simple to need tests.” | Simple code breaks too. Tests can take 30 seconds. |
| “I’ll test later.” | Immediate-pass tests prove nothing. |
| “Manual testing is enough.” | Temporary ≠ systematic. |
| “Deleting is waste.” | Keeping unverified code is technical debt. |
| “I’ll keep it as reference.” | You’ll bias the test toward the implementation. Delete means delete. |
| “I need exploration first.” | Fine. Throw away the exploration, then start TDD. |
| “Testing is hard.” | Hard-to-test often means unclear design. Simplify. |
| “TDD slows me down.” | TDD is faster than debugging. Pragmatism = test first. |

---

## Red flags — stop and restart

- Wrote code before tests
- Wrote tests after implementation
- Tests pass immediately
- You can’t explain why a test fails
- “I’ll add tests later”
- Rationalizing “just this once”
- “I already manually tested”
- “The spirit matters more than the form”
- “I already spent X hours, deleting is wasteful”

**All of these mean: delete the code and restart with TDD.**

---

## Example: bug fix

**Bug**: empty email is accepted

**RED**

```python
def test_rejects_empty_email():
    result = submit_form({"email": ""})
    assert result.error == "Email required"
```

**Verify RED**

```bash
$ pytest test_form.py
FAIL: expected 'Email required', got None
```

**GREEN**

```python
def submit_form(data):
    if not data.get("email", "").strip():
        return Result(error="Email required")
    # ...
```

**Verify GREEN**

```bash
$ pytest test_form.py
PASS
```

**REFACTOR**

Extract validation logic if needed (shared across fields), without adding behavior.

---

## Verification checklist

Before claiming “done”:

- [ ] Every new function/method has tests
- [ ] You saw each test fail before implementation
- [ ] Each test failed for the expected reason (missing feature, not typos)
- [ ] You wrote the minimum code to pass each test
- [ ] All tests pass
- [ ] Output is clean (no errors/warnings)
- [ ] Tests use real code (mock only when unavoidable)
- [ ] Edge cases and error paths are covered

Can’t check all boxes? You skipped TDD. Restart.

---

## When you’re stuck

| Problem | Fix |
|--------|-----|
| Don’t know how to test | Write the desired API first. Start with assertions. Ask your human partner. |
| Test is too complex | Design is too complex. Simplify the interface. |
| Must mock everything | Code is too tightly coupled. Use dependency injection. |
| Setup is too large | Extract helpers. Still huge? Simplify design. |

---

## Final rule

```
Production code → tests exist and failed first
Otherwise → not TDD
```

No exceptions without your human partner’s permission.
