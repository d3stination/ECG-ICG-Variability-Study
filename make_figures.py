"""Verify or restage the report-linked, accepted PNG figure set."""

from __future__ import annotations

import argparse
import csv
import hashlib
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "manifests" / "figures.csv"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source-project",
        type=Path,
        help="Completed working project used to restage the accepted PNGs.",
    )
    args = parser.parse_args()

    rows = list(csv.DictReader(MANIFEST.open(encoding="utf-8")))
    failures: list[str] = []
    for row in rows:
        target = ROOT / row["release_path"]
        if args.source_project:
            source = args.source_project.resolve() / row["source_path"]
            if not source.exists():
                failures.append(f"missing source: {source}")
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
        if not target.exists():
            failures.append(f"missing release figure: {target}")
        elif sha256(target) != row["sha256"]:
            failures.append(f"hash mismatch: {target}")

    if failures:
        raise SystemExit("\n".join(failures))
    action = "restaged and verified" if args.source_project else "verified"
    print(f"{len(rows)} accepted PNG figures {action}.")


if __name__ == "__main__":
    main()

