---
name: kaizen
description: Continuous-improvement and mistake-proofing methodology (YAGNI / Poka-Yoke / iterative improvement). Use ONLY when: (1) refactoring existing code to remove over-engineering or tech debt; (2) improving existing workflows or pipelines; (3) applying mistake-proofing patterns to prevent known classes of errors. NOT for: greenfield feature development (code directly), architecture-level redesign (use software-architecture), or one-shot bug fixes (use systematic-debugging). Trigger words: continuous improvement, Kaizen, YAGNI, Poka-Yoke, mistake-proofing, eliminate waste, iterative optimization.
---

# Kaizen: Continuous Improvement

Apply a continuous improvement mindset: small iterative improvements, mistake-proofing by design, following established patterns, and avoiding over-engineering.

## Overview

Small improvements, continuously. Prevent errors by design. Follow what works. Build only what you need.

**Core belief**: Many small improvements beat one large change. Prevent errors early rather than fixing them later.

---

## The Four Pillars

### 1) Continuous Improvement (Kaizen)

Small, frequent improvements compound into major gains.

#### Principles

**Incremental over revolutionary**:
- Make the smallest change that improves quality
- One improvement at a time
- Verify after each change before moving on
- Build momentum through small wins

**Always leave the code better**:
- Fix small issues when you see them
- Refactor while working (within scope)
- Update outdated comments
- Delete dead code when found

**Iterative refinement**:
- First pass: make it work
- Second pass: make it clear
- Third pass: make it robust / efficient
- Don’t try to do all three at once

#### Example

```python
# Iteration 1: make it work
def calculate_total(items):
    total = 0
    for item in items:
        total += item.price * item.quantity
    return total

# Iteration 2: make it clear
def calculate_total(items):
    return sum(item.price * item.quantity for item in items)

# Iteration 3: make it robust (add validation)
def calculate_total(items):
    if not items:
        return 0
    
    for item in items:
        if item.price < 0 or item.quantity < 0:
            raise ValueError("价格和数量必须非负")
    
    return sum(item.price * item.quantity for item in items)
```

Each step is complete, tested, and shippable.

---

### 2) Poka-Yoke (Mistake-Proofing)

Design systems that prevent errors at compile-time / design-time, not at runtime.

#### Principles

**Make errors impossible**:
- Use the type system to catch errors
- Let compilers enforce contracts
- Make invalid states unrepresentable
- Catch errors early (before production)

**Design for safety**:
- Fail fast and loudly
- Provide helpful error messages
- Make the correct path obvious
- Make the wrong path hard

#### Mistake-proofing with types

```typescript
// Bad: string status can be anything
type OrderBad = {
    status: string;
};

// Good: only valid statuses are possible
type OrderStatus = 'pending' | 'processing' | 'shipped' | 'delivered';
type Order = {
    status: OrderStatus;
};

// Better: statuses carry associated data
type Order =
    | { status: 'pending'; createdAt: Date }
    | { status: 'shipped'; trackingNumber: string; shippedAt: Date }
    | { status: 'delivered'; deliveredAt: Date };

// Now it’s impossible to have shipped without trackingNumber
```

#### Mistake-proofing with validation

```python
# Bad: validate after use
def process_payment(amount):
    fee = amount * 0.03  # Used before validation!
    if amount <= 0:
        raise ValueError("无效金额")

# Good: validate immediately
def process_payment(amount):
    if amount <= 0:
        raise ValueError("支付金额必须为正")
    if amount > 10000:
        raise ValueError("支付超过允许的最大值")
    
    fee = amount * 0.03
    # ... safe to use now
```

#### Guards and preconditions

```python
# Early returns prevent deeply nested code
def process_user(user):
    if not user:
        logger.error("用户不存在")
        return
    
    if not user.email:
        logger.error("用户邮箱缺失")
        return
    
    if not user.is_active:
        logger.info("用户未激活，跳过")
        return
    
    # Main logic: user is valid + active
    send_email(user.email, "欢迎！")
```

#### Mistake-proofing configuration

```python
# Bad: optional config with unsafe defaults
config = {"timeout": 5000}  # api_key missing!

# Good: required config, fail early
def load_config():
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API_KEY 环境变量必需")
    
    return {"api_key": api_key, "timeout": 5000}

# App fails at startup if config is invalid
config = load_config()
```

---

### 3) Standardized Work

Follow established patterns. Document what works. Make good practices easy to follow.

#### Principles

**Consistency over cleverness**:
- Follow existing codebase patterns
- Don’t reinvent solved problems
- Introduce new patterns only when clearly better
- New patterns require team agreement

**Docs live with the code**:
- `README` for setup and architecture
- `CLAUDE.md` for AI coding norms
- Comments explain “why”, not “what”
- Provide examples for complex patterns

**Automate standards**:
- Linters enforce style
- Type checks enforce contracts
- Tests validate behavior
- CI/CD enforces quality gates

#### Following a pattern

```python
# Existing codebase pattern for API clients
class UserAPIClient:
    async def get_user(self, id: str) -> User:
        return await self.fetch(f"/users/{id}")

# New code follows the same pattern ✓
class OrderAPIClient:
    async def get_order(self, id: str) -> Order:
        return await self.fetch(f"/orders/{id}")

# Don’t introduce a different pattern “because I prefer functions” ✗
async def get_order(id: str) -> Order:
    # Breaks consistency
    pass
```

---

### 4) Just-In-Time (JIT)

Build what you need now. No more, no less. Avoid premature optimization and over-engineering.

#### Principles

**YAGNI (You aren’t gonna need it)**:
- Implement only current requirements
- No “just in case” features
- No “maybe we’ll need this later” code
- Delete speculation

**Simplest viable solution**:
- Start with the direct solution
- Add complexity only when required
- Refactor when requirements evolve
- Don’t predict future requirements

**Optimize after measurement**:
- Don’t optimize prematurely
- Profile before optimizing
- Measure impact of changes
- Accept “good enough” performance

#### YAGNI in practice

```python
# Current requirement: log error to console
def log_error(error):
    print(f"ERROR: {error}")
# Simple and sufficient ✓

# Over-engineering for “future needs” ✗
class LogTransport(ABC):
    @abstractmethod
    async def write(self, level, message): pass

class ConsoleTransport(LogTransport): ...
class FileTransport(LogTransport): ...
class RemoteTransport(LogTransport): ...

class Logger:
    def __init__(self):
        self.transports = []
        self.queue = []
        # 200 lines for “maybe”
```

#### When to add complexity

- Current requirements demand it
- Pain points observed through usage
- Measured performance issues
- Multiple use cases emerged

```python
# Add complexity as requirements evolve
# v1: simple
def format_currency(amount):
    return f"${amount:.2f}"

# v2: support multiple currencies
def format_currency(amount, currency):
    symbols = {"USD": "$", "EUR": "€", "GBP": "£"}
    return f"{symbols[currency]}{amount:.2f}"

# v3: support localization
def format_currency(amount, locale):
    # use locale library...
```

Complexity is only added when needed.

#### Premature abstraction

```python
# Bad: one use case, but build a framework
class BaseCRUDService(ABC):
    @abstractmethod
    def get_all(self): pass
    @abstractmethod
    def get_by_id(self, id): pass
    # ... build an ORM for a single table

# Good: simple function for the current need
async def get_users():
    return await db.query("SELECT * FROM users")

# Rule of three: abstract after a pattern appears in 3+ places
```

#### Performance optimization

```python
# Current: simple approach
def filter_active_users(users):
    return [u for u in users if u.is_active]

# Benchmark: 1000 users → 50ms (acceptable)
# ✓ Ship it, no optimization needed

# Later: after profiling shows bottleneck
# optimize with indexing or caching
```

Optimize based on measurements, not assumptions.

---

## Red Flags

**Violating Kaizen**:
- “I’ll refactor it later” (you won’t)
- Leaving code worse than you found it
- Big-bang rewrites instead of incremental improvements

**Violating Poka-Yoke**:
- “Users should be careful”
- Validate after use, not before
- Optional configuration without validation

**Violating standardized work**:
- “I prefer my own way”
- Not checking existing patterns
- Ignoring project norms

**Violating JIT**:
- “We might need this someday”
- Building frameworks before usage
- Optimizing without measuring

---

## Remember

**Kaizen is about**:
- Continuous small improvements
- Preventing errors by design
- Following proven patterns
- Building only what’s needed

**Kaizen is NOT about**:
- Being perfect on the first try
- Massive refactors
- Clever abstractions
- Premature optimization

**Mindset**: Good enough today, better tomorrow. Repeat.
