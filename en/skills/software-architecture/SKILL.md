---
name: software-architecture
description: Architecture-decision guidance based on Clean Architecture and DDD. Use ONLY for: (1) cross-module architecture decisions (layer placement of new modules, direction of dependencies); (2) domain-boundary partitioning or aggregate-root design; (3) evaluating soundness of an architecture proposal (e.g. whether to introduce a new abstraction layer). NOT for: everyday single-file coding (follow learned-conventions), code refactoring/cleanup (use kaizen), or Prompt / expert design (use prompt-context-design). Trigger words: architecture design, layering, DDD boundary, Clean Architecture, module partitioning, dependency inversion.
---

# Software Architecture Skill

Quality-centered software development and architecture guidance, based on Clean Architecture and Domain-Driven Design (DDD).

## Code style rules

### General principles

- **Early-return style**: Prefer early returns over nested conditionals for readability
- Avoid duplication by extracting reusable functions/modules
- Split long components/functions (> 80 LOC) into smaller units
- Split files that exceed ~200 LOC
- Prefer arrow functions over function declarations when applicable (JS/TS)

---

## Best practices

### Library-first approach

**Always search existing solutions before writing custom code**

- Check npm/pip for libraries that already solve the problem
- Evaluate existing services/SaaS solutions
- Consider third-party APIs for common features
- Prefer libraries over rolling your own `utils`/`helpers`

**Example**: Use `cockatiel` (JS) or `tenacity` (Python) instead of hand-rolling retry logic.

**When custom code is justified**

- Domain-specific business logic
- Performance-critical path with special requirements
- External dependency adds too much complexity
- Security-sensitive code requiring full control
- Existing solutions were evaluated thoroughly and do not fit

### Architecture & design

**Clean Architecture & DDD principles**

- Use ubiquitous language and domain modeling
- Separate domain entities from infrastructure concerns
- Keep business logic independent from frameworks
- Define clear use cases and keep them isolated

**Naming conventions**

| Avoid | Prefer |
|------|--------|
| `utils`, `helpers`, `common`, `shared` | domain-specific names |
| `processData()` | `OrderCalculator`, `UserAuthenticator` |
| `misc.py` | `invoice_generator.py` |

- Follow bounded-context naming
- Each module should have a single, clear purpose

**Separation of concerns**

- Don’t mix business logic into UI components
- Don’t put DB queries in controllers/handlers
- Maintain clear boundaries between contexts
- Ensure responsibilities are well separated

---

## Anti-pattern checklist

### NIH (Not Invented Here) syndrome

| Don’t | Use |
|------|-----|
| Build custom auth | Auth0/Supabase/Firebase |
| Write your own state management | Redux/Zustand/Pinia |
| Create custom form validation | mature validation libraries |

### Bad architecture choices

- Mixing business logic with UI components
- Querying the database directly in controllers
- Lack of clear separation of concerns

### Generic naming anti-patterns

- `utils.js` with 50 unrelated functions
- `helpers/misc.js` as a dumping ground
- `common/shared.js` with unclear purpose

**Remember**: every line of custom code is debt that must be maintained, tested, and documented.

---

## Code quality

### Error handling

```python
# Good: typed exception handling
try:
    result = process_data(data)
except ValidationError as e:
    logger.error(f"Validation failed: {e}")
    return Result(error=str(e))
except DatabaseError as e:
    logger.error(f"Database error: {e}")
    raise
```

### Function design

- Break complex logic into smaller reusable functions
- Avoid deep nesting (max ~3 levels)
- Keep functions under ~50 LOC when possible
- Keep files under ~200 LOC when possible

### Early-return example

```python
# Bad: deeply nested
def process_user(user):
    if user:
        if user.is_active:
            if user.has_permission:
                do_something()
            else:
                return "No permission"
        else:
            return "User inactive"
    else:
        return "User not found"

# Good: early returns
def process_user(user):
    if not user:
        return "User not found"
    
    if not user.is_active:
        return "User inactive"
    
    if not user.has_permission:
        return "No permission"
    
    do_something()
```

---

## Mistake-proofing with types

### Make string types safer

```typescript
// Bad: string status can be anything
type OrderBad = {
    status: string;  // could be "pending", "PENDING", "pnding", anything!
};

// Good: only valid statuses are possible
type OrderStatus = 'pending' | 'processing' | 'shipped' | 'delivered';
type Order = {
    status: OrderStatus;
};

// Better: statuses carry associated data
type Order =
    | { status: 'pending'; createdAt: Date }
    | { status: 'processing'; startedAt: Date; estimatedCompletion: Date }
    | { status: 'shipped'; trackingNumber: string; shippedAt: Date }
    | { status: 'delivered'; deliveredAt: Date; signature: string };
```

### Validate at the boundary

```python
# Good: validate once at system boundary
def handle_payment_request(request):
    amount = validate_positive(request.body.amount)
    process_payment(amount)

def validate_positive(n: float) -> float:
    if n <= 0:
        raise ValueError("Must be positive")
    return n

def process_payment(amount: float):
    fee = amount * 0.03
```

---

## Mistake-proofing configuration

```python
# Bad: optional config with unsafe defaults
config = {
    "api_key": os.getenv("API_KEY"),  # could be None
    "timeout": 5000,
}

# Good: required config, fail early
def load_config():
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API_KEY env var is required")
    
    return {
        "api_key": api_key,
        "timeout": 5000,
    }

config = load_config()
```

---

## Standardized work

### Follow patterns

```python
class UserAPIClient:
    async def get_user(self, id: str) -> User:
        return await self.fetch(f"/users/{id}")

class OrderAPIClient:
    async def get_order(self, id: str) -> Order:
        return await self.fetch(f"/orders/{id}")
```

Consistency makes the codebase predictable.

### Documentation standard (explain why)

```python
"""
Retry an async operation with exponential backoff.

Why: network requests fail transiently; retries improve reliability
When: external API calls, database ops
When NOT: user input validation, internal pure functions

Example:
    result = await retry(
        lambda: fetch('https://api.example.com/data'),
        max_attempts=3, base_delay=1.0
    )
"""
```

---

## YAGNI (You Aren’t Gonna Need It)

### Good example

```python
def log_error(error):
    print(f"ERROR: {error}")
```

### Bad example

```python
class LogTransport(ABC):
    @abstractmethod
    async def write(self, level, message, meta=None): pass

class ConsoleTransport(LogTransport): ...
class FileTransport(LogTransport): ...
class RemoteTransport(LogTransport): ...

class Logger:
    def __init__(self):
        self.transports = []
        self.queue = []
        self.rate_limiter = RateLimiter()
        # 200 LOC for “maybe”
```

Build for real needs, not imaginary futures.

### When to add complexity

- Current requirements demand it
- Pain points observed through usage
- Measured performance issues
- Multiple use cases emerged

---

## Premature abstraction

```python
# Bad: build a framework for a single use case
class BaseCRUDService(ABC):
    @abstractmethod
    def get_all(self): pass
    @abstractmethod
    def get_by_id(self, id): pass
    @abstractmethod
    def create(self, data): pass

# Good: simple functions for current needs
async def get_users():
    return await db.query("SELECT * FROM users")

async def get_user_by_id(id: str):
    return await db.query("SELECT * FROM users WHERE id = $1", [id])
```

**Rule of three**: Abstract only after the pattern proves itself in 3+ similar cases.

---

## Performance optimization

```python
def filter_active_users(users):
    return [u for u in users if u.is_active]

# Benchmark: 1000 users → 50ms (acceptable) → ship it.
# Later: optimize after profiling shows a bottleneck.
```

Optimize based on measurement, not assumptions.

---

## Remember

**This is about**:
- Continuous small-step improvement
- Preventing errors by design
- Following proven patterns
- Building only what you need

**This is NOT about**:
- Being perfect on the first try
- Massive refactors
- Clever abstractions
- Premature optimization

**Mindset**: Good enough today, better tomorrow. Repeat.
