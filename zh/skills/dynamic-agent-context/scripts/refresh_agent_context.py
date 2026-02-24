"""
Refresh dynamic AI context files.

Modes:
  --full          always regenerate
  --changed-only  regenerate only when key files changed (or output missing)
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


KEY_PATTERNS = (
    "src/",
    "app/",
    "lib/",
    "tests/",
    "test/",
    "pyproject.toml",
    "requirements.txt",
    ".cursor/rules/",
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _run_git_changed(root: Path) -> list[str]:
    changed: list[str] = []
    cmds = [
        ["git", "diff", "--name-only", "--ignore-submodules=all"],
        ["git", "diff", "--name-only", "--cached", "--ignore-submodules=all"],
        ["git", "ls-files", "--others", "--exclude-standard"],
    ]
    for cmd in cmds:
        try:
            out = subprocess.check_output(cmd, cwd=root, stderr=subprocess.DEVNULL).decode("utf-8")
            changed.extend([line.strip() for line in out.splitlines() if line.strip()])
        except Exception:
            continue
    # de-dup while keeping order
    unique: list[str] = []
    seen: set[str] = set()
    for p in changed:
        if p not in seen:
            unique.append(p)
            seen.add(p)
    return unique


def _needs_refresh(root: Path, changed_files: list[str]) -> bool:
    out_dir = root / ".agent-context"
    required = [
        out_dir / "conventions.md",
        out_dir / "project-context.md",
        out_dir / "metadata.json",
        root / "AGENTS.md",
        root / "CLAUDE.md",
        root / ".cursor" / "rules" / "learned-conventions.mdc",
    ]
    if any(not p.exists() for p in required):
        return True
    return any(p.startswith(KEY_PATTERNS) for p in changed_files)


def _run_python(script: Path, root: Path) -> int:
    return subprocess.call([sys.executable, str(script), "--root", str(root)], cwd=root)


def refresh(root: Path, full: bool) -> int:
    changed = _run_git_changed(root)
    if not full and not _needs_refresh(root, changed):
        print("[SKIP] no key changes detected and context files exist")
        return 0

    gen = root / "scripts" / "generate_agent_context.py"
    sync = root / "scripts" / "sync_agent_entrypoints.py"
    if not gen.exists() or not sync.exists():
        print("[ERR] required scripts are missing under scripts/")
        return 2

    if _run_python(gen, root) != 0:
        return 3
    if _run_python(sync, root) != 0:
        return 4

    print("[OK] refresh completed")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Refresh .agent-context and entrypoint files")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--full", action="store_true", help="Force full refresh")
    group.add_argument("--changed-only", action="store_true", help="Refresh only when key files changed")
    parser.add_argument("--root", type=Path, default=_repo_root(), help="Repository root")
    args = parser.parse_args()

    full = args.full and not args.changed_only
    return refresh(args.root.resolve(), full=full)


if __name__ == "__main__":
    raise SystemExit(main())

