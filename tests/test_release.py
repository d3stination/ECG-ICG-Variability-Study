from __future__ import annotations

import hashlib
import unittest
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "results" / "tables"


class ReleaseTests(unittest.TestCase):
    def test_primary_tables_have_unique_observation_units(self) -> None:
        detections = pd.read_csv(TABLES / "detections.csv", low_memory=False)
        reference = pd.read_csv(TABLES / "reference_accuracy.csv", low_memory=False)
        variability = pd.read_csv(TABLES / "variability.csv", low_memory=False)
        self.assertFalse(detections.duplicated(["dataset", "condition", "point_type", "algorithm_id"]).any())
        self.assertFalse(reference.duplicated(["dataset", "condition", "point_type", "subject_id", "algorithm_id"]).any())
        self.assertFalse(variability.duplicated(["dataset", "condition", "point_type", "subject_id", "algorithm_id", "observation_type"]).any())

    def test_frozen_registry_contains_all_methods(self) -> None:
        registry = pd.read_csv(ROOT / "configs/canonical_method_registry.csv")
        self.assertEqual(set(registry.loc[registry.candidate_type.eq("B"), "algorithm_id"]), {f"B{i}" for i in range(1, 11)})
        self.assertEqual(set(registry.loc[registry.candidate_type.eq("X"), "algorithm_id"]), {f"X{i}" for i in range(1, 14)})

    def test_no_raw_recordings_are_packaged(self) -> None:
        blocked = {".h5", ".hdf5", ".mat", ".edf", ".wfdb"}
        found = [path for path in ROOT.rglob("*") if path.is_file() and path.suffix.lower() in blocked]
        self.assertEqual(found, [])

    def test_report_is_a_docx_package(self) -> None:
        report = ROOT / "results/P1_Report.docx"
        self.assertTrue(report.exists())
        self.assertEqual(report.read_bytes()[:2], b"PK")

    def test_reference_builder_imports(self) -> None:
        from src.reference_validation import create_heartcycle_validation_csv as builder

        self.assertEqual(builder.DATASET_ID, "heartcycle_healthy")
        self.assertTrue(callable(builder.add_echo_references))

    def test_no_local_path_is_committed_in_text_files(self) -> None:
        offenders = []
        windows_user_root = "C:" + "\\Users\\"
        for path in ROOT.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in {".py", ".md", ".yaml", ".json", ".csv", ".txt"}:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            if windows_user_root in text or "C:/" + "Users/" in text:
                offenders.append(str(path.relative_to(ROOT)))
        self.assertEqual(offenders, [])


if __name__ == "__main__":
    unittest.main()

