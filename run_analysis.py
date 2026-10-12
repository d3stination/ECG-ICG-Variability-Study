"""Replay the frozen pipeline against external data, then verify packaged results."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def run(*parts: str) -> None:
    command = [sys.executable, *parts]
    print(" ".join(command), flush=True)
    subprocess.run(command, cwd=ROOT, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data-root",
        type=Path,
        help="External Variability Analysis directory. Omit to verify packaged results only.",
    )
    parser.add_argument("--keep-heartcycle-work", action="store_true")
    args = parser.parse_args()

    if args.data_root:
        heartcycle = ["scripts/replay_heartcycle.py", "--data-root", str(args.data_root)]
        if args.keep_heartcycle_work:
            heartcycle.append("--keep-work")
        run(*heartcycle)
        run("scripts/replay_iitb_rebeat.py", "--data-root", str(args.data_root))
    else:
        print("No --data-root supplied; raw-data replay was not run.", flush=True)

    run("check_results.py")


if __name__ == "__main__":
    main()

