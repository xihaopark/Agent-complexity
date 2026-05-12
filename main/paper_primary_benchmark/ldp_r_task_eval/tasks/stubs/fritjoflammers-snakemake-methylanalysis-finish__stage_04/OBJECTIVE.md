# R-task stub: `fritjoflammers-snakemake-methylanalysis-finish` / `stage_04`

> **Status:** stub — evaluation inputs, metrics, and gold outputs are **not** filled in yet.
> Pipeline overlay comes from `paper_primary_benchmark/task_definitions/fritjoflammers-snakemake-methylanalysis-finish.json`.

## Stage

- **Label:** Automated stage 4 (4 finish steps)
- **Order:** 4
- **Finish manifest (reference):** `finish/fritjoflammers-snakemake-methylanalysis-finish/manifest.json`

## Snakemake steps in this stage

- `notebook_data_structure`
- `gemma_subset_samples`
- `macau_prep_counts_file`
- `extract_column_from_spreadsheet`

## Summary (from task_definitions metadata)

Contiguous partition from finish manifest order; refine labels and IO as needed.

### Declared inputs (path hints)
- **upstream** — (from steps: notebook_data_structure)

### Declared outputs (path hints)
- **checkpoint_last_step** — `results/finish/extract_column_from_spreadsheet.done` — (from steps: extract_column_from_spreadsheet)

## TODO — fill before marking `status: ready` in registry

1. **Data:** Place minimal inputs under `input/` (or document symlinks/capsules). Do not commit large raw data without LFS or external URLs.
2. **Objective:** Replace this stub text with precise success criteria (files, metrics, thresholds).
3. **Gold / baseline:** Optional path to expected artifacts or a Snakemake/finish command used to produce reference outputs.
4. **Environment:** Note R/Bioconductor/conda requirements if different from the default pilot.

## Default env hint

`RTaskEvalEnv` expects a success artifact (see registry `success_artifact_glob`, default `output/result.txt`) before `submit_done(success=true)` with reward.
