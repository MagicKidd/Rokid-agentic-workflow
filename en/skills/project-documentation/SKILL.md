---
name: project-documentation
description: Create structured developer documentation for a project. Use when starting a new project, taking over an existing one, or generating README / CLAUDE.md / developer guides. Trigger words: project documentation, dev guide, CLAUDE.md, project conventions, architecture docs.
---

# Project Documentation Generator

Create structured developer documentation for any project, including overview, dev commands, architecture, testing guide, and important notes.

## Documentation Structure Template

### 1) Project overview

```markdown
## Project Overview

[Project name] is [one sentence describing what it does].

Key features:
- Feature 1
- Feature 2
- Feature 3
```

### 2) Development commands

```markdown
## Development Commands

### Environment setup
```bash
# Install dependencies
[package manager command]

# Env vars
cp .env.example .env
```

### Run the project
```bash
# Dev mode
[dev run command]

# Production mode
[prod run command]
```

### Tests
```bash
# Run all tests
[test command]

# Run a single test
[single test command]
```

### Code quality
```bash
# Lint
[lint command]

# Format
[format command]

# Type-check
[type check command]
```
```

### 3) Architecture overview

```markdown
## Architecture Overview

### Core components

1. **Component A** (`path/to/component_a/`)
   - Responsibility
   - Key classes/functions

2. **Component B** (`path/to/component_b/`)
   - Responsibility
   - Key classes/functions

### Data flow

```
Input → Component A → Component B → Component C → Output
```

### Design patterns

- **Pattern 1**: used for [scenario]
- **Pattern 2**: used for [scenario]
```

### 4) Directory structure

```markdown
## Directory Structure

```
project/
├── src/              # source
│   ├── module_a/     # module A
│   └── module_b/     # module B
├── tests/            # tests
│   ├── unit/         # unit tests
│   └── integration/  # integration tests
├── docs/             # docs
├── scripts/          # tooling scripts
└── config/           # configs
```
```

### 5) Testing guidelines

```markdown
## Testing Guidelines

### Test categories

| Type | Directory | Notes |
|------|----------|------|
| Unit | `tests/unit/` | Isolated component tests |
| Functional | `tests/functional/` | Component interaction tests |
| Integration | `tests/integration/` | Tests with external services |

### Conventions

- Unit tests: mock external dependencies
- Integration tests: use real services
- Naming: `test_<feature>_<scenario>_<expected>`
```

### 6) Important considerations

```markdown
## Important Considerations

### When adding features

1. Check for existing patterns in similar components
2. Ensure sync & async versions exist (if applicable)
3. Add type annotations
4. Write corresponding tests

### Common issues

1. **Issue 1**: [description] → solution
2. **Issue 2**: [description] → solution

### Performance considerations

- Consideration 1
- Consideration 2
```

---

## Generation Workflow

When generating docs for a project:

### Step 1: Analyze the project

```bash
# Inspect structure
ls -la
tree -L 2 -I 'node_modules|__pycache__|.git|venv'

# Inspect package manager files
cat package.json     # Node.js
cat pyproject.toml   # Python
cat Cargo.toml       # Rust

# Inspect existing docs
cat README.md
```

### Step 2: Identify key information

- Project type (web app / CLI / library / service, etc.)
- Language & frameworks
- Package manager
- Test framework
- Main entry points
- Core modules

### Step 3: Generate the documentation

Generate the documentation using the templates above, based on the information gathered.

### Step 4: Place the documentation

| Scenario | Filename | Location |
|---------|----------|----------|
| Claude Code project | `CLAUDE.md` | project root |
| Cursor project rule | `project-guide.mdc` | `.cursor/rules/` |
| General README | `README.md` | project root |
| Contributor guide | `CONTRIBUTING.md` | project root |

---

## Example Output

Docs generated for a Python FastAPI project:

```markdown
# Project Guide

## Project Overview

User management service providing REST APIs for registration, authentication, and permissions.

## Development Commands

### Environment setup
```bash
# Install dependencies
pip install -r requirements.txt

# Start database
docker-compose up -d postgres redis
```

### Run the project
```bash
# Dev mode
uvicorn app.main:app --reload --port 8000

# Production mode
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Tests
```bash
pytest tests/ -v --cov=app
```

## Architecture Overview

### Core components

1. **API layer** (`app/api/`)
   - REST endpoints
   - Request validation

2. **Service layer** (`app/services/`)
   - Business logic
   - External service calls

3. **Data layer** (`app/models/`)
   - SQLAlchemy models
   - Pydantic schemas

### Data flow

```
Request → Router → Service → Repository → Database
                                      ↓
Response ← Router ← Service ← Repository
```
```

---

## Remember

- **Be concise**: only write what developers need
- **Be executable**: commands should be copy-pastable
- **Keep updated**: update docs when code changes
- **Write for newcomers**: assume first-time readers
