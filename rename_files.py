#!/usr/bin/env python3
"""
rename_files.py
Safe renamer with collision handling and dry-run.

Usage:
    python rename_files.py --folder files --prefix invoice_ --start 1 --dry-run
"""
from pathlib import Path
import argparse
import logging
from typing import List, Tuple

logging.basicConfig(level=logging.INFO, format="%(message)s")
LOG = logging.getLogger(__name__)


def plan_renames(folder: Path, prefix: str, start: int) -> List[Tuple[Path, Path]]:
    """
    Create a plan: list of (old_path, new_path).
    - Skips files already starting with prefix (idempotent)
    - Finds next free index if collision occurs
    """
    entries = sorted(folder.iterdir(), key=lambda p: p.name)
    plan = []
    counter = start

    for p in entries:
        if not p.is_file():
            continue
        if p.name.startswith(prefix):
            continue

        ext = p.suffix
        while True:
            candidate = folder / f"{prefix}{counter}{ext}"
            if not candidate.exists():
                break
            counter += 1

        plan.append((p, candidate))
        counter += 1

    return plan


def parse_args(argv=None):
    p = argparse.ArgumentParser(description="Rename files in folder safely.")
    p.add_argument("--folder", "-f", default="files", help="Folder containing files")
    p.add_argument("--prefix", "-p", default="file_", help="Prefix for renamed files")
    p.add_argument("--start", "-s", type=int, default=1, help="Starting index")
    p.add_argument("--dry-run", action="store_true", help="Preview changes without renaming")
    return p.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    folder = Path(args.folder)

    if not folder.exists() or not folder.is_dir():
        LOG.error("Folder not found: %s", folder)
        return

    plan = plan_renames(folder, args.prefix, args.start)
    if not plan:
        LOG.info("No files to rename.")
        return

    LOG.info("Planned renames (%d files):", len(plan))
    for old, new in plan:
        LOG.info("  %s -> %s", old.name, new.name)

    if args.dry_run:
        LOG.info("Dry-run enabled. No changes made.")
        return

    for old, new in plan:
        if new.exists():
            LOG.warning("Skipping %s (target exists)", old.name)
            continue
        try:
            old.rename(new)
        except Exception as exc:
            LOG.error("Failed to rename %s -> %s: %s", old.name, new.name, exc)

    LOG.info("✅ Rename complete.")


if __name__ == "__main__":
    main()

