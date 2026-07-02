#!/usr/bin/env python3
"""Lightweight session bootstrap check for AI coding agents."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def _run(root: Path, cmd: list[str]) -> str:
    try:
        return subprocess.check_output(cmd, cwd=root, stderr=subprocess.STDOUT).decode("utf-8").strip()
    except Exception as exc:
        return f"[unavailable] {' '.join(cmd)}: {exc}"


def _latest_ledgers(root: Path, limit: int) -> list[Path]:
    ledger_dir = root / "Docs" / "AgentWork"
    if not ledger_dir.exists():
        return []
    files = [p for p in ledger_dir.glob("*.md") if p.is_file()]
    return sorted(files, key=lambda p: p.stat().st_mtime, reverse=True)[:limit]


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a lightweight new-session continuity check.")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Project root")
    parser.add_argument("--ledger-limit", type=int, default=5, help="Number of recent ledgers to show")
    args = parser.parse_args()

    root = args.root.resolve()
    print(f"[root] {root}")
    print(f"[branch] {_run(root, ['git', 'branch', '--show-current'])}")
    print("[status]")
    status = _run(root, ["git", "status", "--short"])
    print(status if status else "clean")

    ledgers = _latest_ledgers(root, args.ledger_limit)
    print("[recent-ledgers]")
    if not ledgers:
        print("none")
    else:
        for ledger in ledgers:
            print(str(ledger.relative_to(root)))

    print("[reminder]")
    print("Before first editing a target file in this session, reread that file from disk.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
