# ECG-ICG B/X Fiducial Analysis

This repository is the compact release package for Publication 1 Research Question 1: how accurately and reliably do ten B-point definitions and thirteen X-point definitions behave across HeartCycle, IITB-ICG and ReBeatICG, and which waveform or recording conditions are linked to disagreement or failure?

The evidence does not support one universally best definition. HeartCycle provides ECHO AVO and AVC event references, ReBeat provides expert ICG annotations, and IITB has no independent B/X timing reference. Reference error, algorithm disagreement and detection failure are therefore reported as different outcomes. X-point comparisons also require an explicit coverage caution: lower disagreement among common-valid beats cannot be read as better reliability when failed beats were excluded.

## Repository map

```text
.
├── run_analysis.py          # external raw-data replay and result verification
├── make_figures.py          # verify or restage the accepted report figures
├── check_results.py         # scientific, hash, figure and report checks
├── configs/                 # frozen method registry, parameters and path template
├── docs/                    # method, dataset setup and known limitations
├── manifests/               # frozen-source and accepted-figure hashes
├── results/
│   ├── P1_Report.docx       # unchanged 19-page supervisor report
│   ├── tables/              # one primary CSV per observation unit
│   └── figures/             # 27 selected final PNGs only
├── scripts/                 # HeartCycle and IITB/ReBeat clean replay scripts
├── src/
│   ├── data_loading.py
│   ├── signal_filtering.py
│   ├── r_c_detection.py
│   ├── beat_segmentation.py
│   ├── bx_definitions.py
│   ├── detect_points.py
│   ├── reference_matching.py
│   ├── reference_validation/ # original HeartCycle ECHO alignment builder
│   ├── plotting.py
│   ├── analysis/
│   └── variability_analysis/ # byte-verified frozen implementation
└── tests/
```

`results/README.md` defines every table and its observation unit. The 115-row `detections.csv` keeps valid, missed, invalid and upstream-ineligible counts together. Reference accuracy, common-valid disagreement, matched condition changes, morphology tests, failure mechanisms and Bland-Altman comparisons remain separate because their denominators differ.

## Environment

Python 3.12 was used for release validation.

```powershell
python3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

`requirements-lock.txt` records the versions used in the verified environment.

## Verify the packaged release

```powershell
.\.venv\Scripts\python.exe check_results.py
.\.venv\Scripts\python.exe make_figures.py
```

The first command checks all B1-B10 and X1-X13 strata, status denominators, the 1,794 continuous morphology tests, 2,208 categorical contrasts, 672 condition-morphology tests, corrected IITB X3 statistics, failure reconciliation, frozen implementation hashes, 27 PNG hashes and the unchanged Word report. It also runs the regression tests.

## External data and full replay

Raw HDF5 and MAT recordings are not redistributed. Set up the authorised data directory exactly as described in `docs/dataset_setup.md`, then run:

```powershell
.\.venv\Scripts\python.exe run_analysis.py --data-root "D:\path\to\Variability Analysis"
```

This replays HeartCycle source inventory, preprocessing, R/C detection, beat segmentation, all frozen B/X definitions and ECHO alignment. The original reference builder is included at `src/reference_validation/create_heartcycle_validation_csv.py`. The command also replays all IITB and ReBeat recordings and compares detection counts with the packaged canonical results. Generated replay files stay under ignored `validation/` paths. Without `--data-root`, `run_analysis.py` performs the maximum reproducible check of the packaged evidence and states that raw-data replay was not run.

The external data root must contain the raw HeartCycle, IITB and ReBeat recordings plus the preserved HeartCycle `outputs/phase2`, `outputs/phase3` and finalized `outputs/phase4` CSVs used as replay comparators. ReBeat expert annotations must be present under `ReBeatICG/Annotations`. Exact directory names are listed in `docs/dataset_setup.md`.

From these inputs, the repository can independently replay signal preprocessing, R/C detection, beat segmentation, all 23 B/X definitions, detection status counts, HeartCycle ECHO alignment and the final HeartCycle reference metrics. The packaged checks verify the final statistical tables, figures and report. The compact repository does not rebuild every morphology and publication table from raw recordings because the larger event-level derived analysis workspace was deliberately not duplicated.

Copy `configs/paths.example.yaml` to the ignored `configs/paths.local.yaml` only if local path notes are useful. No private absolute path is committed.

## Figures

The public figure set contains 27 PNGs linked to the final report: reference accuracy, signed timing error, failure, common-valid disagreement, matched condition change, morphology, waveform cases and paired method agreement. They are preserved accepted artifacts, not redrawn during repository cleanup.

To restage them from the completed working project and confirm every hash:

```powershell
.\.venv\Scripts\python.exe make_figures.py --source-project "D:\path\to\completed-working-project"
```

Exact waveform and event-level figure regeneration requires the authorised external recordings and the larger derived files from the completed working project. Those files were intentionally not duplicated in this public-facing package.

## Scientific limits

- ECHO valve-event timing and expert ICG annotation timing are not equivalent reference types and are never pooled as a single ground truth.
- IITB has no independent B/X timing reference.
- No approved clinical or analytical timing-error tolerance exists, so no percentage-above-tolerance claim is made.
- Morphology and condition analyses are participant-aware but exploratory. They do not establish physiological causation.
- Participant-relative morphology categories are descriptive strata, not clinical thresholds.
- Source replay requires authorised local access to the original recordings and preserved HeartCycle comparison outputs. The reference builder itself is included and hash-verified.

Additional boundaries are listed in `docs/known_limitations.md`.

## Data acknowledgement and licensing

HeartCycle data and reference channels remain subject to their source permissions. IITB-ICG recordings must be obtained from the authorised source. ReBeatICG is associated with Zenodo record 4725433; users must follow the dataset's own citation and licence terms. The repository does not redistribute raw recordings.

No software licence is included because code ownership and third-party redistribution permissions have not been confirmed. No Git remote is configured and this release process does not publish or push the repository.
