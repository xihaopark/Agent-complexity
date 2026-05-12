# R-task stub: `tgirke-systempiperdata-riboseq-finish` / `stage_08`

> **Status:** stub — evaluation inputs, metrics, and gold outputs are **not** filled in yet.
> Pipeline overlay comes from `paper_primary_benchmark/task_definitions/tgirke-systempiperdata-riboseq-finish.json`.

## Stage

- **Label:** Automated stage 8 (4 finish steps)
- **Order:** 8
- **Finish manifest (reference):** `finish/tgirke-systempiperdata-riboseq-finish/manifest.json`

## Snakemake steps in this stage

- `diff_loading`
- `diff_translational_eff`
- `heatmap`
- `sessionInfo`

## Summary (from task_definitions metadata)

Contiguous partition from finish manifest order; refine labels and IO as needed.

### Declared inputs (path hints)
- **upstream** — (from steps: diff_loading)

### Declared outputs (path hints)
- **checkpoint_last_step** — `results/finish/sessionInfo.done` — (from steps: sessionInfo)

## TODO — fill before marking `status: ready` in registry

1. **Data:** Place minimal inputs under `input/` (or document symlinks/capsules). Do not commit large raw data without LFS or external URLs.
2. **Objective:** Replace this stub text with precise success criteria (files, metrics, thresholds).
3. **Gold / baseline:** Optional path to expected artifacts or a Snakemake/finish command used to produce reference outputs.
4. **Environment:** Note R/Bioconductor/conda requirements if different from the default pilot.

## Default env hint

`RTaskEvalEnv` expects a success artifact (see registry `success_artifact_glob`, default `output/result.txt`) before `submit_done(success=true)` with reward.
