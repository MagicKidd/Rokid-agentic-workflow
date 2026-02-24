"""
Generate dynamic project context for AI coding agents.

Outputs (auto-generated):
  - .agent-context/conventions.md
  - .agent-context/project-context.md
  - .agent-context/metadata.json
  - .cursor/rules/learned-conventions.mdc

Design goals:
  - Deterministic and reproducible
  - Project-agnostic (portable to any repository)
  - Preserve manual notes section on refresh
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


MANUAL_START = "<!-- MANUAL_NOTES_START -->"
MANUAL_END = "<!-- MANUAL_NOTES_END -->"

_CJK_RE = re.compile(r"[\u4e00-\u9fff]")


@dataclass(frozen=True)
class FunctionStat:
    total: int
    fully_typed: int
    async_total: int


@dataclass(frozen=True)
class ScanResult:
    src_files: tuple[Path, ...]
    test_files: tuple[Path, ...]
    py_files: tuple[Path, ...]
    naming_classes: tuple[str, ...]
    naming_functions: tuple[str, ...]
    naming_constants: tuple[str, ...]
    function_stat: FunctionStat
    import_order_score: float
    logger_factory_count: int
    std_logging_count: int
    print_count: int
    asyncio_gather_count: int
    asyncio_create_task_count: int
    await_count: int
    except_exception_count: int
    parametrize_count: int
    type_old_style: int
    type_new_style: int
    docstring_total: int
    docstring_chinese: int
    docstring_google: int
    comment_total: int
    comment_chinese: int
    module_singletons: tuple[tuple[str, str], ...]


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _iter_py_files(base: Path) -> list[Path]:
    if not base.exists():
        return []
    bad_parts = {".venv", "venv", "__pycache__", "node_modules", ".git"}
    out: list[Path] = []
    for p in base.rglob("*.py"):
        if any(part in bad_parts for part in p.parts):
            continue
        out.append(p)
    return sorted(out)


def _resolve_scan_roots(root: Path) -> tuple[list[Path], list[Path]]:
    src_roots: list[Path] = []
    test_roots: list[Path] = []

    for cand in ("src", "app", "lib"):
        p = root / cand
        if p.exists():
            src_roots.append(p)
            break

    if (root / "tests").exists():
        test_roots.append(root / "tests")
    elif (root / "test").exists():
        test_roots.append(root / "test")

    return src_roots, test_roots


def _parse_ast(path: Path) -> ast.AST | None:
    try:
        return ast.parse(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _uniq(values: list[str], limit: int = 8) -> tuple[str, ...]:
    out: list[str] = []
    seen: set[str] = set()
    for v in values:
        if v not in seen:
            out.append(v)
            seen.add(v)
        if len(out) >= limit:
            break
    return tuple(out)


def _extract_naming(py_files: list[Path]) -> tuple[tuple[str, ...], tuple[str, ...], tuple[str, ...]]:
    classes: list[str] = []
    functions: list[str] = []
    constants: list[str] = []

    for path in py_files:
        tree = _parse_ast(path)
        if tree is None:
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                classes.append(node.name)
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                functions.append(node.name)

        for node in getattr(tree, "body", []):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id.isupper():
                        constants.append(target.id)

    return _uniq(classes), _uniq(functions), _uniq(constants)


def _function_stats(py_files: list[Path]) -> FunctionStat:
    total = 0
    fully_typed = 0
    async_total = 0

    for path in py_files:
        tree = _parse_ast(path)
        if tree is None:
            continue
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                total += 1
                if isinstance(node, ast.AsyncFunctionDef):
                    async_total += 1
                args = (
                    list(node.args.posonlyargs)
                    + list(node.args.args)
                    + list(node.args.kwonlyargs)
                )
                all_args_typed = all(a.annotation is not None or a.arg == "self" for a in args)
                return_typed = node.returns is not None
                if all_args_typed and return_typed:
                    fully_typed += 1

    return FunctionStat(total=total, fully_typed=fully_typed, async_total=async_total)


def _import_category(mod: str) -> int:
    if mod == "__future__":
        return 0
    root = mod.split(".")[0]
    if root in sys.stdlib_module_names:
        return 0
    return 1


def _import_order_score(py_files: list[Path]) -> float:
    checked = 0
    ordered = 0
    for path in py_files:
        categories: list[int] = []
        for line in path.read_text(encoding="utf-8").splitlines():
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            if s.startswith("from ") and " import " in s:
                mod = s[5:].split(" import ", 1)[0].strip()
                categories.append(_import_category(mod))
                continue
            if s.startswith("import "):
                mod = s[7:].split(",", 1)[0].strip()
                categories.append(_import_category(mod))
                continue
            break
        if not categories:
            continue
        checked += 1
        if categories == sorted(categories):
            ordered += 1
    return round((ordered / checked * 100.0), 1) if checked else 0.0


def _count_regex(py_files: list[Path], pattern: str) -> int:
    r = re.compile(pattern)
    count = 0
    for path in py_files:
        count += len(r.findall(path.read_text(encoding="utf-8")))
    return count


def _count_ast(py_files: list[Path], node_type: type[ast.AST]) -> int:
    count = 0
    for path in py_files:
        tree = _parse_ast(path)
        if tree is None:
            continue
        for node in ast.walk(tree):
            if isinstance(node, node_type):
                count += 1
    return count


_FRAMEWORK_CLASSES = frozenset({"FastAPI", "APIRouter", "Compiler", "ArgumentParser", "Path"})


def _detect_module_singletons(py_files: list[Path]) -> tuple[tuple[str, str], ...]:
    pairs: list[tuple[str, str]] = []
    for path in py_files:
        tree = _parse_ast(path)
        if tree is None:
            continue
        for node in getattr(tree, "body", []):
            if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.value, ast.Call):
                t = node.targets[0]
                if not isinstance(t, ast.Name):
                    continue
                if t.id.startswith("_") or t.id.isupper() or t.id == "logger":
                    continue
                func = node.value.func
                cls = ""
                if isinstance(func, ast.Name):
                    cls = func.id
                elif isinstance(func, ast.Attribute):
                    cls = func.attr
                if cls and cls[0].isupper() and cls not in _FRAMEWORK_CLASSES:
                    pairs.append((t.id, cls))
    out: list[tuple[str, str]] = []
    seen: set[str] = set()
    for inst, cls in pairs:
        if inst not in seen:
            out.append((inst, cls))
            seen.add(inst)
        if len(out) >= 10:
            break
    return tuple(out)


def _docstring_stats(py_files: list[Path]) -> tuple[int, int, int]:
    total = 0
    chinese = 0
    google = 0
    for path in py_files:
        tree = _parse_ast(path)
        if tree is None:
            continue
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                ds = ast.get_docstring(node)
                if not ds:
                    continue
                total += 1
                if _CJK_RE.search(ds):
                    chinese += 1
                if "Args:" in ds or "Returns:" in ds or "Yields:" in ds:
                    google += 1
    return total, chinese, google


def _comment_lang(py_files: list[Path]) -> tuple[int, int]:
    total = 0
    chinese = 0
    for path in py_files:
        for line in path.read_text(encoding="utf-8").splitlines():
            s = line.strip()
            if s.startswith("#"):
                total += 1
                if _CJK_RE.search(s):
                    chinese += 1
    return total, chinese


def _extract_manual_notes(path: Path, default_text: str) -> str:
    if not path.exists():
        return default_text
    text = path.read_text(encoding="utf-8")
    if MANUAL_START not in text or MANUAL_END not in text:
        return default_text
    start = text.index(MANUAL_START) + len(MANUAL_START)
    end = text.index(MANUAL_END)
    return text[start:end].strip("\n")


def _run_git(root: Path, args: list[str]) -> str:
    try:
        out = subprocess.check_output(["git", *args], cwd=root, stderr=subprocess.DEVNULL)
        return out.decode("utf-8").strip()
    except Exception:
        return ""


def _project_tree(root: Path) -> str:
    entries: list[str] = []
    for p in sorted(root.iterdir()):
        if p.name.startswith(".git"):
            continue
        entries.append(f"- {p.name}/" if p.is_dir() else f"- {p.name}")
    return "\n".join(entries[:60])


def _safe_pct(num: int, den: int) -> str:
    return "0.0%" if den <= 0 else f"{(num / den) * 100:.1f}%"


def _scan(root: Path) -> ScanResult:
    src_roots, test_roots = _resolve_scan_roots(root)
    src_files: list[Path] = []
    test_files: list[Path] = []
    for r in src_roots:
        src_files.extend(_iter_py_files(r))
    for r in test_roots:
        test_files.extend(_iter_py_files(r))

    py_files = sorted(src_files + test_files)

    classes, funcs, consts = _extract_naming(py_files)
    fstat = _function_stats(py_files)

    type_old = _count_regex(src_files, r"\b(Dict|List|Tuple|Optional|Set|FrozenSet)\[")
    type_new = _count_regex(src_files, r"\b(dict|list|tuple|set|frozenset)\[")

    doc_total, doc_zh, doc_google = _docstring_stats(src_files)
    comment_total, comment_zh = _comment_lang(src_files)

    return ScanResult(
        src_files=tuple(src_files),
        test_files=tuple(test_files),
        py_files=tuple(py_files),
        naming_classes=classes,
        naming_functions=funcs,
        naming_constants=consts,
        function_stat=fstat,
        import_order_score=_import_order_score(py_files),
        logger_factory_count=_count_regex(py_files, r"Logger\(__name__\)\.get_logger\(\)"),
        std_logging_count=_count_regex(py_files, r"logging\.getLogger\("),
        print_count=_count_regex(py_files, r"\bprint\("),
        asyncio_gather_count=_count_regex(py_files, r"asyncio\.gather\("),
        asyncio_create_task_count=_count_regex(py_files, r"asyncio\.create_task\("),
        await_count=_count_ast(py_files, ast.Await),
        except_exception_count=_count_ast(py_files, ast.ExceptHandler),
        parametrize_count=_count_regex(test_files, r"@pytest\.mark\.parametrize"),
        type_old_style=type_old,
        type_new_style=type_new,
        docstring_total=doc_total,
        docstring_chinese=doc_zh,
        docstring_google=doc_google,
        comment_total=comment_total,
        comment_chinese=comment_zh,
        module_singletons=_detect_module_singletons(src_files),
    )


def _write_conventions(root: Path, out: Path, scan: ScanResult) -> None:
    now = datetime.now(timezone.utc).isoformat()
    manual = _extract_manual_notes(
        out,
        default_text="Add maintainer notes here.\nThis section is preserved on refresh.",
    )

    type_style = "typing (Dict/List/...)" if scan.type_old_style >= scan.type_new_style else "builtins (dict/list/...)"
    doc_lang = "Chinese" if scan.docstring_chinese > scan.docstring_total * 0.3 else "English"
    comment_lang = "Chinese" if scan.comment_chinese > scan.comment_total * 0.3 else "English"

    singleton_examples = ", ".join(f"`{i} = {c}(...)`" for i, c in scan.module_singletons[:4]) or "(none)"

    content = f"""# Agent Conventions Profile

> Auto-generated. Do not edit generated sections directly.
> Generated at: {now}
> Source files scanned: {len(scan.src_files)} | Test files: {len(scan.test_files)} | Total: {len(scan.py_files)}

## Actionable Conventions

- **Type hints**: dominant style is {type_style} (old={scan.type_old_style}, new={scan.type_new_style})
- **Docstrings**: {doc_lang}, Google-style sections count={scan.docstring_google}
- **Comments**: {comment_lang}
- **Module singletons**: preferred pattern `service = Service()` at module bottom
  - examples: {singleton_examples}

## Naming Snapshot
- Class: PascalCase — {", ".join(scan.naming_classes) or "(none)"}
- Function: snake_case — {", ".join(scan.naming_functions) or "(none)"}
- Constant: UPPER_SNAKE — {", ".join(scan.naming_constants) or "(none)"}

## Typing & Function Style
- Functions detected: {scan.function_stat.total}
- Fully typed: {scan.function_stat.fully_typed} ({_safe_pct(scan.function_stat.fully_typed, scan.function_stat.total)})
- Async: {scan.function_stat.async_total} ({_safe_pct(scan.function_stat.async_total, scan.function_stat.total)})

## Runtime Metrics
| Metric | Count |
|--------|-------|
| `print()` calls | {scan.print_count} |
| `asyncio.gather()` | {scan.asyncio_gather_count} |
| `asyncio.create_task()` | {scan.asyncio_create_task_count} |
| `await` expressions | {scan.await_count} |
| `@pytest.mark.parametrize` | {scan.parametrize_count} |

## Maintainer Notes
{MANUAL_START}
{manual}
{MANUAL_END}
"""
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content, encoding="utf-8")


def _write_project_context(root: Path, out: Path, scan: ScanResult) -> None:
    now = datetime.now(timezone.utc).isoformat()
    manual = _extract_manual_notes(
        out,
        default_text="Add project semantics and constraints here.\nThis section is preserved on refresh.",
    )
    branch = _run_git(root, ["rev-parse", "--abbrev-ref", "HEAD"]) or "unknown"
    remote = _run_git(root, ["remote", "get-url", "origin"]) or "unknown"

    content = f"""# Project Context Profile

> Auto-generated. Do not edit generated sections directly.
> Generated at: {now}

## Repository
- Root: `{root}`
- Git branch: `{branch}`
- Git remote(origin): `{remote}`

## Technology Signals
- Python files: {len(scan.py_files)}
- `pyproject.toml` exists: {"yes" if (root / "pyproject.toml").exists() else "no"}
- `requirements.txt` exists: {"yes" if (root / "requirements.txt").exists() else "no"}

## Top-Level Layout
{_project_tree(root)}

## Maintainer Notes
{MANUAL_START}
{manual}
{MANUAL_END}
"""
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content, encoding="utf-8")


def _write_metadata(root: Path, out: Path, scan: ScanResult) -> None:
    data = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repo_root": str(root),
        "python_files_scanned": len(scan.py_files),
        "source_files_scanned": len(scan.src_files),
        "test_files_scanned": len(scan.test_files),
        "metrics": {
            "import_order_score": scan.import_order_score,
            "logger_factory_count": scan.logger_factory_count,
            "std_logging_count": scan.std_logging_count,
            "print_count": scan.print_count,
            "asyncio_gather_count": scan.asyncio_gather_count,
            "asyncio_create_task_count": scan.asyncio_create_task_count,
            "await_count": scan.await_count,
            "parametrize_count": scan.parametrize_count,
            "functions_total": scan.function_stat.total,
            "functions_fully_typed": scan.function_stat.fully_typed,
            "functions_async": scan.function_stat.async_total,
            "type_annotation_old_style": scan.type_old_style,
            "type_annotation_new_style": scan.type_new_style,
            "docstring_total": scan.docstring_total,
            "docstring_chinese": scan.docstring_chinese,
            "comment_total": scan.comment_total,
            "comment_chinese": scan.comment_chinese,
            "module_singletons": list(scan.module_singletons),
        },
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _write_cursor_rule(root: Path, scan: ScanResult) -> None:
    out = root / ".cursor" / "rules" / "learned-conventions.mdc"

    type_hint = (
        "Use typing generics (`Dict`, `List`, `Optional`, `Tuple`)"
        if scan.type_old_style >= scan.type_new_style
        else "Use builtin generics (`dict`, `list`, `tuple`)"
    )

    singleton = ""
    if scan.module_singletons:
        examples = ", ".join(f"`{i} = {c}(...)`" for i, c in scan.module_singletons[:3])
        singleton = f"- **Module singletons**: instantiate services once at module level (e.g. {examples})\n"

    content = f"""---
description: Learned conventions from this codebase - load for coding, architecture code design, tests, refactors, code review, and bug fixes
alwaysApply: false
---

# Learned Conventions (Auto-generated)

> Auto-generated by `scripts/generate_agent_context.py`.
> Do NOT edit manually. Refresh via `python scripts/refresh_agent_context.py`.

## Protocol

Priority order:
1. User instruction
2. This file (project-local)
3. Global baseline (e.g. `ai-coding-protocol.mdc`)

## Summary (Actionable)

{singleton}- **Type hints**: {type_hint}
- **Naming**: PascalCase classes, snake_case functions, UPPER_SNAKE constants
- **Logging**: prefer module-level logger factory when present
- **Docs/Comments**: follow dominant repo language (see `.agent-context/conventions.md`)

Data source: {len(scan.src_files)} source files + {len(scan.test_files)} test files.
"""
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content, encoding="utf-8")


def generate(root: Path) -> int:
    scan = _scan(root)
    out_dir = root / ".agent-context"
    _write_conventions(root, out_dir / "conventions.md", scan)
    _write_project_context(root, out_dir / "project-context.md", scan)
    _write_metadata(root, out_dir / "metadata.json", scan)
    _write_cursor_rule(root, scan)
    print(f"[OK] generated agent context in: {out_dir}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate .agent-context profiles")
    parser.add_argument("--root", type=Path, default=_repo_root(), help="Repository root")
    args = parser.parse_args()
    return generate(args.root.resolve())


if __name__ == "__main__":
    raise SystemExit(main())

