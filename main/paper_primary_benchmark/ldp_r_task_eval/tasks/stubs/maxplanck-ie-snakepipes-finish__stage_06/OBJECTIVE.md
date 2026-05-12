# R-task stub: `maxplanck-ie-snakepipes-finish` / `stage_06`

> **Status:** stub — evaluation inputs, metrics, and gold outputs are **not** filled in yet.
> Pipeline overlay comes from `paper_primary_benchmark/task_definitions/maxplanck-ie-snakepipes-finish.json`.

## Stage

- **Label:** Automated stage 6 (5 finish steps)
- **Order:** 6
- **Finish manifest (reference):** `finish/maxplanck-ie-snakepipes-finish/manifest.json`

## Snakemake steps in this stage

- `MACS2_peak_qc`
- `CSAW`
- `calc_matrix_log2r_CSAW`
- `plot_heatmap_log2r_CSAW`
- `calc_matrix_cov_CSAW`

## Summary (from task_definitions metadata)

Contiguous partition from finish manifest order; refine labels and IO as needed.

### Declared inputs (path hints)
- **upstream** — (from steps: MACS2_peak_qc)

### Declared outputs (path hints)
- **checkpoint_last_step** — `results/finish/calc_matrix_cov_CSAW.done` — (from steps: calc_matrix_cov_CSAW)

## TODO — fill before marking `status: ready` in registry

1. **Data:** Place minimal inputs under `input/` (or document symlinks/capsules). Do not commit large raw data without LFS or external URLs.
2. **Objective:** Replace this stub text with precise success criteria (files, metrics, thresholds).
3. **Gold / baseline:** Optional path to expected artifacts or a Snakemake/finish command used to produce reference outputs.
4. **Environment:** Note R/Bioconductor/conda requirements if different from the default pilot.

## Default env hint

`RTaskEvalEnv` expects a success artifact (see registry `success_artifact_glob`, default `output/result.txt`) before `submit_done(success=true)` with reward.
