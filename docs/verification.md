# Verification record

## Clean-repository source replay

The clean repository was replayed in Python 3.12.14 with an isolated virtual environment after the original HeartCycle reference builder was packaged.

- IITB and ReBeat: 84 recordings, 20,654 beats, 475,042 candidate records and 92 dataset-condition-point-method strata. Canonical keys matched and no status or count cells differed.
- HeartCycle: 1,706 preprocessing rows, 1,706 segmented beats, 39,238 B/X candidate rows, 1,706 reference-alignment rows and 23 reference-summary rows. All six comparisons passed with matching keys and zero exact or numeric mismatches at the approved tolerances.
- Categorical morphology: 89,157 participant-category summaries, 2,208 method-feature-outcome contrasts and 118 exploratory supported rows reproduced deterministically.
- The compact release completed six regression tests and all packaged scientific, source-hash, figure-hash and report-hash checks without failure.

The compact release does not include those raw recordings or the full event-level derived workspace. Its own validation checks the packaged canonical evidence, source hashes, selected figure hashes and unchanged report.

## Compact release commands

```powershell
.\.venv\Scripts\python.exe check_results.py
.\.venv\Scripts\python.exe make_figures.py
.\.venv\Scripts\python.exe run_analysis.py
```

The packaged checks passed: five regression tests, 115 detection strata, all 10 B and 13 X definitions, denominator reconciliation, 1,794 continuous morphology tests, 2,208 categorical contrasts, 672 condition-morphology tests, corrected IITB X3 statistics, failure-reason reconciliation, three frozen hashes, 27 selected PNG hashes and the report hash.

## Raw-data replay command

```powershell
.\.venv\Scripts\python.exe run_analysis.py --data-root "D:\path\to\Variability Analysis"
```

This command was run successfully from the compact repository against the authorised local data root. The data path is not stored in the repository. Future source replay remains conditional on authorised local access to the raw datasets and preserved HeartCycle canonical comparison outputs described in `docs/dataset_setup.md`.
