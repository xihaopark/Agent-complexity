# R-task stub: `dna-seq-short-read-circle-map-finish` / `stage_05`

> **Status:** stub — evaluation inputs, metrics, and gold outputs are **not** filled in yet.
> Pipeline overlay comes from `paper_primary_benchmark/task_definitions/dna-seq-short-read-circle-map-finish.json`.

## Stage

- **Label:** Automated stage 5 (3 finish steps)
- **Order:** 5
- **Finish manifest (reference):** `finish/dna-seq-short-read-circle-map-finish/manifest.json`

## Snakemake steps in this stage

- `samtools_sort_candidates`
- `circle_map_realign`
- `clean_circle_map_realign_output`

## Summary (from task_definitions metadata)

Contiguous partition from finish manifest order; refine labels and IO as needed.

### Declared inputs (path hints)
- **upstream** — (from steps: samtools_sort_candidates)

### Declared outputs (path hints)
- **checkpoint_last_step** — `results/finish/clean_circle_map_realign_output.done` — (from steps: clean_circle_map_realign_output)

## TODO — fill before marking `status: ready` in registry

1. **Data:** Place minimal inputs under `input/` (or document symlinks/capsules). Do not commit large raw data without LFS or external URLs.
2. **Objective:** Replace this stub text with precise success criteria (files, metrics, thresholds).
3. **Gold / baseline:** Optional path to expected artifacts or a Snakemake/finish command used to produce reference outputs.
4. **Environment:** Note R/Bioconductor/conda requirements if different from the default pilot.

## Default env hint

`RTaskEvalEnv` expects a success artifact (see registry `success_artifact_glob`, default `output/result.txt`) before `submit_done(success=true)` with reward.
