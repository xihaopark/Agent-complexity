# R-task stub: `epigen-fetch_ngs-finish` / `merge_and_finalize`

> **Status:** stub — evaluation inputs, metrics, and gold outputs are **not** filled in yet.
> Pipeline overlay comes from `paper_primary_benchmark/task_definitions/epigen-fetch_ngs-finish.json`.

## Stage

- **Label:** 元数据合并与收尾
- **Order:** 3
- **Finish manifest (reference):** `finish/epigen-fetch_ngs-finish/manifest.json`

## Snakemake steps in this stage

- `merge_metadata`
- `all`

## Summary (from task_definitions metadata)

Merge metadata and run final aggregate target.

### Declared inputs (path hints)
- **fetch_outputs** — (from steps: fetch_file)

### Declared outputs (path hints)
- **final_checkpoint** — `results/finish/all.done` — (from steps: all)

## TODO — fill before marking `status: ready` in registry

1. **Data:** Place minimal inputs under `input/` (or document symlinks/capsules). Do not commit large raw data without LFS or external URLs.
2. **Objective:** Replace this stub text with precise success criteria (files, metrics, thresholds).
3. **Gold / baseline:** Optional path to expected artifacts or a Snakemake/finish command used to produce reference outputs.
4. **Environment:** Note R/Bioconductor/conda requirements if different from the default pilot.

## Default env hint

`RTaskEvalEnv` expects a success artifact (see registry `success_artifact_glob`, default `output/result.txt`) before `submit_done(success=true)` with reward.
