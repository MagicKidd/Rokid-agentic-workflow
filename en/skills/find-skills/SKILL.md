---
name: find-skills
description: "Discover, install, and security-audit skills. Use when you need to find local skills, search for new ones, add third-party skills, or audit skill safety. Trigger words: find skills, search skills, install skill, add skill, skill security audit."
version: 1.1.0
---

# Find Skills — Discovery, Installation, and Security Review

Find locally available skills, search for third-party skills, and install them safely.

## Repository Info

- **Local path**: `~/.cursor/skills/`
- **Remote repo**: `https://github.com/<your-org>/<your-skills-repo>`
- **Branch**: `main`
- **Search log**: `~/.cursor/skills/.search-log.jsonl`

---

## 1) Find Local Skills

### 1.1 List all skills (with trigger descriptions)

Scan all `SKILL.md`, extract the `description` field, and output:

```
Use <skill-path>/SKILL.md — <description>
```

How to run (AI can run on your behalf):

```bash
cd ~/.cursor/skills && find . -name "SKILL.md" -type f | sort | while read f; do
  desc=$(grep -m1 "^description:" "$f" 2>/dev/null | sed 's/^description: *//;s/^"//;s/"$//')
  if [ -n "$desc" ]; then
    echo "Use $f — $desc"
  else
    echo "$f"
  fi
done
```

### 1.2 Keyword search (search content + path)

```bash
PATTERN="keyword"
cd ~/.cursor/skills && {
  grep -E -r -l -- "$PATTERN" --include="SKILL.md" 2>/dev/null || true
  find . -name "SKILL.md" -type f 2>/dev/null | grep -E -- "$PATTERN" 2>/dev/null || true
} | sort -u | while read f; do
  desc=$(grep -m1 "^description:" "$f" 2>/dev/null | sed 's/^description: *//;s/^"//;s/"$//')
  if [ -n "$desc" ]; then
    echo "Use $f — $desc"
  else
    echo "$f"
  fi
done
```

### 1.3 Search log (discover unmet needs)

Every search is recorded to a log so you can track high-frequency queries and “no match” gaps.

```bash
# Record a search (AI should do this each time it searches)
echo "{\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"query\":\"$PATTERN\",\"results\":$COUNT}" \
  >> ~/.cursor/skills/.search-log.jsonl

# View history
cat ~/.cursor/skills/.search-log.jsonl

# Find frequent queries with zero results (signals new skill needs)
grep '"results":0' ~/.cursor/skills/.search-log.jsonl
```

**Why log?** If the same keyword is searched repeatedly but finds nothing, you should create a new skill to cover that need.

### 1.4 Search strategy cheatsheet

| Need | Method |
|------|--------|
| You know the skill name | Read `~/.cursor/skills/<name>/SKILL.md` |
| You know keywords | Use 1.2 (content + path search) |
| Browse everything | Use 1.1 list all (with descriptions) |
| Browse by category | `ls ~/.cursor/skills/` |
| Find gaps | Use 1.3 and look at `results:0` |

---

## 2) Install Third-Party Skills (MUST follow safety process)

### 2.1 Installation principles

1. **Audit one by one** — no blind bulk installs
2. **Only add `SKILL.md` by default** — copy markdown and data files (CSV/JSON/YAML) first
3. **Scripts must be audited** — any executable file (`.py/.sh/.js/.ts`) requires a security scan
4. **Prefer trusted sources** — high-star repos, well-known orgs

### 2.2 Safety checklist (required for every skill)

Before installing any third-party skill, **MUST** check all items:

#### Step 1: Source validation

- [ ] Confirm repo origin (GitHub URL, author/org, stars, forks)
- [ ] Check LICENSE exists
- [ ] Review recent commits for active maintenance
- [ ] Check Issues for security reports

#### Step 2: Content scan

Scan for risky patterns across all files:

```bash
# Scan in a temp directory
grep -r -E \
  "subprocess|os\.system|eval\(|exec\(|requests\.|urllib|shutil\.rm|os\.remove|import socket|curl |wget |rm -rf|sudo |nc |netcat|/dev/tcp|base64\.decode|pickle\.load|__import__|compile\(" \
  /tmp/skill_to_review/ \
  --include="*.py" --include="*.sh" --include="*.js" --include="*.ts"
```

#### Step 3: Risk rating

| Risk | Signals | Handling |
|------|---------|----------|
| **Safe** | Markdown-only (`SKILL.md`), no scripts | Install directly |
| **Low** | Data files (CSV/JSON/YAML) | Inspect data then install |
| **Medium** | Python/Shell scripts | Line-by-line review before deciding |
| **High** | Network calls, file deletion, system calls | Copy only `SKILL.md`, discard scripts |
| **Reject** | Obfuscated code, base64 payloads, pickle | Do not install; warn user |

#### Step 4: Install decision

- **Safe/Low**: copy everything
- **Medium**: copy `SKILL.md` + approved scripts
- **High**: only `SKILL.md` + safe data files
- **Reject**: do not install; output a security report

### 2.3 Standard install flow

```
1. Clone to temp dir     → /tmp/skill_to_review/
2. Run security scan     → follow checklist
3. Produce safety report → communicate rating
4. Install after consent → copy into ~/.cursor/skills/
5. Commit & sync         → git add + commit + push
6. Clean temp dir        → rm -rf /tmp/skill_to_review/
```

### 2.4 Standard commands

```bash
# 1) Clone to temp dir
git clone --depth 1 <repo-url> /tmp/skill_to_review

# 2) Security scan (required)
grep -r -E "subprocess|os\.system|eval\(|exec\(|requests\.|urllib|curl |wget |rm -rf|sudo " \
  /tmp/skill_to_review/ \
  --include="*.py" --include="*.sh" --include="*.js" --include="*.ts"

# 3) If safe, copy `SKILL.md` + data files
mkdir -p ~/.cursor/skills/<skill-name>
cp /tmp/skill_to_review/path/to/SKILL.md ~/.cursor/skills/<skill-name>/

# 4) Commit & sync
cd ~/.cursor/skills && git add -A && \
  git commit -m "feat: add <skill-name> (security-reviewed)" && \
  git push origin main

# 5) Clean up
rm -rf /tmp/skill_to_review
```

---

## 3) Recommended Trusted Sources

| Source | URL | Trust | Notes |
|--------|-----|-------|------|
| **Anthropic official** | `https://github.com/anthropics/skills` | Highest | Official examples |
| **Anthropic Claude Code** | `https://github.com/anthropics/claude-code` | Highest | Official plugin skills |
| **obra/superpowers** | `https://github.com/obra/superpowers-skills` | High | Large, top community set |
| **K-Dense-AI** | `https://github.com/K-Dense-AI/claude-scientific-skills` | High | Science skills |
| **ComposioHQ** | `https://github.com/ComposioHQ/awesome-claude-skills` | Medium | Many scripts; audit required |
| **SkillsMP market** | `https://skillsmp.com/` | Medium | Huge catalog; audit one-by-one |

### Untrusted source signals (reject)

- No LICENSE
- Stars < 10 and no reputable org backing
- Obfuscated scripts or base64 payloads
- Known security issues in Issues without resolution
- Requests you to set API keys/tokens in env vars (credential theft risk)

---

## 4) Create a Custom Skill

### 4.1 Minimal structure

```
skill-name/
└── SKILL.md          # Required: YAML frontmatter + Markdown instructions
```

### 4.2 `SKILL.md` template

```markdown
---
name: skill-name
description: "A concise description of what this skill does and when to use it. Trigger words: keyword1, keyword2."
version: 1.0.0
---

# Skill Name

Short explanation of what the skill is for.

## When to use

- Scenario 1
- Scenario 2

## How to use

[Concrete steps / commands]
```

### 4.3 Sync after creation

```bash
cd ~/.cursor/skills && git add -A && \
  git commit -m "feat: create <skill-name>" && \
  git push origin main
```

---

## 5) Skills Management Norms

### 5.1 Directory structure conventions

Example:

```
~/.cursor/skills/
├── .git/
├── README.md
├── _global_rules/
├── brainstorming/
├── document-skills/
├── expert-collaboration/
├── expert-debate/
├── find-skills/
├── frontend-design/
├── internalized-cognition/
├── kaizen/
├── planning-with-files/
├── project-documentation/
├── prompt-engineering/
├── skill-creator/
├── software-architecture/
├── subagent-driven-development/
├── superpowers/
└── test-driven-development/
```

### 5.2 Always sync after changes

After any add/edit/delete:

```bash
cd ~/.cursor/skills && \
  git add -A && \
  git commit -m "<type>: <message>" && \
  git push origin main
```

Commit types:
- `feat`: new skill
- `fix`: bugfix
- `docs`: documentation
- `refactor`: refactor
- `chore`: maintenance

### 5.3 Restore on a new machine

```bash
git clone https://github.com/<your-org>/<your-skills-repo>.git ~/.cursor/skills
```

---

## 6) Safety Report Template

After installing a third-party skill, output:

```
## Security Review Report

- **Skill name**: xxx
- **Source**: https://github.com/xxx/xxx
- **Stars**: xxx
- **Risk rating**: Safe / Low / Medium / High
- **Scan result**: None found / Found N suspicious patterns
- **Handling**: Full install / Only SKILL.md / Rejected
- **Installed files**: list actual copied files
- **Excluded files**: list excluded files and why
```
