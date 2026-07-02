"""
Generate dynamic project context for AI coding agents.

Outputs (auto-generated):
  - .agent-context/conventions.md
  - .agent-context/project-context.md
  - .agent-context/metadata.json

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
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


MANUAL_START = "<!-- MANUAL_NOTES_START -->"
MANUAL_END = "<!-- MANUAL_NOTES_END -->"


@dataclass(frozen=True)
class FunctionStat:
    total: int = 0
    fully_typed: int = 0
    async_total: int = 0


@dataclass(frozen=True)
class NamingStat:
    classes: tuple[str, ...]
    functions: tuple[str, ...]
    constants: tuple[str, ...]


@dataclass(frozen=True)
class ModuleSingletonStat:
    instances: tuple[tuple[str, str], ...]  # (instance_name, class_name)
    file_count: int
    total_src_files: int


@dataclass(frozen=True)
class DocstringStat:
    total: int
    chinese: int
    with_args_section: int
    style: str  # "Google", "NumPy", "reST", "mixed", "none"


@dataclass(frozen=True)
class TypeAnnotationStat:
    old_style: int  # Dict, List, Optional, Tuple from typing
    new_style: int  # dict, list, ... as builtin generics


@dataclass(frozen=True)
class LoggingStyleStat:
    fstring: int
    lazy_pct: int  # plain string or % formatting
    total: int


@dataclass(frozen=True)
class CommentLangStat:
    chinese_lines: int
    total_comment_lines: int


@dataclass(frozen=True)
class ErrorHandlingStat:
    except_exception: int
    return_on_error: int
    reraise: int
    nested_try: int


@dataclass(frozen=True)
class ScanResult:
    py_files: tuple[Path, ...]
    test_files: tuple[Path, ...]
    src_files: tuple[Path, ...]
    naming: NamingStat
    function_stat: FunctionStat
    import_order_score: float
    except_exception_count: int
    logger_factory_count: int
    std_logging_count: int
    print_count: int
    asyncio_gather_count: int
    asyncio_create_task_count: int
    await_count: int
    parametrize_count: int
    module_singletons: ModuleSingletonStat
    docstring_stat: DocstringStat
    type_annotation_stat: TypeAnnotationStat
    logging_style: LoggingStyleStat
    comment_lang: CommentLangStat
    error_handling: ErrorHandlingStat


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _iter_py_files(base: Path) -> list[Path]:
    if not base.exists():
        return []
    return sorted(
        [
            p
            for p in base.rglob("*.py")
            if "__pycache__" not in p.parts and ".venv" not in p.parts
        ]
    )


def _parse_ast(path: Path) -> ast.AST | None:
    try:
        return ast.parse(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _extract_naming(py_files: list[Path]) -> NamingStat:
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
        for node in tree.body:  # module-level constants only
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id.isupper():
                        constants.append(target.id)

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

    return NamingStat(classes=_uniq(classes), functions=_uniq(functions), constants=_uniq(constants))


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


def _import_category(module_name: str) -> int:
    """
    Category order:
      0: future/stdlib
      1: third-party
      2: local project
    """
    if module_name == "__future__":
        return 0
    root = module_name.split(".")[0]
    if root in {"<project_repo>", "tests"}:
        return 2
    if root in sys.stdlib_module_names:
        return 0
    return 1


def _import_order_score(py_files: list[Path]) -> float:
    if not py_files:
        return 0.0
    checked = 0
    ordered = 0

    for path in py_files:
        lines = path.read_text(encoding="utf-8").splitlines()
        categories: list[int] = []
        for line in lines:
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
            # Stop at first non-import statement
            break

        if not categories:
            continue
        checked += 1
        if categories == sorted(categories):
            ordered += 1

    if checked == 0:
        return 0.0
    return round(ordered / checked * 100.0, 1)


def _count_pattern(py_files: list[Path], pattern: str) -> int:
    regex = re.compile(pattern)
    count = 0
    for path in py_files:
        text = path.read_text(encoding="utf-8")
        count += len(regex.findall(text))
    return count


def _count_ast_await(py_files: list[Path]) -> int:
    count = 0
    for path in py_files:
        tree = _parse_ast(path)
        if tree is None:
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Await):
                count += 1
    return count


def _count_except_exception(py_files: list[Path]) -> int:
    count = 0
    for path in py_files:
        tree = _parse_ast(path)
        if tree is None:
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.ExceptHandler) and isinstance(node.type, ast.Name):
                if node.type.id == "Exception":
                    count += 1
    return count


_FRAMEWORK_CLASSES = frozenset({
    "FastAPI", "APIRouter", "Compiler", "Counter", "Path",
    "ArgumentParser", "Logger", "Depends",
})


def _detect_module_singletons(py_files: list[Path]) -> ModuleSingletonStat:
    """Detect `var = ClassName(...)` at module level (service/component singletons)."""
    instances: list[tuple[str, str]] = []
    files_with: set[Path] = set()

    for path in py_files:
        tree = _parse_ast(path)
        if tree is None:
            continue
        for node in tree.body:
            if isinstance(node, ast.Assign) and len(node.targets) == 1:
                target = node.targets[0]
                if (
                    isinstance(target, ast.Name)
                    and isinstance(node.value, ast.Call)
                    and not target.id.startswith("_")
                    and not target.id.isupper()
                    and target.id != "logger"
                ):
                    func = node.value.func
                    cls_name = ""
                    if isinstance(func, ast.Name):
                        cls_name = func.id
                    elif isinstance(func, ast.Attribute):
                        cls_name = func.attr
                    if cls_name and cls_name[0].isupper() and cls_name not in _FRAMEWORK_CLASSES:
                        instances.append((target.id, cls_name))
                        files_with.add(path)

    seen_names: set[str] = set()
    unique: list[tuple[str, str]] = []
    for inst, cls in instances:
        if inst not in seen_names:
            unique.append((inst, cls))
            seen_names.add(inst)

    return ModuleSingletonStat(
        instances=tuple(unique[:12]),
        file_count=len(files_with),
        total_src_files=len(py_files),
    )


_CJK_RE = re.compile(r"[\u4e00-\u9fff]")


def _detect_docstring_style(py_files: list[Path]) -> DocstringStat:
    total = 0
    chinese = 0
    with_args = 0
    google = 0
    numpy = 0

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
                    with_args += 1
                    google += 1
                elif "Parameters\n----------" in ds:
                    numpy += 1

    if google > numpy:
        style = "Google"
    elif numpy > google:
        style = "NumPy"
    elif total == 0:
        style = "none"
    else:
        style = "mixed"

    return DocstringStat(total=total, chinese=chinese, with_args_section=with_args, style=style)


def _detect_type_annotation_style(py_files: list[Path]) -> TypeAnnotationStat:
    old_re = re.compile(r"\b(Dict|List|Tuple|Optional|Set|FrozenSet)\[")
    new_re = re.compile(r"\b(dict|list|tuple|set|frozenset)\[")
    old = 0
    new = 0
    for path in py_files:
        text = path.read_text(encoding="utf-8")
        old += len(old_re.findall(text))
        new += len(new_re.findall(text))
    return TypeAnnotationStat(old_style=old, new_style=new)


def _detect_logging_style(py_files: list[Path]) -> LoggingStyleStat:
    fstring_re = re.compile(r"logger\.\w+\(f[\"']")
    plain_re = re.compile(r"logger\.\w+\([\"'][^f]")
    fstring = 0
    plain = 0
    for path in py_files:
        text = path.read_text(encoding="utf-8")
        fstring += len(fstring_re.findall(text))
        plain += len(plain_re.findall(text))
    total = fstring + plain
    return LoggingStyleStat(fstring=fstring, lazy_pct=plain, total=total)


def _detect_comment_language(py_files: list[Path]) -> CommentLangStat:
    chinese_lines = 0
    total_comments = 0
    for path in py_files:
        for line in path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped.startswith("#"):
                total_comments += 1
                if _CJK_RE.search(stripped):
                    chinese_lines += 1
    return CommentLangStat(chinese_lines=chinese_lines, total_comment_lines=total_comments)


def _detect_error_handling(py_files: list[Path]) -> ErrorHandlingStat:
    except_exception = 0
    return_on_error = 0
    reraise = 0
    nested_try = 0

    for path in py_files:
        tree = _parse_ast(path)
        if tree is None:
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.ExceptHandler):
                if isinstance(node.type, ast.Name) and node.type.id == "Exception":
                    except_exception += 1
                    has_return = any(isinstance(n, ast.Return) for n in ast.walk(node))
                    has_raise = any(isinstance(n, ast.Raise) for n in ast.walk(node))
                    if has_return:
                        return_on_error += 1
                    if has_raise:
                        reraise += 1
            if isinstance(node, ast.Try):
                for child in ast.walk(node):
                    if child is not node and isinstance(child, ast.Try):
                        nested_try += 1
                        break

    return ErrorHandlingStat(
        except_exception=except_exception,
        return_on_error=return_on_error,
        reraise=reraise,
        nested_try=nested_try,
    )


def _resolve_scan_roots(root: Path) -> tuple[list[Path], list[Path]]:
    src_candidates: list[Path] = []
    tests_candidates: list[Path] = []

    # Prefer focused app roots when available.
    focused_src = root / "src" / "<project_repo>"
    if focused_src.exists():
        src_candidates.append(focused_src)
    elif (root / "src").exists():
        src_candidates.append(root / "src")

    if (root / "tests").exists():
        tests_candidates.append(root / "tests")

    return src_candidates, tests_candidates


def _scan(root: Path) -> ScanResult:
    src_roots, test_roots = _resolve_scan_roots(root)
    src_files: list[Path] = []
    test_files: list[Path] = []
    for p in src_roots:
        src_files.extend(_iter_py_files(p))
    for p in test_roots:
        test_files.extend(_iter_py_files(p))
    py_files = sorted(src_files + test_files)

    naming = _extract_naming(py_files)
    fstat = _function_stats(py_files)

    return ScanResult(
        py_files=tuple(py_files),
        test_files=tuple(test_files),
        src_files=tuple(src_files),
        naming=naming,
        function_stat=fstat,
        import_order_score=_import_order_score(py_files),
        except_exception_count=_count_except_exception(py_files),
        logger_factory_count=_count_pattern(py_files, r"Logger\(__name__\)\.get_logger\(\)"),
        std_logging_count=_count_pattern(py_files, r"logging\.getLogger\("),
        print_count=_count_pattern(py_files, r"\bprint\("),
        asyncio_gather_count=_count_pattern(py_files, r"asyncio\.gather\("),
        asyncio_create_task_count=_count_pattern(py_files, r"asyncio\.create_task\("),
        await_count=_count_ast_await(py_files),
        parametrize_count=_count_pattern(test_files, r"@pytest\.mark\.parametrize"),
        module_singletons=_detect_module_singletons(src_files),
        docstring_stat=_detect_docstring_style(src_files),
        type_annotation_stat=_detect_type_annotation_style(src_files),
        logging_style=_detect_logging_style(src_files),
        comment_lang=_detect_comment_language(src_files),
        error_handling=_detect_error_handling(src_files),
    )


def _safe_pct(num: int, den: int) -> str:
    if den <= 0:
        return "0.0%"
    return f"{(num / den) * 100:.1f}%"


def _relative(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except Exception:
        return str(path)


def _diverse_sample(py_files: tuple[Path, ...], root: Path, limit: int = 8) -> list[Path]:
    """Pick sample files from diverse subdirectories, preferring real logic files."""
    by_parent: dict[Path, list[Path]] = {}
    for p in py_files:
        rel = p.relative_to(root)
        by_parent.setdefault(rel.parent, []).append(p)

    def _best_pick(files: list[Path]) -> Path:
        non_init = [f for f in files if f.name != "__init__.py"]
        return non_init[0] if non_init else files[0]

    def _sort_key(parent: Path) -> tuple[int, int]:
        is_src = 0 if str(parent).startswith("src") else 1
        return (is_src, len(parent.parts))

    result: list[Path] = []
    seen_parents: set[Path] = set()

    for parent in sorted(by_parent, key=_sort_key):
        if len(result) >= limit:
            break
        if parent in seen_parents:
            continue
        result.append(_best_pick(by_parent[parent]))
        seen_parents.add(parent)

    return result[:limit]


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
    entries = []
    for p in sorted(root.iterdir()):
        if p.name.startswith(".git"):
            continue
        if p.is_dir():
            entries.append(f"- {p.name}/")
        else:
            entries.append(f"- {p.name}")
    return "\n".join(entries[:40])


def _commit_style_summary(root: Path) -> str:
    logs = _run_git(root, ["log", "--oneline", "-50"])
    if not logs:
        return "unknown"
    counter: Counter[str] = Counter()
    for line in logs.splitlines():
        msg = line.split(" ", 1)[1] if " " in line else line
        m = re.match(r"([a-zA-Z]+)\s*:", msg)
        if m:
            counter[m.group(1).lower()] += 1
    if not counter:
        return "free-form"
    top = ", ".join(f"{k}:{v}" for k, v in counter.most_common(6))
    return top


def _write_conventions(root: Path, out: Path, scan: ScanResult) -> None:
    now = datetime.now(timezone.utc).isoformat()
    manual = _extract_manual_notes(
        out,
        default_text=(
            "在这里补充团队约定（人工维护）。\n"
            "自动刷新不会覆盖本区域内容。"
        ),
    )

    samples = _diverse_sample(scan.py_files, root, limit=8)
    sample_files = "\n".join(
        f"- `{_relative(p, root)}`" for p in samples
    ) or "- (no python files found)"

    # --- Build actionable sections ---
    s = scan  # shorthand

    # Module singleton section
    singleton_section = ""
    if s.module_singletons.instances:
        examples = ", ".join(
            f"`{inst} = {cls}(...)`" for inst, cls in s.module_singletons.instances[:5]
        )
        singleton_section = f"""
## Architectural Pattern: Module-Level Singletons
- **Convention**: Service/expert classes are instantiated once at module level
- **Confidence**: found in {s.module_singletons.file_count}/{s.module_singletons.total_src_files} source files
- **Examples**: {examples}
- **Instruction**: When creating a new service class, add a module-level instance at the bottom of the file
"""

    # Type annotation section
    ta = s.type_annotation_stat
    total_ta = ta.old_style + ta.new_style
    if total_ta > 0:
        dominant_style = "old-style `Dict[str, Any]` from `typing`" if ta.old_style > ta.new_style else "built-in `dict[str, Any]`"
        ta_section = f"""
## Type Annotation Style
- **Dominant**: {dominant_style} ({ta.old_style} old-style vs {ta.new_style} new-style)
- **Instruction**: Use `Dict`, `List`, `Optional`, `Tuple` from `typing` module (not builtin generics)
"""
    else:
        ta_section = ""

    # Docstring section
    ds = s.docstring_stat
    if ds.total > 0:
        lang = "Chinese" if ds.chinese > ds.total * 0.3 else "English"
        ds_section = f"""
## Docstring Convention
- **Language**: {lang} ({ds.chinese}/{ds.total} contain Chinese)
- **Format**: {ds.style} style ({ds.with_args_section}/{ds.total} have Args/Returns sections)
- **Instruction**: Write docstrings in {"Chinese" if lang == "Chinese" else "English"}, use {ds.style}-style `Args:` / `Returns:` sections
"""
    else:
        ds_section = ""

    # Logging style section
    ls = s.logging_style
    if ls.total > 0:
        fstring_pct = round(ls.fstring / ls.total * 100)
        logger_init = "`logger = Logger(__name__).get_logger()`" if s.logger_factory_count > s.std_logging_count else "`logging.getLogger(__name__)`"
        ls_section = f"""
## Logging Convention
- **Logger init**: {logger_init} (used in {s.logger_factory_count} files)
- **Format style**: f-string ({fstring_pct}% of {ls.total} log calls)
- **Instruction**: Initialize logger at module level using `Logger(__name__).get_logger()`, format messages with f-strings
"""
    else:
        ls_section = ""

    # Comment language section
    cl = s.comment_lang
    if cl.total_comment_lines > 0:
        ch_pct = round(cl.chinese_lines / cl.total_comment_lines * 100)
        cl_section = f"""
## Comment Language
- **Chinese comments**: {cl.chinese_lines}/{cl.total_comment_lines} ({ch_pct}%)
- **Instruction**: {"Write inline comments in Chinese" if ch_pct > 30 else "Write inline comments in English"}
"""
    else:
        cl_section = ""

    # Error handling section
    eh = s.error_handling
    if eh.except_exception > 0:
        total_handled = eh.return_on_error + eh.reraise
        if total_handled > 0:
            ret_pct = round(eh.return_on_error / total_handled * 100)
        else:
            ret_pct = 0
        if ret_pct >= 60:
            instruction = "return sensible defaults and log at warning/error level (do not re-raise in service methods)"
        elif ret_pct <= 30:
            instruction = "re-raise after logging; only return defaults when the caller cannot handle the exception"
        else:
            instruction = "return defaults in service/API boundaries, re-raise in internal/utility code"
        eh_section = f"""
## Error Handling Strategy
- **Pattern**: `except Exception` ({eh.except_exception} total), return-on-error ({eh.return_on_error}, {ret_pct}%), re-raise ({eh.reraise})
- **Nested try blocks**: {eh.nested_try} (granular per-operation wrapping)
- **Instruction**: {instruction}
"""
    else:
        eh_section = ""

    content = f"""# Agent Conventions Profile

> Auto-generated. Do not edit generated sections directly.
> Generated at: {now}
> Source files scanned: {len(scan.src_files)} | Test files: {len(scan.test_files)} | Total: {len(scan.py_files)}
{singleton_section}{ta_section}{ds_section}{ls_section}{cl_section}{eh_section}
## Naming Snapshot
- Class: PascalCase — {", ".join(scan.naming.classes) or "(none)"}
- Function: snake_case — {", ".join(scan.naming.functions) or "(none)"}
- Constant: UPPER_SNAKE — {", ".join(scan.naming.constants) or "(none)"}

## Typing & Function Style
- Functions detected: {scan.function_stat.total}
- Fully typed: {scan.function_stat.fully_typed} ({_safe_pct(scan.function_stat.fully_typed, scan.function_stat.total)})
- Async: {scan.function_stat.async_total} ({_safe_pct(scan.function_stat.async_total, scan.function_stat.total)})

## Import Order
- Consistency score: {scan.import_order_score}% (stdlib → third-party → local)

## Runtime Metrics
| Metric | Count |
|--------|-------|
| `print()` calls | {scan.print_count} |
| `asyncio.gather()` | {scan.asyncio_gather_count} |
| `asyncio.create_task()` | {scan.asyncio_create_task_count} |
| `await` expressions | {scan.await_count} |
| `@pytest.mark.parametrize` | {scan.parametrize_count} |

## Sample Files Used
{sample_files}

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
        default_text=(
            "在这里记录业务语义、架构决策和约束（人工维护）。\n"
            "自动刷新不会覆盖本区域内容。"
        ),
    )

    branch = _run_git(root, ["rev-parse", "--abbrev-ref", "HEAD"]) or "unknown"
    remote = _run_git(root, ["remote", "get-url", "origin"]) or "unknown"
    commit_style = _commit_style_summary(root)

    content = f"""# Project Context Profile

> Auto-generated. Do not edit generated sections directly.
> Generated at: {now}

## Repository
- Root: `{root}`
- Git branch: `{branch}`
- Git remote(origin): `{remote}`
- Recent commit style signal: `{commit_style}`

## Technology Signals
- Python files: {len(scan.py_files)}
- Source dir exists: {"yes" if (root / "src").exists() else "no"}
- Tests dir exists: {"yes" if (root / "tests").exists() else "no"}
- `pyproject.toml` exists: {"yes" if (root / "pyproject.toml").exists() else "no"}
- `requirements.txt` exists: {"yes" if (root / "requirements.txt").exists() else "no"}
- `.pre-commit-config.yaml` exists: {"yes" if (root / ".pre-commit-config.yaml").exists() else "no"}

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
    ta = scan.type_annotation_stat
    ls = scan.logging_style
    cl = scan.comment_lang
    eh = scan.error_handling
    ms = scan.module_singletons
    ds = scan.docstring_stat

    data = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repo_root": str(root),
        "python_files_scanned": len(scan.py_files),
        "source_files_scanned": len(scan.src_files),
        "test_files_scanned": len(scan.test_files),
        "metrics": {
            "import_order_score": scan.import_order_score,
            "except_exception_count": scan.except_exception_count,
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
            "type_annotation_old_style": ta.old_style,
            "type_annotation_new_style": ta.new_style,
            "logging_fstring": ls.fstring,
            "logging_plain": ls.lazy_pct,
            "comment_chinese_lines": cl.chinese_lines,
            "comment_total_lines": cl.total_comment_lines,
            "error_return_on_error": eh.return_on_error,
            "error_reraise": eh.reraise,
            "error_nested_try": eh.nested_try,
            "module_singleton_count": len(ms.instances),
            "docstring_total": ds.total,
            "docstring_chinese": ds.chinese,
            "docstring_style": ds.style,
        },
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _write_cursor_rule(root: Path, scan: ScanResult) -> None:
    """Generate a .cursor/rules/learned-conventions.mdc for deterministic loading."""
    out = root / ".cursor" / "rules" / "learned-conventions.mdc"
    s = scan
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # --- Build structured sections ---

    # Section 1: Architecture & Patterns
    arch_items: list[str] = []
    if s.module_singletons.instances:
        examples = ", ".join(f"`{i} = {c}(...)`" for i, c in s.module_singletons.instances[:4])
        arch_items.append(
            f"1. **Module-Level Singletons** — Service/expert classes instantiated once at module bottom.\n"
            f"   Examples: {examples}\n"
            f"   Confidence: {s.module_singletons.file_count}/{s.module_singletons.total_src_files} source files"
        )

    eh = s.error_handling
    if eh.except_exception > 0:
        total_h = eh.return_on_error + eh.reraise
        ret_pct = round(eh.return_on_error / total_h * 100) if total_h else 0
        if ret_pct >= 60:
            strat = "return sensible defaults + log warning (do not re-raise)"
        elif ret_pct <= 30:
            strat = "re-raise after logging"
        else:
            strat = "return defaults at service/API boundaries; re-raise in internal/utility code"
        arch_items.append(
            f"2. **Error Handling** — {strat}.\n"
            f"   Nested try blocks: {eh.nested_try} (granular per-operation wrapping)"
        )

    arch_section = "\n\n".join(arch_items) if arch_items else "(no patterns detected)"

    # Section 2: Code Style
    style_items: list[str] = []

    ta = s.type_annotation_stat
    if ta.old_style + ta.new_style > 0:
        if ta.old_style > ta.new_style:
            style_items.append(
                f"- **Type hints**: Use `Dict`, `List`, `Optional`, `Tuple` from `typing` "
                f"({ta.old_style} old-style vs {ta.new_style} new-style)"
            )
        else:
            style_items.append(
                "- **Type hints**: Use builtin generics (`dict`, `list`, `tuple`)"
            )

    style_items.append(
        f"- **Naming**: PascalCase classes, snake_case functions, UPPER_SNAKE constants"
    )
    style_items.append(
        f"- **Typing density**: {_safe_pct(s.function_stat.fully_typed, s.function_stat.total)} "
        f"fully typed — match this level for new code"
    )

    ds = s.docstring_stat
    if ds.total > 0:
        lang = "Chinese" if ds.chinese > ds.total * 0.3 else "English"
        style_items.append(
            f"- **Docstrings**: {lang}, {ds.style}-style (`Args:` / `Returns:` sections)"
        )

    cl = s.comment_lang
    if cl.total_comment_lines > 0:
        ch_pct = round(cl.chinese_lines / cl.total_comment_lines * 100)
        if ch_pct > 30:
            style_items.append(f"- **Comments**: Chinese inline comments ({ch_pct}%)")

    style_section = "\n".join(style_items)

    # Section 3: Logging
    ls = s.logging_style
    if ls.total > 0 and s.logger_factory_count > 0:
        fstring_pct = round(ls.fstring / ls.total * 100) if ls.total else 0
        log_section = (
            f"- **Init**: `logger = Logger(__name__).get_logger()` at module level ({s.logger_factory_count} files)\n"
            f"- **Format**: f-string ({fstring_pct}% of {ls.total} log calls)\n"
            f"- **Levels**: `logger.info` for flow, `logger.warning` for recoverable, `logger.error` for fatal"
        )
    else:
        log_section = "- (no dominant logging pattern detected)"

    content = f"""---
description: 代码库自动学习的编码约定 - 编写代码、工程架构代码设计、编写测试、重构代码、代码审查、修复 bug 时加载
alwaysApply: false
---

# 项目编码约定（自动学习）

> Auto-generated by `scripts/generate_agent_context.py` on {now}.
> **Do NOT manually edit** — changes will be overwritten on next refresh.

---

## 加载条件

本规则在以下场景由 Cursor 自动注入：

- 编写或修改 Python 代码
- 工程架构代码设计（涉及目录边界、模块拆分、依赖关系、服务分层）
- 编写或修改测试用例
- 重构现有代码
- 代码审查
- 修复 bug

**不加载**：产品交互/UI 设计、纯文档编辑、配置调整、问答咨询。

---

## 使用协议

```text
优先级链（从高到低）：
  1. 用户明确指示 → 无条件遵守
  2. 本文件中的约定 → 项目级强约束
  3. ai-coding-protocol.mdc → 全局行为基线
  4. AI 自行采样推断 → 仅当上述都无覆盖时
```

本规则 **替代** `ai-coding-protocol.mdc` 中 Read-Before-Write 的 "Sample + Extract" 步骤。
当本规则已加载时，AI 不需要手动采样推断约定，直接遵循以下内容。

---

## 架构模式

{arch_section}

## 代码风格

{style_section}

## 日志规范

{log_section}

---

## 数据来源

- 扫描范围: {len(s.src_files)} 源文件 + {len(s.test_files)} 测试文件
- 详细统计: `.agent-context/conventions.md`
- 机器指标: `.agent-context/metadata.json`

## 刷新方式

```bash
python scripts/refresh_agent_context.py --full        # 全量刷新
python scripts/refresh_agent_context.py --changed-only # 增量刷新
```

## 与其他规则的关系

| 规则 | 关系 | 说明 |
|------|------|------|
| `ai-coding-protocol.mdc` | 上游 | 全局行为基线；本规则提供项目级细节，替代其手动采样步骤 |
| `rokid-agent-project-playbook.mdc` | 并行 | playbook 管架构/路径/分支；本规则管代码风格 |
| `core-think.mdc` | 被引用 | Phase 4c 编码阶段自动加载本规则 |
| `.agent-context/conventions.md` | 数据源 | 本规则是其精简摘要，详细数据见源文件 |
"""

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content, encoding="utf-8")


def generate(root: Path) -> int:
    out_dir = root / ".agent-context"
    scan = _scan(root)
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
