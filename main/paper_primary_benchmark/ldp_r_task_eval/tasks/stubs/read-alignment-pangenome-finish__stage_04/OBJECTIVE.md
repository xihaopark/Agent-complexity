# R-task stub: `read-alignment-pangenome-finish` / `stage_04`

> **Status:** stub — evaluation inputs, metrics, and gold outputs are **not** filled in yet.
> Pipeline overlay comes from `paper_primary_benchmark/task_definitions/read-alignment-pangenome-finish.json`.

## Stage

- **Label:** Automated stage 4 (5 finish steps)
- **Order:** 4
- **Finish manifest (reference):** `finish/read-alignment-pangenome-finish/manifest.json`

## Snakemake steps in this stage

- `count_sample_kmers`
- `create_reference_paths`
- `map_reads_vg`
- `reheader_mapped_reads`
- `fix_mate`

## Summary (from task_definitions metadata)

Contiguous partition from finish manifest order; refine labels and IO as needed.

### Declared inputs (path hints)
- **upstream** — (from steps: count_sample_kmers)

### Declared outputs (path hints)
- **checkpoint_last_step** — `results/finish/fix_mate.done` — (from steps: fix_mate)

## TODO — fill before marking `status: ready` in registry

1. **Data:** Place minimal inputs under `input/` (or document symlinks/capsules). Do not commit large raw data without LFS or external URLs.
2. **Objective:** Replace this stub text with precise success criteria (files, metrics, thresholds).
3. **Gold / baseline:** Optional path to expected artifacts or a Snakemake/finish command used to produce reference outputs.
4. **Environment:** Note R/Bioconductor/conda requirements if different from the default pilot.

## Default env hint

`RTaskEvalEnv` expects a success artifact (see registry `success_artifact_glob`, default `output/result.txt`) before `submit_done(success=true)` with reward.
