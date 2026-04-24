# R-task stub: `epigen-rnaseq_pipeline-finish` / `stage_06`

> **Status:** stub — evaluation inputs, metrics, and gold outputs are **not** filled in yet.
> Pipeline overlay comes from `paper_primary_benchmark/task_definitions/epigen-rnaseq_pipeline-finish.json`.

## Stage

- **Label:** Automated stage 6 (3 finish steps)
- **Order:** 6
- **Finish manifest (reference):** `finish/epigen-rnaseq_pipeline-finish/manifest.json`

## Snakemake steps in this stage

- `trim_filter`
- `align`
- `count_matrix`

## Summary (from task_definitions metadata)

Contiguous partition from finish manifest order; refine labels and IO as needed.

### Declared inputs (path hints)
- **upstream** — (from steps: trim_filter)

### Declared outputs (path hints)
- **checkpoint_last_step** — `results/finish/count_matrix.done` — (from steps: count_matrix)

## TODO — fill before marking `status: ready` in registry

1. **Data:** Place minimal inputs under `input/` (or document symlinks/capsules). Do not commit large raw data without LFS or external URLs.
2. **Objective:** Replace this stub text with precise success criteria (files, metrics, thresholds).
3. **Gold / baseline:** Optional path to expected artifacts or a Snakemake/finish command used to produce reference outputs.
4. **Environment:** Note R/Bioconductor/conda requirements if different from the default pilot.

## Default env hint

`RTaskEvalEnv` expects a success artifact (see registry `success_artifact_glob`, default `output/result.txt`) before `submit_done(success=true)` with reward.
