"""Run scientific integrity, frozen-source, figure, and report checks."""

from __future__ import annotations

import csv
import hashlib
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image


ROOT = Path(__file__).resolve().parent
TABLES = ROOT / "results" / "tables"
EXPECTED_FROZEN = {
    "src/variability_analysis/bx_candidates.py": "b5581c121542731b4b34ce8b33eb4b420ce33b43c93b02cf3ef4a97116a057cd",
    "src/variability_analysis/phase4.py": "2351684a1c03a8a53fb66f4da1ea4fbb25c162aefad392212bfc5333f5099140",
    "src/variability_analysis/signal_processing.py": "0a5b6741e50ec47773b4a8367825b428592a80c076a37bcf1ccb40a49ceaab2e",
}
EXPECTED_REFERENCE_BUILDER = {
    "src/reference_validation/create_heartcycle_validation_csv.py": "c6f5487c2167f0d4c3f34ff67e5104e5c582af9de2f1de3654713752ea633591",
}
EXPECTED_REPORT = "af5a42f4bbc3b1b5c19a934c333ea6026949726d91baedd7fe3aea390131ac88"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def require(name: str, passed: bool, observed: object, expected: object) -> None:
    state = "PASS" if passed else "FAIL"
    print(f"{state:4}  {name}: {observed}")
    if not passed:
        raise AssertionError(f"{name}: observed {observed!r}; expected {expected!r}")


def main() -> None:
    detections = pd.read_csv(TABLES / "detections.csv", low_memory=False)
    morphology = pd.read_csv(TABLES / "morphology_continuous.csv", low_memory=False)
    categories = pd.read_csv(TABLES / "morphology_categories.csv", low_memory=False)
    condition = pd.read_csv(TABLES / "condition_morphology.csv", low_memory=False)
    failure = pd.read_csv(TABLES / "failure_mechanisms.csv", low_memory=False)

    require("dataset-condition-method rows", len(detections) == 115, len(detections), 115)
    require("datasets", set(detections.dataset) == {"HeartCycle", "IITB", "ReBeat"}, sorted(detections.dataset.unique()), ["HeartCycle", "IITB", "ReBeat"])
    require("B definitions", set(detections.loc[detections.point_type.eq("B"), "algorithm_id"]) == {f"B{i}" for i in range(1, 11)}, 10, 10)
    require("X definitions", set(detections.loc[detections.point_type.eq("X"), "algorithm_id"]) == {f"X{i}" for i in range(1, 14)}, 13, 13)
    status_ok = (
        detections.total_beat_n.eq(detections.valid_detection_n + detections.missed_detection_n + detections.invalid_detection_n + detections.upstream_ineligible_n)
        & detections.attempted_beat_n.eq(detections.valid_detection_n + detections.missed_detection_n + detections.invalid_detection_n)
    )
    require("status denominators", bool(status_ok.all()), int((~status_ok).sum()), 0)
    require("continuous morphology tests", len(morphology) == 1794 and morphology.feature.nunique() == 6, f"{len(morphology)} rows, {morphology.feature.nunique()} features", "1794 rows, 6 features")
    require("categorical morphology tests", len(categories) == 2208 and categories.feature.nunique() == 6, f"{len(categories)} rows, {categories.feature.nunique()} features", "2208 rows, 6 features")
    require("condition-morphology tests", len(condition) == 672, len(condition), 672)

    x3 = condition.loc[
        condition.dataset.eq("IITB")
        & condition.point_type.eq("X")
        & condition.algorithm_id.eq("X3")
        & condition.outcome.eq("failure_rate_pct")
        & condition.feature.eq("beat_to_beat_variability")
    ]
    require("IITB X3 row", len(x3) == 1, len(x3), 1)
    row = x3.iloc[0]
    x3_ok = (
        np.isclose(row.spearman_rho, 0.3973597071195132)
        and np.isclose(row.permutation_p, 1 / 9)
        and np.isclose(row.bh_q_value, 0.9604357211337692)
        and not bool(row.exploratory_supported)
    )
    require("IITB X3 corrected statistics", bool(x3_ok), f"rho={row.spearman_rho:.8f}, p={row.permutation_p:.8f}, q={row.bh_q_value:.8f}", "corrected unsupported result")

    keys = ["dataset", "condition", "point_type", "algorithm_id"]
    reconciled = failure.groupby(keys).reason_record_n.sum().eq(failure.groupby(keys).failed_or_ineligible_n.first())
    require("failure-reason reconciliation", bool(reconciled.all()), int((~reconciled).sum()), 0)

    for relative, expected in EXPECTED_FROZEN.items():
        observed = sha256(ROOT / relative)
        require(f"frozen hash {Path(relative).name}", observed == expected, observed, expected)

    for relative, expected in EXPECTED_REFERENCE_BUILDER.items():
        observed = sha256(ROOT / relative)
        require("HeartCycle reference builder hash", observed == expected, observed, expected)

    rows = list(csv.DictReader((ROOT / "manifests/figures.csv").open(encoding="utf-8")))
    figure_ok = True
    for item in rows:
        path = ROOT / item["release_path"]
        if not path.exists() or sha256(path) != item["sha256"]:
            figure_ok = False
            break
        with Image.open(path) as image:
            image.verify()
    require("accepted PNG figures", figure_ok and len(rows) == 27, len(rows), 27)

    report = ROOT / "results/P1_Report.docx"
    require("unchanged report", report.exists() and sha256(report) == EXPECTED_REPORT, sha256(report) if report.exists() else "missing", EXPECTED_REPORT)
    subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], cwd=ROOT, check=True)
    print("All release checks passed.")


if __name__ == "__main__":
    main()

